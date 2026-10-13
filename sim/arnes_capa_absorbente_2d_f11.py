#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ARNES DE LA CAPA ABSORBENTE 2D -- GATE 2D-F11.

Pre-registro: sim/PREREGISTRO_GATE_2D_F11_20261013.md (291 l, 18367 B, sha f4b50bb764f82492f4f0).
Arnes certificado del que se IMPORTA la maquinaria: sim/arnes_richardson_2d_f2_v3.py.

FISICA CONGELADA (no se rebaja; no se hereda de 1D):
  * M = 0.0 estricto; Zerilli APAGADO; coordenadas (r*, theta); CFL sellado = 0.50.
  * Arranque de Cauchy exacto (misma familia que el arnes certificado de F2).
  * Perfil monotonico C^1 gamma(r*) = gamma_max * xi^n, xi = (r* - r*_sponge)/L, n en {2,3}.
  * Cero ESTRUCTURAL en el interior: gamma == 0.0 por mascara exacta (rs >= r*_sponge).
  * Pico M1 ELEGIDO: gamma_max = (n+1)*A/L  =>  integral de gamma = A EXACTA.
  * A, L, gamma_max y n se fijan ANTES de la primera cifra de reflexion.
  * Regla anti-solape (acta 20261013): L_sponge = L_frac * ancho, L_frac = 0.25
    => 2*L = 0.50*ancho < ancho => la guarda C3 queda INACTIVA POR CONSTRUCCION.
  * Prescripcion 1D marcada DIVERGE: no se hereda el exponente -1.3936.

MEDIDOR (declarado antes de la primera cifra):
  * Flujo radial en el anillo testigo r* = p_eff:
        P(t) = - suma_theta (d_t u)(d_r u) r^2 sin(theta) hth   [factor 2*pi suprimido: se mide RAZON]
  * E_sal    = integral de P sobre la ventana de ida      (energia que sale por el anillo).
  * E_vuelta = -integral de P sobre la ventana de vuelta  (energia que regresa por el anillo).
  * E_muerta = |integral de P| sobre la ventana muerta    (debe ser despreciable).
  * R_dB = 10*log10(E_vuelta / E_sal)  EN ENERGIA (la unidad se imprime en cada cifra).
  * Clausula aparte (AMPLITUD): eco prematuro en la banda de testigos rs <= c - 6 sigma,
    ratio < 1e-2 respecto de max|u_inc|.

LO QUE NO CAMBIA (sellado, inmutable): ecuacion escalar con M = 0; operador angular R3
importado del arnes certificado; malla radial UNIFORME (sin delta/offset: el no-anidamiento
era del metro de Richardson, no de esta fisica); arranque de Cauchy; pared Dirichlet
reflexiva en r*_max para el control C1 (SIN Mur-1); umbral R_dB <= -40.0 dB EN ENERGIA.

Los crudos que emite este arnes son SALIDA del instrumento, no escritura manual del agente.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import math
import os
import sys

import numpy as np

_AQUI = os.path.dirname(os.path.abspath(__file__))
if _AQUI not in sys.path:
    sys.path.insert(0, _AQUI)
import arnes_richardson_2d_f2_v3 as f2

# --------------------------------------------------------------------------------------------
# Identidad de la pieza
# --------------------------------------------------------------------------------------------

HUELLA = "HUELLA-ARNES-CAPA-ABSORBENTE-2D-F11-20261013"
HUELLA_PREREGISTRO = "HUELLA-PREREGISTRO-GATE-2D-F11-20261013"
PREREGISTRO = "sim/PREREGISTRO_GATE_2D_F11_20261013.md"
ARNES_V3 = "sim/arnes_richardson_2d_f2_v3.py"
HUELLA_V3 = "HUELLA-ARNES-RICHARDSON-2D-F2-V3-20261013"

# --------------------------------------------------------------------------------------------
# Sellos y umbrales (inmutables)
# --------------------------------------------------------------------------------------------

UMBRAL_R_DB = -40.0                 # EN ENERGIA (pre-registro §D.1)
CFL_SELLADO = 0.50
FAMILIA_N = (2, 3)
N_ELEGIDO = 3
A_EXPLORACION = 25.0                # rung E1
RS_MIN = 2.0
ANCHO = 96.0                        # = 4*L con L_frac = 0.25
L_FRAC = 0.25
SIGMA = 2.0
OMEGA = 1.0
LAMBDA = 2.0 * math.pi / OMEGA
NR0_BASE = 384                      # hr <= min(sigma/8, lambda/10) = 0.25
NT0 = 33
UMBRAL_C2 = 1e-13
UMBRAL_C4 = 1e-3
UMBRAL_C5_DB = 0.5
UMBRAL_C7 = 1e-2
UMBRAL_C1_DB = 1.0
TOL_1D_DB = 3.0
D_1D_MIN = 12.0
D_1D_MAX = 64.0
COEF_1D = 9.8807e-02
EXP_1D = -1.3936

