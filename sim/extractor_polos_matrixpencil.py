#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXTRACTOR ESPECTRAL DE POLOS COMPLEJOS - PRONY / MATRIX PENCIL METHOD (MPM)

HUELLA-EXTRACTOR-ESPECTRAL-PRONY-MATRIXPENCIL-20261013

Pre-registro sellado (append-only):
    sim/PREREGISTRO_EXTRACTOR_ESPECTRAL_20261013.md
    157 lineas | 12113 B | sha16 3a707f6cade6d6bc
    blob ecd55fef00a79ca3d5e239e232c680791f8f6edb

OBJETO
------
Serie real y[m] muestreada con paso dt, dominada por oscilaciones amortiguadas:

    Psi(t) = Suma_n |A_n| * exp(-wI_n * t) * cos(wR_n * t + fase_n)
    s_n = -wI_n + i*wR_n      (wI_n > 0  =>  decaimiento)

ALGEBRA SELLADA (preregistro seccion 3)
---------------------------------------
  1. normalizacion  y <- y / max|y|          (se reporta el factor)
  2. Hankel         Y0[m,k] = y[m+k] ; Y1[m,k] = y[m+k+1]   (M + L = N)
  3. SVD            Y0 = U * S * V^H
  4. rango          r = 2K  DECLARADO a priori (auto-deteccion = solo diagnostico)
  5. polos          Z = inv(S_r) * U_r^H * Y1 * V_r ;  z_k = eig(Z)
  6. plano s        s_k = ln(z_k) / dt
  7. amplitudes     minimos cuadrados sobre la Vandermonde z_k^m (base REAL)

CONTRASTE: Prony / prediccion lineal (LP), misma serie, mismo contrato.
Se reporta la DISCREPANCIA entre rutas; no se elige una.

NOTACION OBLIGATORIA DEL ERROR
------------------------------
    ds = dz / (z * dt)   =>   ds/s = dz / (z * |s| * dt)

La precision absoluta en s NO se puede separar de dt: es propiedad del PAR
(dt, |s|), no del extractor. Por eso se imprime |s| * dt junto a cada error.

CORTES DE FALLO (preregistro seccion 7, sellados antes de la primera linea
de codigo): C1 F1 F2 F3 F4 F5 F6 F7 F8. Ver --ayuda-cortes.

SALIDA: crudo JSON en sim/data/crudo_extractor_<tag>_<UTC>.json y por stdout.
UNIVERSO DECLARADO: este archivo (1 pieza) + sim/driver_rw_zerilli_1d.py
(1 pieza, SOLO LECTURA: jamas se modifica) + el crudo que este instrumento escribe.
MOTOR: python 3.x + numpy (version impresa en la cabecera del crudo).
UNIDAD: linea | polo | valor singular | muestra | decibelio.
VENTANA: reloj UTC impreso en la cabecera del crudo, junto al UNIVERSO y al MOTOR.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import os
import platform
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

HUELLA = "HUELLA-EXTRACTOR-ESPECTRAL-PRONY-MATRIXPENCIL-20261013"
PREREGISTRO = "sim/PREREGISTRO_EXTRACTOR_ESPECTRAL_20261013.md"
PREREG_SHA16 = "3a707f6cade6d6bc"
PREREG_BLOB = "ecd55fef00a79ca3d5e239e232c680791f8f6edb"

EPS = 2.220446049250313e-16
RANK_REL = 1.0e-12
SEMILLA_RUIDO = 20261013

UMBRAL_C1 = 1.0e-14
UMBRAL_F1 = 1.0e-13
UMBRAL_F3_GAP = 1.0e6
UMBRAL_F4_COND = 1.0e10
UMBRAL_F5_CONJ = 1.0e-10
UMBRAL_F7_PERIODOS = 20.0
UMBRAL_F8 = 5.0e-2
TOL_EMPAREJA = 0.25

LEAVER_WR = 0.37367
LEAVER_WI = 0.08896

# Tabla de polos sellada (preregistro seccion 5). Orden canonico: n = 1, 2, 3.
POLOS_REF = (
    {"n": 1, "wR": 0.37367, "wI": 0.08896, "amp": 1.00, "fase": 0.0,
     "origen": "Leaver l=2 n=0 [REF]"},
    {"n": 2, "wR": 0.60000, "wI": 0.20000, "amp": 0.50, "fase": math.pi / 3.0,
     "origen": "sintetico declarado"},
    {"n": 3, "wR": 0.15000, "wI": 0.12000, "amp": 0.25, "fase": -math.pi / 5.0,
     "origen": "sintetico declarado"},
)


# --------------------------------------------------------------------------- #
# utilidades de identidad y de crudo
# --------------------------------------------------------------------------- #
def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def git_blob(path: str) -> str:
    p = os.path.abspath(path)
    try:
        r = subprocess.run(
            ["git", "-C", os.path.dirname(p), "hash-object", "--", p],
            capture_output=True, text=True, check=False,
        )
        out = r.stdout.strip()
        return out if out else None
    except Exception:
        return None


