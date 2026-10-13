#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HUELLA-DRIVER-RW-ZERILLI-1D-LEAPFROG-V3-20261013
"""
BANCO 1D REGGE-WHEELER / ZERILLI -- DRIVER LEAPFROG EN COORDENADA DE TORTUGA
============================================================================

HUELLA-DRIVER-RW-ZERILLI-1D-LEAPFROG-V3-20261013

UNIVERSO DECLARADO : este archivo (1 pieza) + sim/PREREGISTRO_RW_ZERILLI_20261013.md (1 pieza).
MOTOR              : numpy 2.4.6 + scipy 1.17.1 (CubicSpline, least_squares). Sin red,
                     sin aleatoriedad, sin estado oculto: mismo argv => mismo crudo.
UNIDAD             : linea / nodo / paso temporal / encabezado.
VENTANA            : reloj UTC impreso en la cabecera del crudo.

Ecuacion maestra (Klein-Gordon escalar, dispersiva por V; SIN ligadura que preservar):

    d2_t Psi = d2_{r*} Psi - V(r) Psi ,      r* = r + 2M ln(r/2M - 1)

Potenciales sellados (l dado, lambda = (l-1)(l+2)/2):

    V_RW = (1 - 2M/r) [ l(l+1)/r^2 - 6M/r^3 ]
    V_Z  = (1 - 2M/r) [ 2 lam^2 (lam+1) r^3 + 6 lam^2 M r^2 + 18 lam M^2 r + 18 M^3 ]
                       / [ r^3 (lam r + 3M)^2 ]

Esquema: leapfrog escalonado (campo en tiempos enteros n, velocidad en n+1/2).
Fase V2 (D-A): bucle ARRASTRAR-LUEGO-PATEAR; la entrada vhalf es v^{+1/2}.
CFL sellado: dt/dr* = 0.50.
Nulo N-RW-0 (V2, D-B/D-C): capa esponja FORZADA OFF y certificacion F1 a CFL = 1.00
(nodo-exacto); la corrida a CFL = 0.50 NO certifica F1 (dominio del umbral, declarado).
Tres mallas NO anidadas: Delta_k = Delta_0 / 2^k, offset delta_k.
Absorbentes: capa esponja de perfil CUBICO (p = 3, C^2 en la interfaz) + condicion
de radiacion de primer orden (Mur-1) en el nodo extremo, con la DIRECCION invertida entre
el extremo del infinito espacial y el extremo del horizonte (sellado 3, se mide en F4).
Fase V3 (D-E/D-F, orden del dueno): (i) perfil de esponja sen^2 (C^1) -> cubico (C^2),
sigma = sigmax*(x/L)^3 con x = distancia a la INTERFAZ y sigma(0)=sigma'(0)=sigma''(0)=0
=> se elimina el salto de impedancia del borde interior (que reflejaba a -21.68 dB);
(ii) monitor izquierdo de F4 movido de r* = -30 (dentro de la capa [-40,-28]) a r* = -26
(fuera), para medir A_inc intacta (V2 daba 0.7317). Mur-1 pura ya daba -90.66 dB: la
frontera exterior era impecable; V3 empareja la impedancia de la capa disipativa.

Cortes de fallo sellados (F1..F7) -- ver sim/PREREGISTRO_RW_ZERILLI_20261013.md seccion 7.
"""

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import least_squares

HUELLA = "HUELLA-DRIVER-RW-ZERILLI-1D-LEAPFROG-V3-20261013"

# Referencia EXTERNA citada (Leaver). No se autogenera; su acuerdo no se usa como prueba.
LEAVER_MWR = 0.37367
LEAVER_MWI = -0.08896          # M*omega = M*wR - i*M*gamma  =>  M*gamma = 0.08896