ESCALERA = {
    "E1": {"n": 3, "A": 25.0, "L_frac": 0.25},
    "E2": {"n": 3, "A": 100.0, "L_frac": 0.25},
    "E3": {"n": 3, "A": 400.0, "L_frac": 0.25},
    "E4": {"n": 3, "A": 400.0, "L_frac": 0.30},
}

# --------------------------------------------------------------------------------------------
# Utilidades de identidad
# --------------------------------------------------------------------------------------------


def utc_now():
    return _dt.datetime.now(_dt.timezone.utc)


def stamp_utc():
    return utc_now().strftime("%Y%m%dT%H%M%SZ")


def hora_utc():
    return utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_de(ruta):
    if not os.path.isfile(ruta):
        return None
    h = hashlib.sha256()
    with open(ruta, "rb") as fh:
        for bloque in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def identidad_self():
    ruta = os.path.abspath(__file__)
    txt = open(ruta, "r", encoding="utf-8").read()
    return {
        "ruta": ruta,
        "sha256": sha256_de(ruta),
        "bytes": len(txt.encode("utf-8")),
        "lineas": txt.count("\n"),
        "cabezas": txt.count("\n#"),
        "encabezados": sum(1 for l in txt.splitlines() if l.startswith("#")),
        "huella_en_self": txt.count(HUELLA),
        "huella_verbo": HUELLA,
    }


# --------------------------------------------------------------------------------------------
# Geometria de la capa (unica decision de dimensionado; regla anti-solape)
# --------------------------------------------------------------------------------------------


def geometria(rs_min, ancho, L_frac, n, A):
    L = float(L_frac) * float(ancho)
    solape = 2.0 * L
    if solape >= float(ancho):
        raise SystemExit(
            "C3 FAIL-CLOSED: solape de capa: 2*L = %.15f >= ancho = %.15f "
            "(guarda anti-solape del pre-registro §B.3; no se rebaja el umbral, "
            "se corrige L_frac)" % (solape, float(ancho)))
    rs_max = float(rs_min) + float(ancho)
    rs_sp = rs_max - L
    c = float(rs_min) + L
    p = float(rs_min) + 2.0 * L
    gmax = (float(n) + 1.0) * float(A) / L
    integ = gmax * L / (float(n) + 1.0)
    return {
        "rs_min": float(rs_min), "ancho": float(ancho), "L": L, "L_frac": float(L_frac),
        "n": int(n), "A": float(A), "rs_max": rs_max, "rs_sponge": rs_sp,
        "c": c, "p": p, "gamma_max": gmax, "integral_gamma": integ, "solape": solape,
        "interior_util_frac": (rs_sp - float(rs_min)) / float(ancho),
        "regla_anticolape": "2*L < ancho  =>  C3 INACTIVA POR CONSTRUCCION",
    }


def gamma_de(rs, g):
    """Perfil M1. CERO ESTRUCTURAL en el interior por mascara exacta."""
    x = (rs - g["rs_sponge"]) / g["L"]
    val = g["gamma_max"] * np.power(np.clip(x, 0.0, 1.0), g["n"])
    return np.where(rs >= g["rs_sponge"], val, 0.0)


def damp_de(rs, g, dt):
    """Factor exponencial de amortiguamiento por paso. Exactamente 1.0 en el interior."""
    return np.where(rs >= g["rs_sponge"], np.exp(-2.0 * gamma_de(rs, g) * dt), 1.0)


# --------------------------------------------------------------------------------------------
# Dato: paquete GAUSSIANO SALIENTE PURO en la rama l = 0
# --------------------------------------------------------------------------------------------


def dato_saliente(rs, c, sigma, omega):
    """u^0 = env*cos(omega*(r*-c));  v^0 = -d_r u^0  (onda saliente pura, l = 0, exacta).

    Para la ecuacion de ondas 1D con velocidad 1, u = f(r* - t) implica d_t u = -d_r u.
    env y su derivada se evaluan analiticamente; el soporte util es c +- 6 sigma.
    """
    x = rs - c
    env = np.exp(-(x * x) / (2.0 * sigma * sigma))
    denv = -(x / (sigma * sigma)) * env
    ph = omega * x
    co = np.cos(ph)
    si = np.sin(ph)
    u0 = env * co
    v0 = -(denv * co - omega * env * si)
    return u0, v0


# --------------------------------------------------------------------------------------------
# Integrador amortiguado (EXTENSION, no reemplazo): PATEAR-LUEGO-ARRASTRAR exponencial
# --------------------------------------------------------------------------------------------
#
#   v <- exp(-2 gamma dt) * v + dt * a(u)        (la multiplicacion por 1.0 es EXACTA)
#   u <- u + dt * v
#   u[0,:] = u[-1,:] = 0.0                        (las dos paredes Dirichlet, igual que v3)
#
# Cero estructural: damp == 1.0 bit-exacto en el interior => el nucleo certificado de F2
# se reproduce sin holgura (control C0). Arranque de Cauchy con v^0 != 0:
#   u^{-1} = u^0 - dt*v^0 + 0.5*dt^2*a^0    ;    v^{-1/2} = (u^0 - u^{-1})/dt
# con v^0 == 0 reduce EXACTAMENTE al arranque certificado de F2.