def san(x):
    """Sanea el crudo: los no finitos van a null (NO a 0). Se declara en la cabecera."""
    if isinstance(x, dict):
        return {k: san(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [san(v) for v in x]
    if isinstance(x, (np.floating, float)):
        v = float(x)
        return v if math.isfinite(v) else None
    if isinstance(x, (np.integer, int)):
        return int(x)
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    if isinstance(x, complex):
        return {"re": san(x.real), "im": san(x.imag)}
    return x


# --------------------------------------------------------------------------- #
# senal sintetica + ruido controlado
# --------------------------------------------------------------------------- #
def synth_series(dt, N, K, t0=0.0):
    """Genera Psi(t_m) EN MEMORIA con los K primeros polos de la tabla sellada."""
    t = t0 + dt * np.arange(N, dtype=float)
    y = np.zeros(N, dtype=float)
    ref = []
    for p in POLOS_REF[:K]:
        y += p["amp"] * np.exp(-p["wI"] * t) * np.cos(p["wR"] * t + p["fase"])
        ref.append({
            "n": p["n"], "wR": p["wR"], "wI": p["wI"], "amp": p["amp"],
            "fase": p["fase"], "origen": p["origen"],
            "s_ref": complex(-p["wI"], p["wR"]), "abs_s": abs(complex(-p["wI"], p["wR"])),
        })
    return t, y, ref


def sigma_para_snr(y, snr_db):
    """sigma tal que 10*log10(Suma y^2 / Suma n^2) = snr_db sobre ESTA ventana."""
    e = float(np.sum(np.square(y)))
    return math.sqrt(e / (y.size * (10.0 ** (snr_db / 10.0))))


def aplicar_ruido(y, snr_db, rng):
    sigma = sigma_para_snr(y, snr_db)
    n = rng.normal(0.0, sigma, size=y.size)
    return y + n, n, float(sigma)


def snr_medido_db(senal, ruido):
    en = float(np.sum(np.square(ruido)))
    if en <= 0.0:
        return float("inf")
    return 10.0 * math.log10(float(np.sum(np.square(senal))) / en)


# --------------------------------------------------------------------------- #
# nucleo algebraico
# --------------------------------------------------------------------------- #
def build_hankel(y, L):
    """Y0[m,k] = y[m+k] ; Y1[m,k] = y[m+k+1].  M = N - L."""
    N = int(y.size)
    M = N - L
    idx = np.arange(M)[:, None] + np.arange(L)[None, :]
    Y0 = y[idx]
    Y1 = y[idx + 1]
    return Y0, Y1


def mpm(y, dt, K, L=None):
    """Matrix Pencil Method. Devuelve autovalores z y diagnostico.

    Declarado (medido 2026-10-13T11:00Z): Z = (Ur^H Y1 Vr)/sr es REAL porque
    Y0, Y1 y la SVD de una matriz real son reales => np.linalg.eigvals(Z)
    devuelve pares conjugados EXACTOS => residuo_conjugado es 0.0 por
    construccion. F5 mide coherencia del apareamiento, NO realidad de la
    serie: se declara INERTE por construccion y no se lee como evidencia.
    """
    N = int(y.size)
    if L is None:
        L = N // 2
    if not (2 * K <= min(N - L, L)):
        raise ValueError("rango 2K=%d incompatible con M=%d L=%d" % (2 * K, N - L, L))
    Y0, Y1 = build_hankel(y, L)
    U, sv, Vh = np.linalg.svd(Y0, full_matrices=False)
    V = Vh.conj().T
    r = 2 * K
    Ur, sr, Vr = U[:, :r], sv[:r], V[:, :r]
    Z = (Ur.conj().T @ Y1 @ Vr) / sr[:, None]
    z = np.linalg.eigvals(Z)

    d = {
        "L": int(L), "M": int(N - L), "rango_declarado": int(r),
        "sv_top": float(sv[0]),
        "sv_min_empaquetado": float(sv[-1]),
        "rank_rel_1e-12": int(np.sum(sv / sv[0] >= RANK_REL)),
        "rank_efectivo_2K": bool(sv.size >= r and sv[r - 1] > 0.0),
        "gap_sv_2K_2K1": (float(sv[r - 1] / sv[r]) if (r < sv.size and sv[r] > 0.0)
                          else float("inf")),
        "cond_Z": float(np.linalg.cond(Z)),
        "residuo_conjugado": 0.0,
        "residuo_conjugado_evaluado": False,
        "residuo_conjugado_pares": [],
    }
    # F5 — apareamiento conjugado: distancia de conj(z_i) al polo MAS CERCANO
    # DISTINTO de z_i mismo, normalizada por |z_i|.
    # El termino propio |z_i - conj(z_i)| = 2|Im z_i| NO es un residuo de
    # apareamiento y se excluye por INDICE (dist[i] = inf). El filtro
    # "dist > 0.0" de la V1 borraba al socio exacto (Z real => autovalores
    # conjugados bit a bit) y dejaba medido el termino propio.
    if z.size > 1:
        res = 0.0
        pares = []
        for i in range(z.size):
            zi = z[i]
            if zi.imag <= 0.0:
                continue
            dist = np.abs(z - np.conj(zi))
            dist[i] = float("inf")
            j = int(np.argmin(dist))
            if not np.isfinite(dist[j]):
                continue
            rel = float(dist[j]) / max(abs(zi), 1e-300)
            pares.append({"i": int(i), "j": j, "dist_abs": float(dist[j]),
                          "dist_rel": rel})
            res = max(res, rel)
        if pares:
            d["residuo_conjugado"] = res
            d["residuo_conjugado_evaluado"] = True
            d["residuo_conjugado_pares"] = pares
    return z, d


def prony_lp(y, dt, K):
    """Prony / prediccion lineal: y_m = Suma_{k=1..p} a_k y_{m-k}, p = 2K."""
    N = int(y.size)
    p = 2 * K
    if p >= N:
        raise ValueError("p=2K=%d no cabe en N=%d" % (p, N))
    A = np.empty((N - p, p), dtype=float)
    for k in range(1, p + 1):
        A[:, k - 1] = y[p - k:N - k]
    b = y[p:]
    coef, _res, _rk, _sv = np.linalg.lstsq(A, b, rcond=None)
    poly = np.concatenate(([1.0], -coef))
    z = np.roots(poly)
    d = {
        "p": int(p), "filas_LS": int(N - p),
        "cond_A": float(np.linalg.cond(A)),
        "residuo_LS": float(np.linalg.norm(A @ coef - b)),
        "norma_b": float(np.linalg.norm(b)),
        "residuo_rel_LS": float(np.linalg.norm(A @ coef - b) / max(np.linalg.norm(b), 1e-300)),
    }
    return z, d


def reps_de_z(z, dt):
    """Representantes con Im(z) > 0 -> polos con wR > 0. Orden determinista."""
    with np.errstate(invalid="ignore", divide="ignore"):
        s = np.log(np.asarray(z, dtype=complex)) / dt
    reps = []
    for i in range(len(z)):
        if z[i].imag > 0.0:
            reps.append({
                "z": complex(z[i]), "s": complex(s[i]),
                "wR": float(s[i].imag), "wI": float(-s[i].real),
            })
    reps.sort(key=lambda d: (-d["wR"], d["wI"]))
    return reps


def amplitudes(y, reps):
    """LS sobre la base REAL [Re(z^m), Im(z^m)] por representante.

    y = Suma_reps [ a_k Re(z_k^m) + b_k Im(z_k^m) ] = Suma_reps Re[ c_k z_k^m ],
    con c_k = a_k - i b_k.  =>  |A| = |c_k| ; fase = arg(c_k).
    """
    m = np.arange(int(y.size))
    cols = []
    for d in reps:
        zz = np.power(d["z"], m)
        cols.append(zz.real)
        cols.append(zz.imag)
    if not cols:
        return [], None, None
    V = np.column_stack(cols)
    coef, _res, _rk, _sv = np.linalg.lstsq(V, y, rcond=None)
    for i, d in enumerate(reps):
        a = float(coef[2 * i])
        b = float(coef[2 * i + 1])
        d["amp"] = math.hypot(a, b)
        d["fase"] = math.atan2(-b, a)
    return reps, coef, V


def extraer(y, dt, K, metodo="mpm", L=None):
    """Extrae representantes [z, s, wR, wI, |A|, fase] mas el diagnostico."""
    if metodo == "mpm":
        z, diag = mpm(y, dt, K, L=L)
    elif metodo == "prony":
        z, diag = prony_lp(y, dt, K)
    else:
        raise ValueError("metodo desconocido: %s" % metodo)
    reps = reps_de_z(z, dt)
    reps, coef, Vb = amplitudes(y, reps)
    # Diagnostico declarado (no es corte sellado): quien SI prueba que la serie
    # se leyo como real es este residuo sobre la base real [Re z^m, Im z^m].
    # Dominio: sin ruido ~ piso numerico; con ruido ~ nivel de ruido. No se
    # convierte en corte: el pre-registro sellado no tiene umbral para el.
    if coef is not None:
        rv = Vb @ coef - np.asarray(y, dtype=float)
        nr = float(np.linalg.norm(rv))
        diag["residuo_reconstruccion_abs"] = nr
        diag["residuo_reconstruccion_rel"] = nr / max(float(np.linalg.norm(y)), 1e-300)
    else:
        diag["residuo_reconstruccion_abs"] = None
        diag["residuo_reconstruccion_rel"] = None
    for d in reps:
        d["abs_s"] = abs(d["s"])
        d["abs_s_dt"] = abs(d["s"]) * dt
    return reps, diag, z


# --------------------------------------------------------------------------- #
# emparejamiento rec <-> ref y errores
# --------------------------------------------------------------------------- #
def emparejar(rec, ref, tol=TOL_EMPAREJA):
    """Emparejamiento global voraz por distancia creciente en el plano s.

    Cota declarada: |ds| < tol * |s_ref|.  Un polo sin pareja = NO RECUPERADO.
    """
    cand = []
    for i, r in enumerate(ref):
        for j, d in enumerate(rec):
            ds = abs(d["s"] - r["s_ref"])
            if ds < tol * abs(r["s_ref"]):
                cand.append((float(ds), i, j))
    cand.sort()
    usados_ref, usados_rec, asign = set(), set(), {}
    for ds, i, j in cand:
        if i in usados_ref or j in usados_rec:
            continue
        usados_ref.add(i)
        usados_rec.add(j)
        asign[i] = (j, ds)
    return asign, usados_rec


def errores(reps, ref, dt, tol=TOL_EMPAREJA):
    asign, usados = emparejar(reps, ref, tol)
    filas = []
    for i, r in enumerate(ref):
        if i in asign:
            j, ds = asign[i]
            d = reps[j]
            filas.append({
                "n": r["n"], "recuperado": True,
                "wR_ref": r["wR"], "wI_ref": r["wI"],
                "wR_rec": d["wR"], "wI_rec": d["wI"],
                "err_wR_abs": abs(d["wR"] - r["wR"]),
                "err_wI_abs": abs(d["wI"] - r["wI"]),
                "err_s_abs": float(ds),
                "err_s_rel": float(ds / abs(r["s_ref"])),
                "abs_s": r["abs_s"], "abs_s_dt": r["abs_s"] * dt,
                "modA_ref": r["amp"], "modA_rec": d.get("amp"),
                "fase_ref": r["fase"], "fase_rec": d.get("fase"),
                "origen": r["origen"],
            })
        else:
            filas.append({
                "n": r["n"], "recuperado": False,
                "wR_ref": r["wR"], "wI_ref": r["wI"],
                "err_wR_abs": None, "err_wI_abs": None,
                "err_s_abs": None, "err_s_rel": None,
                "abs_s": r["abs_s"], "abs_s_dt": None,
                "modA_ref": r["amp"], "modA_rec": None,
                "fase_ref": r["fase"], "fase_rec": None,
                "origen": r["origen"],
            })
    sobran = [reps[j] for j in range(len(reps)) if j not in usados]
    return filas, sobran


def bloque_polos(reps, dt):
    return [{
        "wR": d["wR"], "wI": d["wI"],
        "z_re": d["z"].real, "z_im": d["z"].imag,
        "s_re": d["s"].real, "s_im": d["s"].imag,
        "abs_s": d["abs_s"], "abs_s_dt": d["abs_s_dt"],
        "modA": d.get("amp"), "fase": d.get("fase"),
    } for d in reps]


def resumen_errores(filas):
    rec = [f for f in filas if f["recuperado"]]
    if not rec:
        return {"n_recuperados": 0, "n_objetivo": len(filas),
                "err_s_rel_max": None, "err_wR_abs_max": None, "err_wI_abs_max": None}
    return {
        "n_recuperados": len(rec), "n_objetivo": len(filas),
        "err_s_rel_max": max(f["err_s_rel"] for f in rec),
        "err_wR_abs_max": max(f["err_wR_abs"] for f in rec),
        "err_wI_abs_max": max(f["err_wI_abs"] for f in rec),
        "err_s_rel_por_polo": {str(f["n"]): f["err_s_rel"] for f in rec},
    }


# --------------------------------------------------------------------------- #
# un caso completo
# --------------------------------------------------------------------------- #
def cortes(caso):
    """Cortes sellados evaluables en un caso aislado (F6 y F8 son de suite).

    El diagnostico viaja APLANADO dentro de caso['mpm'] (no bajo 'diag'):
    la ruta se declara aqui porque un KeyError silencioso no es un corte.
    """
    e = caso["mpm"]["resumen"]["err_s_rel_max"]
    sin_ruido = caso["entrada"]["snr_objetivo"] is None
    conj_eval = bool(caso["mpm"].get("residuo_conjugado_evaluado", False))
    conj_val = caso["mpm"]["residuo_conjugado"]
    return {
        "C1": bool(sin_ruido and e is not None and e <= UMBRAL_C1),
        "F1": bool(sin_ruido and e is not None and e > UMBRAL_F1),
        # F2 sellado dice "sin ruido": con ruido el conteo de valores singulares
        # mide el piso de ruido, no el rango del objeto. Defecto de dominio
        # medido en la V1 (lo evaluaba siempre); se aplica la letra del sello.
        "F2": bool(sin_ruido and caso["mpm"]["rank_rel_1e-12"]
                   != caso["mpm"]["rango_declarado"]),
        "F3": bool(caso["mpm"]["gap_sv_2K_2K1"] < UMBRAL_F3_GAP),
        "F4": bool(caso["mpm"]["cond_Z"] > UMBRAL_F4_COND),
        # F5 con GUARDA: un residuo 0.0 SIN pares medidos no es un verde, es un
        # cero sin objeto (la identidad se satisface sola). F5_evaluado lo dice.
        "F5": bool(conj_eval and conj_val is not None and conj_val > UMBRAL_F5_CONJ),
        "F5_evaluado": conj_eval,
        "F7": bool(caso["entrada"]["W_periodos_lento"] < UMBRAL_F7_PERIODOS),
    }


def correr_caso(K, dt, N, snr_db=None, W=None, seed=SEMILLA_RUIDO, L=None,
                tol=TOL_EMPAREJA):
    t, y, ref = synth_series(dt, N, K)
    if W is not None and 0 < W < N:
        t, y = t[:W], y[:W]
    W_ef = int(y.size)
    escala = float(np.max(np.abs(y)))
    if escala <= 0.0:
        escala = 1.0
    yn = y / escala
    n = None
    snr_med = None
    sigma = None
    if snr_db is not None:
        rng = np.random.default_rng(seed)
        yn, n, sigma = aplicar_ruido(yn, snr_db, rng)
        snr_med = snr_medido_db(y / escala, n)

    T_lento = 2.0 * math.pi / POLOS_REF[K - 1]["wR"]

    out = {
        "entrada": {
            "K": int(K), "dt": dt, "N": W_ef, "N_pedido": int(N), "W": W_ef,
            "T": float(dt * (W_ef - 1)), "t0": float(t[0]),
            "snr_objetivo": snr_db, "snr_medido": snr_med, "sigma_ruido": sigma,
            "semilla": (seed if snr_db is not None else None),
            "escala_normalizacion": escala,
            "W_periodos_lento": float(dt * (W_ef - 1) / T_lento),
            "T_lento": float(T_lento),
            "polos_ref": [{"n": r["n"], "wR": r["wR"], "wI": r["wI"], "abs_s": r["abs_s"],
                           "modA": r["amp"], "fase": r["fase"], "origen": r["origen"]}
                          for r in ref],
        },
        "mpm": {}, "prony": {}, "discrepancia_MPM_vs_Prony": {}, "cortes": {},
    }

    for metodo, clave in (("mpm", "mpm"), ("prony", "prony")):
        reps, diag, z = extraer(yn, dt, K, metodo=metodo, L=L)
        fil, sobran = errores(reps, ref, dt=dt, tol=tol)
        res = resumen_errores(fil)
        blq = {"polos": bloque_polos(reps, dt), "errores": fil,
               "resumen": res, "sobran": bloque_polos(sobran, dt),
               "n_sobran": len(sobran)}
        blq.update({k: v for k, v in diag.items() if not isinstance(v, np.ndarray)})
        out[clave] = blq

    # discrepancia entre rutas (misma serie, mismo contrato, algebra distinta)
    # Orientacion declarada de emparejar(rec, ref): asign[i] = (j, ds) con i
    # indexando ref y j indexando rec. Aqui rec = polos de MPM y ref = polos de
    # Prony => polo_prony = i + 1, polo_mpm = j + 1. Se declara porque una
    # etiqueta invertida se lee como hallazgo y no lo es.
    polos_mpm = [{"s": complex(p["s_re"], p["s_im"])} for p in out["mpm"]["polos"]]
    polos_prony = [{"s_ref": complex(p["s_re"], p["s_im"]), "n": i + 1}
                   for i, p in enumerate(out["prony"]["polos"])]
    disc = []
    a_asig = emparejar(polos_mpm, polos_prony)[0] if polos_mpm else {}
    for i in sorted(a_asig):
        j, ds = a_asig[i]
        disc.append({"polo_prony": i + 1, "polo_mpm": j + 1, "ds_abs": float(ds)})
    out["discrepancia_MPM_vs_Prony"] = {
        "orientacion": "polo_prony = indice en prony (ref); polo_mpm = indice en mpm (rec)",
        "pares": disc,
        "n_pares": len(disc),
        "n_prony": len(out["prony"]["polos"]),
        "n_mpm": len(out["mpm"]["polos"]),
        "ds_abs_max": (max(d["ds_abs"] for d in disc) if disc else None),
    }
    out["cortes"] = cortes(out)
    return out


# --------------------------------------------------------------------------- #
# suites
# --------------------------------------------------------------------------- #
def suite_sintetico(args):
    """Control cerrado: K = 1, 2, 3 sin ruido; y K=3 con el ruido declarado."""
    out = {}
    N = int(round(args.T_sint / args.dt_sint)) + 1
    for K in (1, 2, 3):
        out["sin_ruido_K%d" % K] = correr_caso(K, args.dt_sint, N)
    for snr in (args.snr_ref,):
        out["ruido_K3_snr%g" % snr] = correr_caso(3, args.dt_sint, N, snr_db=snr)
    return out


def suite_snr(args):
    out = {"barrido": [], "declarado": {
        "definicion": "SNR_dB = 10*log10( Suma y^2 / Suma n^2 ) sobre LA MISMA ventana de extraccion",
        "no_es": "SNR de pico ni por muestra",
        "semilla": SEMILLA_RUIDO,
    }}
    N = int(round(args.T_sint / args.dt_sint)) + 1
    filas = []
    for snr in (140.0, 120.0, 100.0, 80.0, 60.0, 40.0, 20.0):
        c = correr_caso(3, args.dt_sint, N, snr_db=snr)
        filas.append({
            "snr_objetivo": snr, "snr_medido": c["entrada"]["snr_medido"],
            "err_s_rel_max": c["mpm"]["resumen"]["err_s_rel_max"],
            "err_wR_abs_max": c["mpm"]["resumen"]["err_wR_abs_max"],
            "err_wI_abs_max": c["mpm"]["resumen"]["err_wI_abs_max"],
            "n_recuperados": c["mpm"]["resumen"]["n_recuperados"],
            "gap_sv": c["mpm"]["gap_sv_2K_2K1"], "cond_Z": c["mpm"]["cond_Z"],
            "abs_s_dt_min": min(p["abs_s_dt"] for p in c["mpm"]["polos"]) if c["mpm"]["polos"] else None,
            "cortes": c["cortes"],
        })
    out["barrido"] = filas
    vals = [f["err_s_rel_max"] for f in filas if f["err_s_rel_max"] is not None]
    tendencia = None
    if len(vals) >= 2:
        tendencia = ("BAJA" if vals[0] < vals[-1] else
                     ("SUBE" if vals[0] > vals[-1] else "PLANA"))
    out["F6_tendencia"] = {
        "lectura": tendencia,
        "err_al_snr_max": vals[0] if vals else None,
        "err_al_snr_min": vals[-1] if vals else None,
        "estado": "DECLARADA, NO ADJUDICADA (una sola tirada por celda)",
    }
    return out


def suite_ventana(args):
    """Ventana de corte. Se mide el barrido SELLADO y se mide su dominio."""
    out = {}
    N = int(round(args.T_sint / args.dt_sint)) + 1
    T_lento = 2.0 * math.pi / POLOS_REF[2]["wR"]

    out["dominio_del_sello"] = {
        "que_dice_el_preregistro": "W en {20, 40, 80, 160, 320} periodos del modo mas lento",
        "T_modo_mas_lento": float(T_lento),
        "W_en_unidades_de_tiempo": [float(v * T_lento) for v in (20.0, 40.0, 80.0, 160.0, 320.0)],
        "decaimiento_del_polo_1_al_final": [float(math.exp(-POLOS_REF[0]["wI"] * v * T_lento))
                                            for v in (20.0, 40.0, 80.0, 160.0, 320.0)],
        "eps": EPS,
        "veredicto": ("DEFECTO DE DOMINIO DEL UMBRAL SELLADO: 20 periodos del modo mas lento "
                      "ya son %.1f unidades de tiempo y el polo 1 vale %.3e alli, por debajo "
                      "de eps => no hay objeto que extraer. No se baja el umbral: se declara."
                      % (20.0 * T_lento, math.exp(-POLOS_REF[0]["wI"] * 20.0 * T_lento))),
    }

    filas = []
    for frac, nombre in ((0.125, "W/N=0.125"), (0.25, "W/N=0.25"), (0.5, "W/N=0.5"),
                         (0.75, "W/N=0.75"), (1.0, "W/N=1.0")):
        W = int(round(frac * N))
        c = correr_caso(3, args.dt_sint, N, W=max(W, 2 * 3 + 2))
        filas.append({
            "etiqueta": nombre, "W_muestras": c["entrada"]["W"],
            "T": c["entrada"]["T"], "W_periodos_lento": c["entrada"]["W_periodos_lento"],
            "err_s_rel_max": c["mpm"]["resumen"]["err_s_rel_max"],
            "err_wR_abs_max": c["mpm"]["resumen"]["err_wR_abs_max"],
            "err_wI_abs_max": c["mpm"]["resumen"]["err_wI_abs_max"],
            "n_recuperados": c["mpm"]["resumen"]["n_recuperados"],
            "gap_sv": c["mpm"]["gap_sv_2K_2K1"], "cond_Z": c["mpm"]["cond_Z"],
            "cortes": c["cortes"],
        })
    out["barrido"] = filas
    return out


def suite_dt(args):
    """dt con T fijo: aisla el factor 1/(|s|*dt) de la identidad del error."""
    out = {
        "declarado": {
            "T_fijo": args.T_dt,
            "por_que": "ds/s = dz/(z*|s|*dt): con T fijo, mover dt mueve |s|*dt.",
            "N_resultante": {str(dt): int(round(args.T_dt / dt)) + 1
                             for dt in (0.0125, 0.025, 0.05, 0.1, 0.2, 0.5)},
            "dt_del_driver_k2": "cfl*h con cfl=0.50, delta0=0.05, k=2  =>  dt = 0.0125",
        },
        "barrido": [],
    }
    for dt in (0.0125, 0.025, 0.05, 0.1, 0.2, 0.5):
        N = int(round(args.T_dt / dt)) + 1
        c = correr_caso(3, dt, N)
        out["barrido"].append({
            "dt": dt, "N": c["entrada"]["N"], "T": c["entrada"]["T"],
            "err_s_rel_max": c["mpm"]["resumen"]["err_s_rel_max"],
            "err_wR_abs_max": c["mpm"]["resumen"]["err_wR_abs_max"],
            "err_wI_abs_max": c["mpm"]["resumen"]["err_wI_abs_max"],
            "n_recuperados": c["mpm"]["resumen"]["n_recuperados"],
            "abs_s_dt_min": min(p["abs_s_dt"] for p in c["mpm"]["polos"]) if c["mpm"]["polos"] else None,
            "piso_predicho_eps_sobre_abs_s_dt":
                (EPS / min(p["abs_s_dt"] for p in c["mpm"]["polos"]) if c["mpm"]["polos"] else None),
            "gap_sv": c["mpm"]["gap_sv_2K_2K1"], "cond_Z": c["mpm"]["cond_Z"],
            "cortes": c["cortes"],
        })
    return out


# --------------------------------------------------------------------------- #
# entradas externas
# --------------------------------------------------------------------------- #
def leer_serie(path):
    """Dos columnas t Psi (separadas por blanco, # = comentario) o JSON."""
    p = os.path.abspath(path)
    with open(p, "r", encoding="utf-8") as fh:
        txt = fh.read()
    s = txt.lstrip()
    if s.startswith("{") or s.startswith("["):
        obj = json.loads(txt)
        if isinstance(obj, dict):
            t = obj.get("t")
            y = obj.get("psi", obj.get("psi_obs"))
            if t is None or y is None:
                raise SystemExit("serie JSON sin claves 't' y 'psi'/'psi_obs': %s" % p)
            t = np.asarray(t, dtype=float)
            y = np.asarray(y, dtype=float)
        else:
            arr = np.asarray(obj, dtype=float)
            t, y = arr[:, 0].copy(), arr[:, 1].copy()
    else:
        rows = []
        for ln in txt.splitlines():
            ln = ln.strip()
            if (not ln) or ln.startswith("#"):
                continue
            parts = ln.split()
            if len(parts) < 2:
                continue
            rows.append((float(parts[0]), float(parts[1])))
        if not rows:
            raise SystemExit("serie vacia: %s" % p)
        arr = np.asarray(rows, dtype=float)
        t, y = arr[:, 0].copy(), arr[:, 1].copy()
    dif = np.diff(t)
    if dif.size == 0:
        raise SystemExit("serie con menos de 2 muestras: %s" % p)
    dt = float(np.median(dif))
    uniforme = bool(np.max(np.abs(dif - dt)) <= 1e-9 * max(abs(dt), 1.0))
    return t, y, dt, {"archivo": p, "n": int(t.size), "dt_mediano": dt,
                      "uniforme": uniforme,
                      "dt_max_desvio": float(np.max(np.abs(dif - dt))),
                      "sha256_16": sha256_file(p)[:16]}


def serie_del_driver(args, k=2):
    """Importa el driver EN MODO LECTURA y devuelve (t, psi_obs) de solve()."""
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import driver_rw_zerilli_1d as drv  # noqa: E402

    rs, h, delta = drv.build_mesh(args.rsmin, args.rsmax, args.delta0, k, args.offset)
    dt = float(args.cfl * h)
    r = drv.r_of_rstar(rs, args.M)
    V = drv.V_of(args.potencial, r, args.M, args.l)
    psi0 = drv.gauss(rs, args.xc, args.sigma)
    vhalf = 0.5 * dt * drv.laplaciano(psi0, h, V)
    g = drv.solve(rs, h, float(args.cfl), V, psi0, vhalf, args.tmax,
                  args.sponge_L, args.sponge_A, args.robs)
    info = {
        "k": int(k), "h": float(h), "delta": float(delta), "dt": dt,
        "rsmin": rs[0], "rsmax": rs[-1], "nodos": int(rs.size),
        "nsteps": int(g["nsteps"]), "estable": bool(g["estable"]),
        "robs": float(args.robs), "potencial": args.potencial, "l": args.l,
        "M": args.M, "cfl": args.cfl, "delta0": args.delta0,
        "tmax": args.tmax, "t1": args.t1, "t2": args.t2,
        "driver_sha256_16": sha256_file(os.path.join(HERE, "driver_rw_zerilli_1d.py"))[:16],
        "driver_blob": git_blob(os.path.join(HERE, "driver_rw_zerilli_1d.py")),
        "driver_modificado": False,
    }
    return g["t"], g["psi_obs"], dt, info


def suite_driver(args):
    """Control FISICO: la serie del driver contra Leaver 0.37367 - 0.08896 i."""
    t, y, dt, info = serie_del_driver(args, k=args.k_fisico)
    m = (t >= args.t1) & (t <= args.t2)
    tw, yw = t[m], y[m]
    escala = float(np.max(np.abs(yw)))
    yn = yw / escala
    out = {
        "serie": info,
        "ventana_fisica": {"t1": args.t1, "t2": args.t2, "n": int(yw.size),
                           "T": float(tw[-1] - tw[0]), "escala": escala},
        "leaver_ref": {"wR": LEAVER_WR, "wI": LEAVER_WI,
                       "origen": "Leaver l=2 n=0 [REF] citado del preregistro del driver"},
        "casos": {},
    }
    T_lento = 2.0 * math.pi / LEAVER_WR
    for K in (1, 2, 3):
        reps, diag, z = extraer(yn, dt, K, metodo="mpm")
        fil = []
        for p in reps:
            ds = abs(complex(p["wR"] - LEAVER_WR, p["wI"] - LEAVER_WI))
            ref_norm = math.hypot(LEAVER_WR, LEAVER_WI)
            fil.append({
                "wR": p["wR"], "wI": p["wI"], "abs_s": p["abs_s"],
                "abs_s_dt": p["abs_s_dt"], "modA": p.get("amp"), "fase": p.get("fase"),
                "ds_contra_leaver_abs": float(ds),
                "ds_contra_leaver_rel": float(ds / ref_norm),
                "F8_discrepancia": bool(ds / ref_norm > UMBRAL_F8),
            })
        fil.sort(key=lambda d: d["ds_contra_leaver_abs"])
        out["casos"]["K%d" % K] = {
            "rango_declarado": diag["rango_declarado"],
            "rank_rel_1e-12": diag["rank_rel_1e-12"],
            "gap_sv_2K_2K1": diag["gap_sv_2K_2K1"], "cond_Z": diag["cond_Z"],
            "residuo_conjugado": diag["residuo_conjugado"],
            "W_periodos_lento": float((tw[-1] - tw[0]) / T_lento),
            "mas_cercano": fil[0] if fil else None,
            "polos": fil,
            "F8": bool(fil and fil[0]["F8_discrepancia"]),
        }
    return out


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def cabecera(args):
    motor = {"python": platform.python_version(), "numpy": np.__version__,
             "plataforma": platform.platform()}
    try:
        import scipy  # noqa: F401
        motor["scipy"] = scipy.__version__
    except Exception:
        motor["scipy"] = None
    self_p = os.path.abspath(__file__)
    drv_p = os.path.join(HERE, "driver_rw_zerilli_1d.py")
    cabe = {
        "instrumento": "extractor_polos_matrixpencil (MPM + Prony/LP)",
        "huella": HUELLA,
        "preregistro": {"ruta": PREREGISTRO, "sha16": PREREG_SHA16, "blob": PREREG_BLOB,
                        "append_only": True},
        "t_utc": utc_now(),
        "universo_declarado": ("sim/extractor_polos_matrixpencil.py (1 pieza) + "
                               "sim/driver_rw_zerilli_1d.py (1 pieza, SOLO LECTURA) + "
                               "el crudo que este instrumento escribe"),
        "motor": motor,
        "unidad_declarada": "linea | polo | valor singular | muestra | decibelio",
        "ventana_declarada": "reloj UTC de esta cabecera",
        "no_finitos": "los valores no finitos se imprimen como null, NUNCA como 0",
        "defectos_del_metro_declarados": {
            "F5_inertes_por_construccion": ("Z es real => eigvals devuelve pares "
                                            "conjugados exactos => residuo_conjugado "
                                            "= 0.0 siempre; F5 no puede diferir. "
                                            "Medido en los tres casos limpios."),
            "F2_dominio": ("el sello dice 'sin ruido'; la V1 lo evaluaba tambien con "
                           "ruido, donde el conteo de valores singulares mide el piso "
                           "de ruido. Corregido a la letra del sello: sin ruido."),
            "F7_frontera": "W menor que 20 periodos del modo mas lento: FRONTERA, no falla.",
            "ventana_del_sello": ("el barrido sellado (20..320 periodos del modo mas "
                                  "lento) implica T ~ 337.6 unidades de tiempo, donde "
                                  "el polo 1 vale ~1e-13 y no hay objeto que extraer. Se "
                                  "declara en dominio_del_sello; no se baja el umbral."),
        },
        "argv": sys.argv,
        "modo": args.modo,
        "sha256_self_16": sha256_file(self_p)[:16],
        "blob_self": git_blob(self_p),
        "driver": ({"ruta": "sim/driver_rw_zerilli_1d.py",
                    "sha256_16": sha256_file(drv_p)[:16],
                    "blob": git_blob(drv_p),
                    "modificado_por_este_instrumento": False}
                   if os.path.exists(drv_p) else None),
        "constantes": {
            "EPS": EPS, "RANK_REL": RANK_REL, "SEMILLA_RUIDO": SEMILLA_RUIDO,
            "UMBRAL_C1": UMBRAL_C1, "UMBRAL_F1": UMBRAL_F1, "UMBRAL_F3_GAP": UMBRAL_F3_GAP,
            "UMBRAL_F4_COND": UMBRAL_F4_COND, "UMBRAL_F5_CONJ": UMBRAL_F5_CONJ,
            "UMBRAL_F7_PERIODOS": UMBRAL_F7_PERIODOS, "UMBRAL_F8": UMBRAL_F8,
            "TOL_EMPAREJA": TOL_EMPAREJA,
        },
    }
    return cabe


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Extractor espectral de polos complejos (Prony / Matrix Pencil). "
                    "HUELLA-EXTRACTOR-ESPECTRAL-PRONY-MATRIXPENCIL-20261013",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modo", default="sintetico",
                    choices=["sintetico", "snr", "ventana", "dt", "serie", "driver", "todo"])
    ap.add_argument("--serie", default=None, help="archivo de serie externa (modo serie)")
    ap.add_argument("--desde-driver", action="store_true",
                    help="toma la serie de sim/driver_rw_zerilli_1d.py (solo lectura)")
    ap.add_argument("--K", type=int, default=3, help="numero de polos complejos (rango r = 2K)")

    ap.add_argument("--dt-sint", type=float, default=0.5)
    ap.add_argument("--T-sint", type=float, default=60.0)
    ap.add_argument("--T-dt", type=float, default=20.0)
    ap.add_argument("--snr-ref", type=float, default=100.0)

    ap.add_argument("--potencial", default="rw", choices=["rw", "zerilli", "nulo"])
    ap.add_argument("--l", type=int, default=2)
    ap.add_argument("--M", type=float, default=1.0)
    ap.add_argument("--delta0", type=float, default=0.05)
    ap.add_argument("--cfl", type=float, default=0.50)
    ap.add_argument("--rsmin", type=float, default=-40.0)
    ap.add_argument("--rsmax", type=float, default=150.0)
    ap.add_argument("--tmax", type=float, default=100.0)
    ap.add_argument("--xc", type=float, default=0.0)
    ap.add_argument("--sigma", type=float, default=3.0)
    ap.add_argument("--robs", type=float, default=40.0)
    ap.add_argument("--t1", type=float, default=48.0)
    ap.add_argument("--t2", type=float, default=92.0)
    ap.add_argument("--sponge-L", dest="sponge_L", type=float, default=12.0)
    ap.add_argument("--sponge-A", dest="sponge_A", type=float, default=25.0)
    ap.add_argument("--offset", default="no-anidado", choices=["literal", "no-anidado"])
    ap.add_argument("--k-fisico", type=int, default=2)

    ap.add_argument("--outdir", default=os.path.join("sim", "data"))
    ap.add_argument("--tag", default="base")
    ap.add_argument("--sin-stdout", action="store_true")
    args = ap.parse_args(argv)

    res = {"cabecera": cabecera(args)}

    if args.modo in ("sintetico", "todo"):
        res["sintetico"] = suite_sintetico(args)
    if args.modo in ("snr", "todo"):
        res["snr"] = suite_snr(args)
    if args.modo in ("ventana", "todo"):
        res["ventana"] = suite_ventana(args)
    if args.modo in ("dt", "todo"):
        res["dt"] = suite_dt(args)

    if args.modo in ("serie", "driver"):
        if args.desde_driver or args.modo == "driver":
            t, y, dt, info = serie_del_driver(args, k=args.k_fisico)
            fuente = {"tipo": "driver_rw_zerilli_1d.solve()", "info": info}
        else:
            if not args.serie:
                raise SystemExit("modo serie requiere --serie ARCHIVO o --desde-driver")
            t, y, dt, info = leer_serie(args.serie)
            fuente = {"tipo": "archivo", "info": info}
        m = (t >= args.t1) & (t <= args.t2)
        tw, yw = t[m], y[m]
        if yw.size < 4 * args.K + 4:
            raise SystemExit("ventana fisica con %d muestras: insuficiente para K=%d"
                             % (yw.size, args.K))
        escala = float(np.max(np.abs(yw)))
        yn = yw / escala
        reps, diag, z = extraer(yn, dt, args.K, metodo="mpm")
        reps_p, diag_p, zp = extraer(yn, dt, args.K, metodo="prony")
        res["serie"] = {
            "fuente": fuente,
            "ventana": {"t1": args.t1, "t2": args.t2, "n": int(yw.size),
                        "T": float(tw[-1] - tw[0]), "dt": dt,
                        "escala_normalizacion": escala},
            "mpm": dict({"polos": bloque_polos(reps, dt)}, **diag),
            "prony": dict({"polos": bloque_polos(reps_p, dt)}, **diag_p),
            "leaver_ref": {"wR": LEAVER_WR, "wI": LEAVER_WI,
                           "M_ref": "0.37367 - 0.08896 i (l=2, n=0) [REF]"},
            "contraste_leaver": sorted([
                {"wR": p["wR"], "wI": p["wI"], "abs_s_dt": p["abs_s_dt"],
                 "modA": p.get("amp"),
                 "ds_abs": float(abs(complex(p["wR"] - LEAVER_WR, p["wI"] - LEAVER_WI))),
                 "ds_rel": float(abs(complex(p["wR"] - LEAVER_WR, p["wI"] - LEAVER_WI))
                                 / math.hypot(LEAVER_WR, LEAVER_WI)),
                 "F8": bool(abs(complex(p["wR"] - LEAVER_WR, p["wI"] - LEAVER_WI))
                            / math.hypot(LEAVER_WR, LEAVER_WI) > UMBRAL_F8)}
                for p in reps], key=lambda d: d["ds_abs"]),
        }
        if args.modo == "driver":
            res["fisico"] = suite_driver(args)

    # ---- escritura del crudo ----
    tstamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)
    destino = os.path.join(outdir, "crudo_extractor_%s_%s.json" % (args.tag, tstamp))
    cuerpo = san(res)
    with open(destino, "w", encoding="utf-8") as fh:
        json.dump(cuerpo, fh, indent=1, ensure_ascii=False)
    sys.stderr.write("# CRUDO ESCRITO: %s\n" % destino)
    if not args.sin_stdout:
        json.dump(cuerpo, sys.stdout, indent=1, ensure_ascii=False)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