CFL_SELLADO = 0.50
EPS = 2.220446049250313e-16
UMBRAL_F1 = 1.0e-12
UMBRAL_F2 = 0.15
UMBRAL_F3 = 100.0 * EPS        # 2.220446049250313e-14
UMBRAL_F4_DB = -40.0
UMBRAL_F5 = 1.0e-2
UMBRAL_F7 = 5.0e-2


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- #
# Potenciales sellados
# --------------------------------------------------------------------------- #
def V_rw(r, M, l):
    return (1.0 - 2.0 * M / r) * (l * (l + 1) / r ** 2 - 6.0 * M / r ** 3)


def V_zerilli(r, M, l):
    lam = 0.5 * (l - 1.0) * (l + 2.0)
    num = (2.0 * lam ** 2 * (lam + 1.0) * r ** 3
           + 6.0 * lam ** 2 * M * r ** 2
           + 18.0 * lam * M ** 2 * r
           + 18.0 * M ** 3)
    den = r ** 3 * (lam * r + 3.0 * M) ** 2
    return (1.0 - 2.0 * M / r) * num / den


def V_of(kind, r, M, l):
    if kind == "rw":
        return V_rw(r, M, l)
    if kind == "zerilli":
        return V_zerilli(r, M, l)
    if kind == "nulo":
        return np.zeros_like(np.asarray(r, dtype=float))
    raise ValueError("potencial desconocido: %r" % kind)


# --------------------------------------------------------------------------- #
# Tortuga: r(r*) por biseccion vectorizada (misma semilla => mismo resultado)
# --------------------------------------------------------------------------- #
def r_of_rstar(rs, M, iters=100):
    rs = np.asarray(rs, dtype=float)
    if M == 0.0:
        return rs.copy()
    lo = np.full(rs.shape, 2.0 * M * (1.0 + 1e-13))
    hi = np.maximum(rs, 4.0 * M) + 60.0 * M
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        f = mid + 2.0 * M * np.log(mid / (2.0 * M) - 1.0) - rs
        neg = f < 0.0
        lo = np.where(neg, mid, lo)
        hi = np.where(neg, hi, mid)
    return 0.5 * (lo + hi)


def rstar_of_r(r, M):
    return r + 2.0 * M * np.log(r / (2.0 * M) - 1.0)


# --------------------------------------------------------------------------- #
# Mallas no anidadas
# --------------------------------------------------------------------------- #
def build_mesh(rsmin, rsmax, d0, k, offset_mode):
    """offset_mode='literal'  -> delta_k = k*Delta_k/3   (formula sellada, literal)
       offset_mode='no-anidado'-> delta_k = k*Delta_0/3  (lectura que satisface F6)"""
    h = d0 / (2.0 ** k)
    if offset_mode == "literal":
        delta = k * h / 3.0
    elif offset_mode == "no-anidado":
        delta = k * d0 / 3.0
    else:
        raise ValueError(offset_mode)
    n = int(math.floor((rsmax - rsmin - delta) / h)) + 1
    rs = rsmin + delta + h * np.arange(n)
    return rs, h, delta


def shared_nodes(node_sets, tol=1e-9):
    """Conteo de nodos compartidos por pares (F6), medido EN POSICION ABSOLUTA.

    Se busca el nodo fino mas cercano a cada nodo grueso y se mide el residuo POSICIONAL:
        q  = round((a_i - b_0)/h_b) ;  resid = |a_i - (b_0 + q*h_b)|
    El residuo NO acumula error de razon (a diferencia de (i*ha/hb - D), que acumula
    ~5.7e-13 por paso y produce un conteo que depende de la TOLERANCIA, no de la geometria).
    Se imprime el residuo minimo de los NO emparejados: si es O(h/2), la separacion
    entre 'coincide' (O(1e-13)) y 'no coincide' es de seis ordenes.
    """
    out = []
    for i in range(len(node_sets)):
        for j in range(i + 1, len(node_sets)):
            a, b = node_sets[i], node_sets[j]
            ha = float(a[1] - a[0])
            hb = float(b[1] - b[0])
            q = np.round((a - b[0]) / hb)
            qc = np.clip(q, 0, b.size - 1)
            resid = np.abs(a - (b[0] + qc * hb))
            inb = (q >= -0.5) & (q <= b.size - 0.5)
            mask = (resid <= tol) & inb
            nm = inb & (~mask)
            out.append({"par": [i, j], "ha": ha, "hb": hb, "ha_sobre_hb": ha / hb,
                        "compartidos": int(mask.sum()),
                        "resid_max_emparejados": (float(resid[mask].max()) if mask.any() else None),
                        "resid_min_no_emparejados": (float(resid[nm].min()) if nm.any() else None),
                        "tol": tol})
    return out