def simula_amortiguado(m, u0, v0, damp, nsteps, dt, orden_r=2, orden_th=2, nulo_ang=False, sonda=None):
    u = np.array(u0, dtype=float, copy=True)
    u[0, :] = 0.0
    u[-1, :] = 0.0
    a0 = f2.acel(m, u, orden_r, orden_th, nulo_ang)
    u_m1 = u - dt * v0 + 0.5 * dt * dt * a0
    u_m1[0, :] = 0.0
    u_m1[-1, :] = 0.0
    v = (u - u_m1) / dt
    for k in range(nsteps):
        v = damp * v + dt * f2.acel(m, u, orden_r, orden_th, nulo_ang)
        u = u + dt * v
        u[0, :] = 0.0
        u[-1, :] = 0.0
        if sonda is not None:
            sonda(k + 1, u, v)
    return u


# --------------------------------------------------------------------------------------------
# Medidor (declarado antes de la primera cifra)
# --------------------------------------------------------------------------------------------


class Medidor:
    """Flujo radial en el anillo r* = p_eff + eco prematuro + simetria angular.

    P(t) = - r_p^2 * hth * suma_theta v[ip,:] * dru[ip,:] * sin(theta)
    (factor 2*pi suprimido: se mide RAZON, no energia absoluta).
    """

    def __init__(self, m, ip, hr, th, hth, filas_testigo, pasos_captura=()):
        self.m = m
        self.ip = int(ip)
        self.hr = float(hr)
        self.sin_th = np.sin(th)
        self.hth = float(hth)
        self.rp2 = float(m.rs[ip]) ** 2
        self.filas_testigo = np.asarray(sorted(set(int(x) for x in filas_testigo)), dtype=int)
        self.pasos_captura = set(int(x) for x in pasos_captura)
        self.capturas = {}
        self.t = []
        self.P = []
        self.eco = []
        self.var_theta = []
        self.amax = 0.0

    def __call__(self, k, u, v):
        ip = self.ip
        dru = (u[ip + 1, :] - u[ip - 1, :]) / (2.0 * self.hr)
        P = -self.rp2 * self.hth * float(np.sum(v[ip, :] * dru * self.sin_th))
        self.t.append(int(k))
        self.P.append(P)
        if self.filas_testigo.size:
            self.eco.append(float(np.max(np.abs(u[self.filas_testigo, :]))))
        else:
            self.eco.append(0.0)
        self.var_theta.append(float(np.max(u.max(axis=1) - u.min(axis=1))))
        am = float(np.max(np.abs(u)))
        if am > self.amax:
            self.amax = am
        if k in self.pasos_captura:
            self.capturas[int(k)] = u.copy()


def acumular(med, dt, t_a, t_b):
    """E_sal en [0, t_a]; E_muerta en (t_a, t_b]; E_vuelta en (t_b, fin]. EN ENERGIA."""
    E_sal = 0.0
    E_muerta = 0.0
    E_vuelta = 0.0
    E_entrante = 0.0
    for k, P in zip(med.t, med.P):
        t = k * dt
        if t <= t_a:
            E_sal += P * dt
            if P < 0.0:
                E_entrante += (-P) * dt
        elif t <= t_b:
            E_muerta += P * dt
        else:
            E_vuelta += (-P) * dt
    return {"E_sal": E_sal, "E_muerta": E_muerta, "E_vuelta": E_vuelta, "E_entrante": E_entrante,
            "dt": dt, "t_a": t_a, "t_b": t_b}


def rdb_de(acc):
    if acc["E_sal"] <= 0.0:
        return None
    if acc["E_vuelta"] <= 0.0:
        return None
    return 10.0 * math.log10(acc["E_vuelta"] / acc["E_sal"])


# --------------------------------------------------------------------------------------------
# Ejecucion
# --------------------------------------------------------------------------------------------


def ejecuta(m, g, dt, nsteps, encender, sigma, omega, filas_testigo, pasos_captura=()):
    ip = int(np.argmin(np.abs(m.rs - g["p"])))
    p_eff = float(m.rs[ip])
    if encender:
        damp = damp_de(m.rs, g, dt)
    else:
        damp = np.ones(m.nr)
    damp = damp[:, None]
    u0_r, v0_r = dato_saliente(m.rs, g["c"], sigma, omega)
    u0 = np.tile(u0_r[:, None], (1, m.nt))
    v0 = np.tile(v0_r[:, None], (1, m.nt))
    med = Medidor(m, ip, m.hr, m.th, m.hth, filas_testigo, pasos_captura)
    u = simula_amortiguado(m, u0, v0, damp, nsteps, dt, 2, 2, False, med)
    return {"u": u, "med": med, "ip": ip, "p_eff": p_eff, "u0": u0, "v0": v0,
            "damp": damp, "nsteps": nsteps, "dt": dt}


# --------------------------------------------------------------------------------------------
# Banco must-fail C0 - C8 (causa impresa + RC, no solo RC)
# --------------------------------------------------------------------------------------------