# --------------------------------------------------------------------------- #
# Stencil de interpolacion cubica (Lagrange, 4 nodos) en un punto fisico fijo
# --------------------------------------------------------------------------- #
def cubic_stencil(rs, x0):
    j = int(np.searchsorted(rs, x0) - 1)
    j = max(0, min(j, rs.size - 4))
    idx = np.arange(j, j + 4)
    x = rs[idx]
    w = np.ones(4)
    for a in range(4):
        for b in range(4):
            if a != b:
                w[a] *= (x0 - x[b]) / (x[a] - x[b])
    return idx, w


# --------------------------------------------------------------------------- #
# Capa esponja + Mur-1
# --------------------------------------------------------------------------- #
def sponge_sigma(rs, L, Amax, sigmax):
    """V3 (D-E), PASADA 2: perfil polinomico CUBICO (p = 3), simetrico en ambos extremos.

       sigma = sigmax * (d / L)^3,   d = PROFUNDIDAD dentro de la capa medida desde su
                                     INTERFAZ (el borde interior, contacto con el dominio
                                     fisico): d = 0 en la INTERFAZ, d = L en el nodo EXTREMO.

       Propiedades selladas en la interfaz (d = 0):
           sigma(0) = 0 · sigma'(0) = 0 · sigma''(0) = 0   =>  C^2
       => NO hay salto de impedancia en el punto de contacto. LA ORIENTACION IMPORTA: la
          rampa debe anularse en la INTERFAZ (donde vive el dominio fisico) y crecer hacia
          el EXTREMO (donde ademas actua Mur-1 y el frente ya no vuelve). La pasada 1 la
          tenia invertida (sigma maxima en la interfaz) y la cazo la sonda estructural:
          ver /tmp/f4v3/pasada1_rampa_invertida.txt (blob e2d51ee4, sin corrida de fisica).
          V2 (sen^2) ya anulaba sigma y sigma' en la interfaz, pero dejaba sigma'' != 0;
          V3 cierra el termino cubico.
       sigma = sigmax en el nodo EXTREMO (d = L); sigma = 0 en todo el dominio fisico.
       Atenuacion de un cruce: int_0^L sigma dd = sigmax * L / 4."""
    dl = np.clip((rs[0] + L) - rs, 0.0, L)      # profundidad desde la interfaz IZQUIERDA
    dr = np.clip(rs - (rs[-1] - L), 0.0, L)     # profundidad desde la interfaz DERECHA
    sl = np.where(rs < rs[0] + L, sigmax * (dl / L) ** 3, 0.0)
    sr = np.where(rs > rs[-1] - L, sigmax * (dr / L) ** 3, 0.0)
    return sl + sr


def laplaciano(psi, h, V):
    d2 = np.empty_like(psi)
    d2[1:-1] = (psi[2:] - 2.0 * psi[1:-1] + psi[:-2]) / (h * h)
    d2[0] = d2[1]
    d2[-1] = d2[-2]
    return d2 - V * psi


def solve(rs, h, cfl, V, psi0, vhalf, tmax, sponge_L, sponge_A, obs_x, diag=None):
    """Leapfrog escalonado + capa esponja + condicion de radiacion de primer orden (Mur-1).

    Mur-1 lleva la DIRECCION INVERTIDA entre extremos (sellado 3):
      extremo del infinito espacial (r* -> +inf): absorbe el frente SALIENTE (derechante)
      extremo del horizonte       (r* -> -inf): absorbe el frente ENTRANTE (izquierdante)

    V2 (D-A): la entrada `vhalf` ES v^{+1/2}; el bucle arrastra-luego-patea.
    """
    dt = cfl * h
    nsteps = int(round(tmax / dt))
    sigmax = 2.0 * sponge_A / sponge_L
    sigma = sponge_sigma(rs, sponge_L, sponge_A, sigmax)
    alpha = 0.5 * sigma * dt
    mur = (cfl - 1.0) / (cfl + 1.0)

    if obs_x is None:
        oidx = wobs = None
        obs = None
    else:
        oidx, wobs = cubic_stencil(rs, obs_x)
        obs = np.empty(nsteps + 1)

    psi = psi0.copy()
    v = vhalf.copy()
    if obs is not None:
        obs[0] = float(wobs @ psi[oidx])
    if diag is not None:
        diag(0, 0.0, psi)

    estable = True
    # V2 (D-A): ARRASTRAR-LUEGO-PATEAR. La entrada `vhalf` es v^{+1/2} (convencion del
    # llamante: 0.5*dt*laplaciano para d_t Psi(x,0) = 0). Orden del paso:
    #   drift:  Psi^n     -> Psi^{n+1}    con v^{n+1/2}
    #   kick:   v^{n+1/2} -> v^{n+3/2}    con lap(Psi^{n+1})
    # => Psi^1 = Psi^0 + 1/2 dt^2 lap(Psi^0).
    # La version V1 pateaba PRIMERO y consumia la entrada como v^{-1/2}, ejecutando
    #    Psi^1 = Psi^0 + 3/2 dt^2 lap(Psi^0)  (error de fase medido; ver D-A).
    for step in range(1, nsteps + 1):
        psi_old = psi
        psi = psi + dt * v
        psi[-1] = psi_old[-2] + mur * (psi[-2] - psi_old[-1])
        psi[0] = psi_old[1] + mur * (psi[1] - psi_old[0])
        lap = laplaciano(psi, h, V)
        v = ((1.0 - alpha) * v + dt * lap) / (1.0 + alpha)
        v[0] = (psi[0] - psi_old[0]) / dt
        v[-1] = (psi[-1] - psi_old[-1]) / dt
        if obs is not None:
            obs[step] = float(wobs @ psi[oidx])
        if diag is not None:
            diag(step, step * dt, psi)
        if step % 200 == 0 and not np.all(np.isfinite(psi)):
            estable = False
            break
    ts = dt * np.arange(nsteps + 1)
    return {
        "t": ts, "psi_obs": obs, "psi_final": psi, "nsteps": nsteps,
        "dt": dt, "h": h, "cfl": cfl,
        "estable": bool(estable and np.all(np.isfinite(psi))),
        "sigma_max": float(sigmax), "sigma_max_dt": float(sigmax * dt),
    }


def gauss(x, xc, sig):
    return np.exp(-0.5 * ((x - xc) / sig) ** 2)


# --------------------------------------------------------------------------- #
# Funcional sellado (seccion 6): amplitud sobre 8 instantes fisicos fijos
# --------------------------------------------------------------------------- #
def amp_functional(ts, psi_obs, t8, wR, g):
    sp = CubicSpline(ts, psi_obs)
    y8 = sp(t8)
    E = np.exp(-g * t8)
    A = np.column_stack([E * np.cos(wR * t8), E * np.sin(wR * t8)])
    coef, *_ = np.linalg.lstsq(A, y8, rcond=None)
    return float(math.hypot(coef[0], coef[1])), y8