def control_C0():
    """Reduccion al arnes certificado: gamma == 0 y v^0 == 0 => diff == 0.0 EXACTO."""
    m = f2.Malla2D(RS_MIN, RS_MIN + ANCHO, 96, NT0, CFL_SELLADO, 0)
    dt = m.dt_cota
    nsteps = 40
    dato = lambda mm: f2.dato_reducido(mm, 22.0, 2.0, 0.35)
    u_f2 = f2.simula(m, dato, nsteps, dt, 2, 2, False)
    u0 = f2.dato_reducido(m, 22.0, 2.0, 0.35)
    v0 = np.zeros_like(u0)
    damp = np.ones(m.nr)[:, None]
    u_f11 = simula_amortiguado(m, u0, v0, damp, nsteps, dt, 2, 2, False, None)
    diff = float(np.max(np.abs(u_f11 - u_f2)))
    return {"control": "C0", "que": "reduccion al arnes certificado (gamma==0, v0==0)",
            "esperado": "diff == 0.0 exacto", "diff": diff,
            "ok": bool(diff == 0.0), "rc": 0 if diff == 0.0 else 1,
            "nr0_prueba": 96, "nt0": NT0, "nsteps": nsteps, "dt": dt}


def control_C3(L_frac_provocado=0.55):
    """Guarda anti-solape: 2*L >= ancho => SystemExit con causa C3."""
    try:
        geometria(RS_MIN, ANCHO, L_frac_provocado, N_ELEGIDO, A_EXPLORACION)
    except SystemExit as exc:
        msg = str(exc)
        return {"control": "C3", "que": "guarda de solape (2*L >= ancho)",
                "provocado_con_L_frac": L_frac_provocado,
                "2L_sobre_ancho": 2.0 * L_frac_provocado, "causa": msg,
                "ok": bool("C3 FAIL-CLOSED" in msg), "rc": 0 if "C3 FAIL-CLOSED" in msg else 1}
    return {"control": "C3", "que": "guarda de solape (2*L >= ancho)",
            "provocado_con_L_frac": L_frac_provocado, "causa": "NO SE DISPARO",
            "ok": False, "rc": 1}


def bloque_1d(D_2d, rdb_2d):
    """Comparacion con la ley 1D a IGUAL D. Se imprimen las DOS lecturas y los TRES rotulos:
    no se elige la que conviene (pre-registro §C.4 + §D.2)."""
    out = {"D": D_2d, "regla": "R_t = %.6e * D^(%.4f)" % (COEF_1D, EXP_1D),
           "dominio_validez_D": [D_1D_MIN, D_1D_MAX], "tolerancia_dB": TOL_1D_DB,
           "rdb_2d": rdb_2d, "se_elige": False,
           "nota": "se reporta la bifurcacion energia/amplitud; NO se elige"}
    if not (D_1D_MIN <= D_2d <= D_1D_MAX):
        out["comparable"] = False
        out["lectura_energia_dB"] = None
        out["lectura_amplitud_dB"] = None
        out["rotulo_energia"] = "NO COMPARABLE"
        out["rotulo_amplitud"] = "NO COMPARABLE"
        return out
    R = COEF_1D * (D_2d ** EXP_1D)
    db_en = 10.0 * math.log10(R)
    db_am = 10.0 * math.log10(R * R)
    out["comparable"] = True
    out["R_1d"] = R
    out["lectura_energia_dB"] = db_en
    out["lectura_amplitud_dB"] = db_am
    if rdb_2d is None:
        out["rotulo_energia"] = "NO MEDIBLE"
        out["rotulo_amplitud"] = "NO MEDIBLE"
    else:
        out["rotulo_energia"] = "COINCIDE" if abs(rdb_2d - db_en) <= TOL_1D_DB else "DIVERGE"
        out["rotulo_amplitud"] = "COINCIDE" if abs(rdb_2d - db_am) <= TOL_1D_DB else "DIVERGE"
    return out


def escribir_crudo(crudo, ruta):
    with open(ruta, "w", encoding="utf-8") as fh:
        json.dump(crudo, fh, indent=1, sort_keys=True, ensure_ascii=False)
        fh.write("\n")
    txt = open(ruta, "r", encoding="utf-8").read()
    return {"ruta": ruta, "lineas": txt.count("\n"), "bytes": len(txt.encode("utf-8")),
            "sha256": sha256_de(ruta)}


# --------------------------------------------------------------------------------------------
# Ventanas de transito (calculadas analiticamente; se imprimen antes de la primera cifra)
# --------------------------------------------------------------------------------------------