def fit_qnm(ts, psi_obs, t1, t2, wR0, g0):
    m = (ts >= t1) & (ts <= t2)
    tt, yy = ts[m], psi_obs[m]

    def model(p):
        a, b, wR, g, c = p
        return np.exp(-g * tt) * (a * np.cos(wR * tt) + b * np.sin(wR * tt)) + c

    p0 = [float(np.max(np.abs(yy))), 0.0, wR0, g0, 0.0]
    try:
        res = least_squares(lambda p: model(p) - yy, p0, method="lm", max_nfev=40000)
        a, b, wR, g, c = res.x
        rms = float(np.sqrt(np.mean(res.fun ** 2)))
        amp = float(math.hypot(a, b))
        return {
            "M_wR": float(wR * M_GLOBAL), "M_gamma": float(g * M_GLOBAL),
            "amp": amp, "offset": float(c), "rms": rms,
            "nsamples": int(tt.size), "ok": bool(np.isfinite(res.x).all()),
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "err": repr(exc)}


M_GLOBAL = 1.0


def richardson(A0, A1, A2):
    """Sellado seccion 6: p = log2((A_0 - A_1)/(A_1 - A_2)); F3 si |A_0 - A_1| < 100 eps max|A|."""
    d1, d2 = A0 - A1, A1 - A2
    escala = max(abs(A0), abs(A1), abs(A2))
    if abs(d1) < UMBRAL_F3 * escala:
        return None, d1, d2, "F3: senal por debajo del piso de redondeo (ORDEN NO MEDIBLE)"
    if d2 == 0.0:
        return None, d1, d2, "d2 == 0 (ORDEN NO MEDIBLE)"
    ratio = d1 / d2
    if ratio <= 0.0:
        return None, d1, d2, "cociente no positivo (ORDEN NO MEDIBLE)"
    return math.log2(ratio), d1, d2, "OK"


# --------------------------------------------------------------------------- #
# Suite N-RW-0 : nulo d'Alembert
# --------------------------------------------------------------------------- #
def suite_nulo(args):
    """N-RW-0: V identicamente 0 y M = 0 => la exacta es la onda de d'Alembert (dos frentes).
    Se mide el error L2 relativo en el dominio interior (8 celdas de borde excluidas por lado)
    y se descarta el transitorio inicial.

    V2 (D-B): la capa esponja se FUERZA OFF en el nulo (sponge_L, sponge_A = 1.0, 0.0):
    d'Alembert vale en R LIBRE, sin fronteras y sin disipacion. Con la esponja activa no se
    mide el propagador sino la absorcion (el borde izquierdo esta a 28 unidades de la fuente
    y contamina desde t ~ 28).

    V2 (D-C): la CERTIFICACION de F1 (err_rel_max <= 1e-12) corre a CFL = 1.00, donde el
    esquema de 3 puntos es NODO-EXACTO para d'Alembert. El regimen sellado CFL = 0.50 arrastra
    su error de truncamiento O(dt^2) (~1e-4) y NO certifica F1: queda declarado aqui como
    dominio del umbral y se audita por orden de convergencia (p=2) en --modo mallas.
    El veredicto F1 se calcula SOLO sobre las filas certificantes (CFL = 1.00)."""
    sponge_L, sponge_A = 1.0, 0.0          # D-B: esponja OFF forzada en el nulo
    out = {"UMBRAL_F1": UMBRAL_F1,
           "ventana_interior": "8 celdas de borde excluidas por lado",
           "esponja": "OFF (forzada en el nulo; d'Alembert vale en R libre)",
           "cfl_certificante": 1.0,
           "tlo": args.nulo_tlo, "tmax": args.nulo_tmax}
    for cfl in (1.0, CFL_SELLADO):
        certifica = (cfl == 1.0)
        for arranque in ("auto", "exacto"):
            filas = []
            for k in (0, 1, 2):
                rs, h, delta = build_mesh(args.rsmin, args.rsmax, args.delta0, k, args.offset)
                dt = cfl * h
                psi0 = gauss(rs, args.xc, args.sigma)
                V = np.zeros_like(rs)
                if arranque == "exacto":
                    u1 = 0.5 * (gauss(rs - dt, args.xc, args.sigma)
                                + gauss(rs + dt, args.xc, args.sigma))
                    vhalf = (u1 - psi0) / dt
                else:
                    vhalf = 0.5 * dt * laplaciano(psi0, h, V)
                inter = slice(8, rs.size - 8)
                est = {"err_max": 0.0, "t_max": None, "err_fin": None, "t_fin": None}

                def diag(step, t, psi, _rs=rs, _inter=inter, _e=est, _tlo=args.nulo_tlo):
                    if t < _tlo:
                        return
                    ue = 0.5 * (gauss(_rs - t, args.xc, args.sigma)
                                + gauss(_rs + t, args.xc, args.sigma))
                    num = psi[_inter] - ue[_inter]
                    den = ue[_inter]
                    e = float(np.linalg.norm(num) / max(np.linalg.norm(den), 1e-300))
                    if e > _e["err_max"]:
                        _e["err_max"], _e["t_max"] = e, t
                    _e["err_fin"], _e["t_fin"] = e, t

                g = solve(rs, h, cfl, V, psi0, vhalf, args.nulo_tmax,
                          sponge_L, sponge_A, None, diag=diag)
                filas.append({"k": k, "h": h, "delta": delta, "dt": dt,
                              "nsteps": g["nsteps"], "N": int(rs.size),
                              "err_rel_max": est["err_max"], "t_del_max": est["t_max"],
                              "err_final": est["err_fin"],
                              "estable": g["estable"],
                              "certifica_F1": certifica,
                              "toca_F1": bool(est["err_max"] > UMBRAL_F1)})
            out["cfl_%.2f_arranque_%s" % (cfl, arranque)] = filas
    # V2 (D-C): veredicto F1 SOLO sobre las filas certificantes (CFL = 1.00)
    cert = [r for kk, vv in out.items() if kk.startswith("cfl_") and isinstance(vv, list)
            for r in vv if r.get("certifica_F1")]
    out["veredicto_F1"] = ("PASA" if cert and all(r["err_rel_max"] <= UMBRAL_F1 for r in cert)
                           else "FALLA")
    out["filas_certificantes"] = len(cert)
    return out


# --------------------------------------------------------------------------- #
# Suite F4 : reflexion de la frontera (dB)
# --------------------------------------------------------------------------- #
def suite_frontera(args):
    out = {}
    for lado in ("derecha", "izquierda"):
        k = 0
        rs, h, delta = build_mesh(args.rsmin, args.rsmax, args.delta0, k, args.offset)
        dt = CFL_SELLADO * h
        V = np.zeros_like(rs)
        if lado == "derecha":
            # frente que viaja a +r*: Psi = f(x - t)  =>  d_t Psi(0) = -f'(x)
            xc, mon = 100.0, 120.0
            t_inc = mon - xc
            t_ref = (rs[-1] - xc) + (rs[-1] - mon)
            v0 = -(-(rs - xc) / (args.sigma_f ** 2) * gauss(rs, xc, args.sigma_f))
        else:
            # frente que viaja a -r* (hacia el horizonte): Psi = f(x + t) => d_t Psi(0) = +f'(x)
            # V3 (D-F): monitor FUERA de la capa esponja [-40,-28] => r* = -26 (V2 usaba -30,
            # dentro de la capa, y medía una incidente ya atenuada: A_inc = 0.7317).
            xc, mon = -20.0, -26.0
            t_inc = xc - mon
            t_ref = (xc - rs[0]) + (mon - rs[0])
            v0 = (-(rs - xc) / (args.sigma_f ** 2) * gauss(rs, xc, args.sigma_f))
        psi0 = gauss(rs, xc, args.sigma_f)
        vhalf = v0 + 0.5 * dt * laplaciano(psi0, h, V)
        g = solve(rs, h, CFL_SELLADO, V, psi0, vhalf, max(t_ref + 30.0, 120.0),
                  args.sponge_L, args.sponge_A, mon)
        ts, y = g["t"], g["psi_obs"]
        w = 3.5 * args.sigma_f
        mi = (ts > t_inc - w) & (ts < t_inc + w)
        mr = (ts > t_ref - w) & (ts < t_ref + w)
        ai = float(np.max(np.abs(y[mi]))) if mi.any() else 0.0
        ar = float(np.max(np.abs(y[mr]))) if mr.any() else 0.0
        ratio = ar / ai if ai > 0 else float("inf")
        out[lado] = {"x_frontera": float(rs[-1] if lado == "derecha" else rs[0]),
                     "x_monitor": mon, "x_fuente": xc,
                     "t_incidente": t_inc, "t_reflejado": t_ref,
                     "A_incidente": ai, "A_reflejado": ar,
                     "coef_amplitud": ratio,
                     "dB": (20.0 * math.log10(ratio) if ratio > 0 else -999.0),
                     "toca_F4": bool(not (ratio > 0 and 20.0 * math.log10(ratio) <= UMBRAL_F4_DB)),
                     "estable": g["estable"]}
    return out