def ventanas(g, p_eff, sigma, rs_min, rs_max):
    t_1 = p_eff - g["c"]                                  # centro del paquete en el anillo p
    t_a = t_1 + 6.0 * sigma                               # el paquete termina de pasar por p
    t_s = g["rs_sponge"] - g["c"] - 6.0 * sigma           # el frente toca la capa
    t_ret = t_s + (g["rs_sponge"] - p_eff)                # primer retorno posible a p
    t_3 = (g["rs_sponge"] - g["c"]) + (g["rs_sponge"] - p_eff)   # centro reflejado en p
    T_obs = t_3 + 6.0 * sigma
    t_4 = t_3 + (p_eff - rs_min)                          # el reflejo llega a la pared interna
    t_s_max = rs_max - g["c"] - 6.0 * sigma               # el frente toca la pared exterior (C1)
    t_ret_c1 = t_s_max + (rs_max - p_eff)
    T_c1 = t_ret_c1 + 12.0 * sigma
    return {"t_1": t_1, "t_a": t_a, "t_s": t_s, "t_ret": t_ret, "t_3": t_3, "T_obs": T_obs,
            "t_4": t_4, "t_s_max": t_s_max, "t_ret_c1": t_ret_c1, "T_c1": T_c1,
            "ventana_ida": [0.0, t_a], "ventana_muerta": [t_a, t_ret],
            "ventana_vuelta": [t_ret, T_obs], "ventana_vuelta_C1": [t_ret_c1, T_c1]}


# --------------------------------------------------------------------------------------------
# Corrida
# --------------------------------------------------------------------------------------------


def corrida(a, g, nr0, nt0, cfl, sigma, omega, encender=True, capturas=(), t_min=None, dt_fijo=None):
    m = f2.Malla2D(g["rs_min"], g["rs_max"], nr0, nt0, cfl, 0)
    dt = float(dt_fijo) if dt_fijo is not None else float(m.dt_cota)
    ip = int(np.argmin(np.abs(m.rs - g["p"])))
    p_eff = float(m.rs[ip])
    v = ventanas(g, p_eff, sigma, g["rs_min"], g["rs_max"])
    filas_testigo = np.nonzero(m.rs <= g["c"] - 6.0 * sigma)[0]
    T = float(t_min) if t_min is not None else v["T_obs"]
    nsteps = int(math.ceil(T / dt))
    res = ejecuta(m, g, dt, nsteps, encender, sigma, omega, filas_testigo, capturas)
    acc = acumular(res["med"], dt, v["t_a"], v["t_ret"])
    return {"m": m, "nr0": nr0, "nr": m.nr, "nt": m.nt, "hr": m.hr, "hth": m.hth, "dt": dt,
            "nivel": m.nivel, "nsteps": nsteps, "p_eff": p_eff, "ip": ip, "ventanas": v,
            "acc": acc, "rdb": rdb_de(acc), "med": res["med"], "u": res["u"],
            "filas_testigo": filas_testigo, "T": T}