# --------------------------------------------------------------------------- #
# Suite F6 : nodos compartidos
# --------------------------------------------------------------------------- #
def suite_mallas(args):
    out = {}
    for modo in ("literal", "no-anidado"):
        sets, deltas = [], []
        for k in (0, 1, 2):
            rs, h, delta = build_mesh(args.rsmin, args.rsmax, args.delta0, k, modo)
            sets.append(rs)
            deltas.append(delta)
        out[modo] = {"deltas": deltas, "nodos": [int(s.size) for s in sets],
                     "compartidos": shared_nodes(sets)}
    return out


# --------------------------------------------------------------------------- #
# Suite fisica : Richardson + isospectralidad + Leaver
# --------------------------------------------------------------------------- #
def suite_fisica(args):
    wR0, g0 = LEAVER_MWR / args.M, abs(LEAVER_MWI) / args.M
    t8 = np.linspace(args.t8a, args.t8b, 8)
    out = {}
    for pot in ("rw", "zerilli"):
        filas = []
        for k in (0, 1, 2):
            rs, h, delta = build_mesh(args.rsmin, args.rsmax, args.delta0, k, args.offset)
            dt = args.cfl * h
            r = r_of_rstar(rs, args.M)
            V = V_of(pot, r, args.M, args.l)
            psi0 = gauss(rs, args.xc, args.sigma)
            vhalf = 0.5 * dt * laplaciano(psi0, h, V)
            g = solve(rs, h, args.cfl, V, psi0, vhalf, args.tmax,
                      args.sponge_L, args.sponge_A, args.robs)
            A, y8 = amp_functional(g["t"], g["psi_obs"], t8, wR0, g0)
            fit = fit_qnm(g["t"], g["psi_obs"], args.t1, args.t2, wR0, g0)
            pico = float(np.max(np.abs(g["psi_obs"])))
            filas.append({"k": k, "h": h, "delta": delta, "dt": dt,
                          "N": int(rs.size), "nsteps": g["nsteps"],
                          "V_max": float(np.max(V)), "A": A, "y8": y8.tolist(),
                          "pico_obs": pico, "fit": fit, "estable": g["estable"]})
        p, d1, d2, nota = richardson(filas[0]["A"], filas[1]["A"], filas[2]["A"])
        out[pot] = {"filas": filas, "p_richardson": p, "d1": d1, "d2": d2, "nota_p": nota}
    # isospectralidad (F5) sobre la malla fina (k=2)
    fRW = out["rw"]["filas"][2]["fit"]
    fZ = out["zerilli"]["filas"][2]["fit"]
    if fRW.get("ok") and fZ.get("ok"):
        wRW = complex(fRW["M_wR"], -fRW["M_gamma"])
        wZ = complex(fZ["M_wR"], -fZ["M_gamma"])
        out["isospectralidad"] = {"M_w_RW": [wRW.real, wRW.imag],
                                  "M_w_Z": [wZ.real, wZ.imag],
                                  "desv_rel": abs(wRW - wZ) / abs(wRW)}
    else:
        out["isospectralidad"] = {"ok": False}
    # Leaver (F7) sobre RW malla fina
    if fRW.get("ok"):
        wmed = complex(fRW["M_wR"], -fRW["M_gamma"])
        wref = complex(LEAVER_MWR, LEAVER_MWI)
        out["leaver"] = {"M_w_medido": [wmed.real, wmed.imag],
                         "M_w_leaver": [wref.real, wref.imag],
                         "desv_rel": abs(wmed - wref) / abs(wref)}
    else:
        out["leaver"] = {"ok": False}
    return out