# --------------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(description="Arnes de la capa absorbente 2D -- Gate 2D-F11")
    ap.add_argument("--rung", default="E1", choices=sorted(ESCALERA))
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--A", type=float, default=None)
    ap.add_argument("--L-frac", dest="L_frac", type=float, default=None)
    ap.add_argument("--ancho", type=float, default=ANCHO)
    ap.add_argument("--rs-min", dest="rs_min", type=float, default=RS_MIN)
    ap.add_argument("--sigma", type=float, default=SIGMA)
    ap.add_argument("--omega", type=float, default=OMEGA)
    ap.add_argument("--nr0", type=int, default=NR0_BASE)
    ap.add_argument("--nt0", type=int, default=NT0)
    ap.add_argument("--cfl", type=float, default=CFL_SELLADO)
    ap.add_argument("--ladder", default="384,768,1536")
    ap.add_argument("--solo-control", dest="solo_control", default=None)
    ap.add_argument("--json", dest="json_ruta", default="auto")
    ap.add_argument("--estricto", action="store_true")
    ap.add_argument("--stamp", action="store_true")
    a = ap.parse_args(argv)

    if a.cfl > CFL_SELLADO + 1e-12:
        raise SystemExit("FAIL-CLOSED: CFL = %.10f > sellado %.10f (la cota no se rebaja)"
                         % (a.cfl, CFL_SELLADO))

    ctrl = (a.solo_control or "").upper()
    if ctrl == "C3":
        info = control_C3(0.55)
        print(json.dumps(info, indent=1, sort_keys=True, ensure_ascii=False))
        return 0 if info["ok"] else 1
    if ctrl == "C0":
        info = control_C0()
        print(json.dumps(info, indent=1, sort_keys=True, ensure_ascii=False))
        return 0 if info["ok"] else 1

    base = ESCALERA[a.rung]
    n = int(a.n) if a.n is not None else int(base["n"])
    A = float(a.A) if a.A is not None else float(base["A"])
    L_frac = float(a.L_frac) if a.L_frac is not None else float(base["L_frac"])
    if n not in FAMILIA_N:
        raise SystemExit("FAIL-CLOSED: perfil n = %d fuera de la familia sellada %s"
                         % (n, str(FAMILIA_N)))

    g = geometria(a.rs_min, a.ancho, L_frac, n, A)

    if ctrl == "C5":
        niveles = [int(x) for x in a.ladder.split(",") if x.strip()]
        filas = []
        for nr0 in niveles:
            r = corrida(a, g, nr0, a.nt0, a.cfl, a.sigma, a.omega, True, (), None, None)
            filas.append(r)
        deltas = []
        for i in range(len(filas) - 1):
            if filas[i]["rdb"] is None or filas[i + 1]["rdb"] is None:
                deltas.append(None)
            else:
                deltas.append(abs(filas[i + 1]["rdb"] - filas[i]["rdb"]))
        finos = [d for d in deltas[-2:] if d is not None]
        ok = bool(finos) and max(finos) <= UMBRAL_C5_DB
        info = {"control": "C5", "que": "resolucion de malla (escalera radial)",
                "ladder": niveles, "umbral_dB": UMBRAL_C5_DB,
                "rdb_por_nivel": [f["rdb"] for f in filas],
                "deltas_dB": deltas, "ok": ok, "rc": 0 if ok else 1,
                "si_no_cumple": "NO RESUELTO"}
        print(json.dumps(info, indent=1, sort_keys=True, ensure_ascii=False))
        return 0 if ok else 1

    # -------- corrida principal --------------------------------------------------------------
    m0 = f2.Malla2D(g["rs_min"], g["rs_max"], a.nr0, a.nt0, a.cfl, 0)
    dt0 = float(m0.dt_cota)
    ip0 = int(np.argmin(np.abs(m0.rs - g["p"])))
    p_eff0 = float(m0.rs[ip0])
    vw = ventanas(g, p_eff0, a.sigma, g["rs_min"], g["rs_max"])
    k_c2a = int(math.floor(12.0 / dt0))
    k_c2b = int(math.floor(vw["t_s"] / dt0))

    r_on = corrida(a, g, a.nr0, a.nt0, a.cfl, a.sigma, a.omega, True, (k_c2a, k_c2b),
                   vw["T_obs"], dt0)
    r_off = corrida(a, g, a.nr0, a.nt0, a.cfl, a.sigma, a.omega, False, (k_c2a, k_c2b),
                    vw["T_c1"], dt0)
    u0_ini_r, _ = dato_saliente(np.array([g["c"]]), g["c"], a.sigma, a.omega)
    max_inc = float(np.max(np.abs(u0_ini_r)))
    rdb = r_on["rdb"]

    # -------- controles ----------------------------------------------------------------------
    c0 = control_C0()
    c3 = control_C3(0.55)

    filas_int = np.nonzero(r_on["m"].rs < g["rs_sponge"])[0]
    dif_c2 = []
    for k in (k_c2a, k_c2b):
        ua = r_on["med"].capturas.get(k)
        ub = r_off["med"].capturas.get(k)
        if ua is None or ub is None:
            dif_c2.append(None)
        else:
            dif_c2.append(float(np.max(np.abs(ua[filas_int, :] - ub[filas_int, :]))))
    c2_ok = all(d is not None and d <= UMBRAL_C2 for d in dif_c2)
    c2 = {"control": "C2", "que": "no contaminacion interior (ON vs OFF, mismo dt)",
          "umbral": UMBRAL_C2, "pasos_captura": [k_c2a, k_c2b],
          "t_capturas": [k_c2a * dt0, k_c2b * dt0],
          "residuo_interior": dif_c2, "ok": bool(c2_ok), "rc": 0 if c2_ok else 1,
          "ref": "corrida con la capa APAGADA (A = 0), mismo dt y misma malla"}

    acc_c1 = acumular(r_off["med"], dt0, vw["t_a"], vw["t_ret_c1"])
    rdb_c1 = rdb_de(acc_c1)
    c1_ok = bool(rdb_c1 is not None and abs(rdb_c1) <= UMBRAL_C1_DB)
    c1 = {"control": "C1", "que": "pared reflectante presente y atenuacion NO del esquema espacial",
          "A": 0.0, "pared_dirichlet_en": g["rs_max"], "mur1": False,
          "T_obs_C1": vw["T_c1"], "E_sal": acc_c1["E_sal"], "E_vuelta": acc_c1["E_vuelta"],
          "rdb_C1": rdb_c1, "umbral_dB": UMBRAL_C1_DB, "ok": c1_ok, "rc": 0 if c1_ok else 1,
          "esperado": "|R_dB| <= 1.0 (reflexion total); NO -90.66 dB de Mur-1"}

    ratio_c4 = (r_on["acc"]["E_entrante"] / r_on["acc"]["E_sal"]) if r_on["acc"]["E_sal"] > 0 else None
    c4_ok = bool(ratio_c4 is not None and ratio_c4 <= UMBRAL_C4)
    c4 = {"control": "C4", "que": "dato saliente puro (flujo entrante en la ventana de ida)",
          "E_entrante": r_on["acc"]["E_entrante"], "E_sal": r_on["acc"]["E_sal"],
          "ratio": ratio_c4, "umbral": UMBRAL_C4, "ok": c4_ok, "rc": 0 if c4_ok else 1,
          "si_no_cumple": "NO MEDIBLE"}

    var_max = float(np.max(r_on["med"].var_theta)) if r_on["med"].var_theta else None
    c6_ok = bool(var_max is not None and var_max == 0.0)
    c6 = {"control": "C6", "que": "simetria angular (rama l = 0)",
          "variacion_theta_max": var_max, "ok": c6_ok, "rc": 0 if c6_ok else 1}

    eco_max = float(np.max(r_on["med"].eco)) if r_on["med"].eco else None
    ratio_c7 = (eco_max / max_inc) if (eco_max is not None and max_inc > 0) else None
    c7_ok = bool(ratio_c7 is not None and ratio_c7 < UMBRAL_C7)
    c7 = {"control": "C7", "que": "eco prematuro en la banda de testigos (AMPLITUD)",
          "banda": [g["rs_min"], g["c"] - 6.0 * a.sigma], "eco_max": eco_max,
          "max_inc": max_inc, "ratio": ratio_c7, "umbral": UMBRAL_C7,
          "unidad": "amplitud", "ok": c7_ok, "rc": 0 if c7_ok else 1}

    c8_int = bool(g["c"] - 6.0 * a.sigma >= g["rs_min"] and g["c"] + 6.0 * a.sigma <= g["rs_sponge"])
    c8_p = bool(6.0 * a.sigma <= r_on["p_eff"] - g["rs_min"])
    c8_int2 = bool(g["c"] - 6.0 * a.sigma <= p_eff0 <= g["c"] + 6.0 * a.sigma)
    c8_ok = bool(c8_int and c8_p)
    c8 = {"control": "C8", "que": "contencion interior (fail-closed)",
          "soporte_en_interior": c8_int, "6sigma_le_p_menos_rsmin": c8_p,
          "p_en_soporte": c8_int2, "6sigma": 6.0 * a.sigma,
          "p_efectivo_menos_rs_min": r_on["p_eff"] - g["rs_min"],
          "ok": c8_ok, "rc": 0 if c8_ok else 1}

    banco = [c0, c1, c2, c3, c4, c6, c7, c8]

    # -------- comparacion 1D (par, sin eleccion) ---------------------------------------------
    b1d = bloque_1d(g["A"], rdb)
    dedo_1d = 1.1 * LAMBDA
    dedo = {"D_prescripcion_1D": dedo_1d, "2L_prescripcion_1D": 2.0 * dedo_1d,
            "ancho": g["ancho"], "deficit": 2.0 * dedo_1d - g["ancho"],
            "rotulo": "DIVERGE", "motivo": "2*L_prescripcion_1D > ancho: la prescripcion 1D "
                     "no cabe en el dominio anti-solape; no se hereda el exponente"}
    if D_1D_MIN <= dedo_1d <= D_1D_MAX:
        R1 = COEF_1D * (dedo_1d ** EXP_1D)
        dedo["ley1D_en_D_1.1lambda_dB_energia"] = 10.0 * math.log10(R1)
        dedo["ley1D_en_D_1.1lambda_dB_amplitud"] = 10.0 * math.log10(R1 * R1)

    # -------- veredicto ----------------------------------------------------------------------
    fallos = [c["control"] for c in banco if not c["ok"]]
    medible = rdb is not None
    verde = (len(fallos) == 0) and medible and (rdb <= UMBRAL_R_DB)
    veredicto = "VERDE" if verde else ("NO MEDIBLE" if not medible else "ROJO")
    if fallos:
        veredicto = "ROJO"

    crudo = {
        "huella": HUELLA,
        "hora_utc": hora_utc(),
        "identidad_self": identidad_self(),
        "piezas_citadas": {
            "arnes_v3": ARNES_V3, "huella_v3": HUELLA_V3, "sha256_v3": sha256_de(os.path.join(_AQUI, "arnes_richardson_2d_f2_v3.py")),
            "preregistro": PREREGISTRO, "huella_preregistro": HUELLA_PREREGISTRO,
            "sha256_preregistro": sha256_de(os.path.join(_AQUI, os.path.basename(PREREGISTRO))),
        },
        "argv": list(sys.argv[1:]),
        "universo_declarado": {
            "arnes": os.path.abspath(__file__),
            "fisica": "M = 0.0 estricto, Zerilli APAGADO, (r*, theta), l = 0 radial",
            "importa": "arnes_richardson_2d_f2_v3 (acel, d2r, L2_theta, simula, Malla2D)",
            "no_hereda_1d": "exponente -1.3936 PROHIBIDO (pre-registro §C)",
        },
        "sellos": {"UMBRAL_R_DB": UMBRAL_R_DB, "unidad_umbral": "energia",
                   "CFL_SELLADO": CFL_SELLADO, "familia_n": list(FAMILIA_N),
                   "pico": "M1 gamma_max = (n+1)*A/L", "pared": "Dirichlet reflexiva sin Mur-1",
                   "arranque": "Cauchy exacto (v^0 != 0 soportado)"},
        "escalera": ESCALERA, "rung": a.rung,
        "geometria": g,
        "malla": {"nr0": r_on["nr"], "nt0": r_on["nt"], "hr": r_on["hr"], "hth": r_on["hth"],
                  "dt": r_on["dt"], "nsteps": r_on["nsteps"], "nsteps_off": r_off["nsteps"],
                  "cfl": a.cfl, "dt_cota": dt0, "nivel": r_on["nivel"]},
        "ventanas": vw, "p_efectivo": r_on["p_eff"], "ip": r_on["ip"],
        "medidor": {"P": "-r^2*hth*suma_theta (d_t u)(d_r u) sin(theta) (2*pi suprimido)",
                    "unidad": "energia", "E_sal": r_on["acc"]["E_sal"],
                    "E_vuelta": r_on["acc"]["E_vuelta"], "E_muerta": r_on["acc"]["E_muerta"],
                    "E_entrante": r_on["acc"]["E_entrante"],
                    "ratio_E_vuelta_sobre_E_sal": (r_on["acc"]["E_vuelta"] / r_on["acc"]["E_sal"])
                    if r_on["acc"]["E_sal"] > 0 else None},
        "R_dB": rdb, "R_dB_unidad": "energia", "UMBRAL_R_DB": UMBRAL_R_DB,
        "banco": banco, "fallos": fallos,
        "comparacion_1D": b1d, "prescripcion_1D_1.1lambda": dedo,
        "max_inc": max_inc,
        "veredicto": veredicto,
    }

    print("UNIVERSO DECLARADO: %s" % os.path.abspath(__file__))
    print("HUELLA: %s | hora %s" % (HUELLA, crudo["hora_utc"]))
    print("v3 citado sha256: %s" % (crudo["piezas_citadas"]["sha256_v3"] or "AUSENTE"))
    print("rung %s | n=%d A=%.1f L_frac=%.2f | L=%.6f D=%.6f ancho=%.1f" % (a.rung, g["n"], g["A"], g["L_frac"], g["L"], g["L"], g["ancho"]))
    print("r*: min %.1f sponge %.1f max %.1f | c %.1f p %.3f | gmax %.15f int_gamma %.15f"
          % (g["rs_min"], g["rs_sponge"], g["rs_max"], g["c"], r_on["p_eff"], g["gamma_max"], g["integral_gamma"]))
    print("regla anti-solape: 2L/ancho = %.6f < 1  => C3 INACTIVA POR CONSTRUCCION" % (2.0 * g["L"] / g["ancho"]))
    print("malla nr0=%d nt0=%d hr=%.15f hth=%.15f dt=%.15f nsteps=%d" % (r_on["nr"], r_on["nt"], r_on["hr"], r_on["hth"], r_on["dt"], r_on["nsteps"]))
    print("ventanas: ida [0,%.1f] muerta [%.1f,%.1f] vuelta [%.1f,%.1f] | T_obs=%.1f t4=%.1f"
          % (vw["t_a"], vw["t_a"], vw["t_ret"], vw["t_ret"], vw["T_obs"], vw["T_obs"], vw["t_4"]))
    print("medidor EN ENERGIA: E_sal=%.15e E_vuelta=%.15e ratio=%.15e"
          % (r_on["acc"]["E_sal"], r_on["acc"]["E_vuelta"], crudo["medidor"]["ratio_E_vuelta_sobre_E_sal"] or float('nan')))
    print("R_dB = %.6f dB (energia) | umbral %.1f" % (rdb if rdb is not None else float('nan'), UMBRAL_R_DB))
    for c in banco:
        print("  %-3s %-4s rc=%d  %s" % (c["control"], "OK" if c["ok"] else "ROJO", c["rc"], c["que"]))
    print("C5 no corrido: control independiente (--solo-control C5 --ladder %s)" % a.ladder)
    print("1D @ D=%.1f: ley R_t = %.6e*D^(%.4f)" % (g["A"], COEF_1D, EXP_1D))
    if b1d["comparable"]:
        print("   lectura energia  = %.6f dB  -> %s" % (b1d["lectura_energia_dB"], b1d["rotulo_energia"]))
        print("   lectura amplitud = %.6f dB  -> %s" % (b1d["lectura_amplitud_dB"], b1d["rotulo_amplitud"]))
    else:
        print("   NO COMPARABLE (D fuera de [%.1f, %.1f])" % (D_1D_MIN, D_1D_MAX))
    print("prescripcion 1D D=1.1lambda=%.15f => 2L=%.15f > ancho=%.1f (deficit %.15f) => MARCADA DIVERGE"
          % (dedo_1d, 2.0 * dedo_1d, g["ancho"], 2.0 * dedo_1d - g["ancho"]))
    print("VEREDICTO: %s" % veredicto)

    if a.json_ruta == "auto":
        ruta = os.path.join(_AQUI, "data", "crudo_2d_f11_%s_nr0_%d_%s.json"
                            % (a.rung, a.nr0, stamp_utc()))
    else:
        ruta = a.json_ruta
    os.makedirs(os.path.dirname(os.path.abspath(ruta)), exist_ok=True)
    meta = escribir_crudo(crudo, ruta)
    print("CRUDO: %s | %d l | %d B | sha256:%s"
          % (meta["ruta"], meta["lineas"], meta["bytes"], meta["sha256"]))

    if a.estricto and veredicto != "VERDE":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