# --------------------------------------------------------------------------- #
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob(path):
    try:
        return subprocess.run(["git", "hash-object", path], cwd=os.path.dirname(path),
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Banco 1D RW/Zerilli -- driver leapfrog")
    ap.add_argument("--modo", default="todo",
                    choices=["todo", "nulo", "frontera", "mallas", "fisica"])
    ap.add_argument("--potencial", default="rw", choices=["rw", "zerilli", "nulo"])
    ap.add_argument("--l", type=int, default=2)
    ap.add_argument("--M", type=float, default=1.0)
    ap.add_argument("--delta0", type=float, default=0.05)
    ap.add_argument("--cfl", type=float, default=CFL_SELLADO)
    ap.add_argument("--rsmin", type=float, default=-40.0)
    ap.add_argument("--rsmax", type=float, default=150.0)
    ap.add_argument("--tmax", type=float, default=100.0)
    ap.add_argument("--xc", type=float, default=0.0)
    ap.add_argument("--sigma", type=float, default=3.0)
    ap.add_argument("--sigma-f", type=float, default=2.0)
    ap.add_argument("--robs", type=float, default=40.0)
    ap.add_argument("--t1", type=float, default=48.0)
    ap.add_argument("--t2", type=float, default=92.0)
    ap.add_argument("--t8a", type=float, default=55.0)
    ap.add_argument("--t8b", type=float, default=90.0)
    ap.add_argument("--nulo-tmax", type=float, default=38.0)
    ap.add_argument("--nulo-tlo", type=float, default=5.0)
    ap.add_argument("--sponge-L", type=float, default=12.0)
    ap.add_argument("--sponge-A", type=float, default=25.0)
    ap.add_argument("--offset", default="no-anidado", choices=["literal", "no-anidado"])
    ap.add_argument("--outdir", default="sim/data")
    ap.add_argument("--tag", default="base")
    args = ap.parse_args(argv)

    global M_GLOBAL
    M_GLOBAL = args.M

    t0 = time.time()
    self_path = os.path.abspath(__file__)
    cab = {
        "HUELLA": HUELLA,
        "T_UTC": utc_now(),
        "UNIVERSO DECLARADO": "este driver (1 pieza) + pre-registro sellado (1 pieza)",
        "MOTOR": "python3 %s | numpy %s | scipy (CubicSpline, least_squares)"
                 % (sys.version.split()[0], np.__version__),
        "UNIDAD": "nodo / paso temporal / linea / encabezado",
        "argv": vars(args),
        "driver_path": self_path,
        "driver_sha256": sha256_file(self_path),
        "driver_git_blob": git_blob(self_path),
    }
    res = {"cabecera": cab}

    if args.modo in ("todo", "mallas"):
        res["F6_mallas"] = suite_mallas(args)
    if args.modo in ("todo", "nulo"):
        res["N_RW_0_nulo"] = suite_nulo(args)
    if args.modo in ("todo", "frontera"):
        res["F4_frontera"] = suite_frontera(args)
    if args.modo in ("todo", "fisica"):
        res["fisica"] = suite_fisica(args)

    res["cabecera"]["t_utc_fin"] = utc_now()
    res["cabecera"]["wall_s"] = round(time.time() - t0, 2)

    os.makedirs(args.outdir, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = os.path.join(args.outdir, "crudo_rw_zerilli_%s_%s" % (args.tag, stamp))
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
    res["cabecera"]["crudo_json"] = base + ".json"
    print(json.dumps(res, indent=1, ensure_ascii=False))
    print("# CRUDO ESCRITO: %s.json" % base, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
