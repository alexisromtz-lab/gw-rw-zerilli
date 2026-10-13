#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HUELLA-ARNES-RICHARDSON-2D-F2-20261013
"""
ARNES INDEPENDIENTE -- GATE 2D-F2: AUTOCONVERGENCIA DE RICHARDSON EN 2D AXISIMETRICO
====================================================================================

HUELLA-ARNES-RICHARDSON-2D-F2-20261013

UNIVERSO DECLARADO : este archivo (1 pieza) + sim/PREREGISTRO_RICHARDSON_2D_F2_20261013.md
                     (1 pieza, blob c91d8447, commit NO ordenado: SIN RASTREAR) + sim/PREREGISTRO_FRENTE_2D_CQG_20261013.md
                     (1 pieza, blob 2b2dd0fa, commit 2eebc3b) + sim/ADENDA_1_RATIFICACION_SECCION_4_Y_ESQUEMA_2D_RATIFICADO_20261013.md
                     (1 pieza, blob 94aa523d, commit 90759a8). Total 4 piezas.
MOTOR              : numpy (sin scipy, sin red, sin aleatoriedad, sin estado oculto): el mismo argv produce
                     el mismo crudo. El .git del arbol queda FUERA del universo contado.
UNIDAD             : nodo / celda / paso temporal / linea / encabezado.
VENTANA            : reloj UTC impreso en la cabecera.

HUELLA vs DRIVER: este arnes NO importa, NO copia y NO toca sim/driver_rw_zerilli_2d.py (581 l, ajeno, SIN
RASTREAR). Un instrumento que se mide a si mismo es x == x (acta de ratificacion §4). El operador angular y
la cota R2 estan REESCRITOS aqui desde la letra ratificada (R2/R3), no importados.

Ecuacion maestra ratificada (m = 0), con M = 0 declarado:

    d2_t Psi = d2_{r*} Psi - (1/r^2) L2_theta Psi ,   L2_theta = -(1/sin t) d_t ( sin t d_t Psi )
    (M = 0  =>  f = 1, r(r*) = r*  EXACTO: sin tortuga, sin Newton-Raphson, sin potencial de Schwarzschild)

Esquema: leapfrog escalonado (campo en n entero, velocidad en n+1/2), el mismo del banco 1D certificado.
Arranque de segundo orden: v^{1/2} = (dt/2) a(Psi^0) con d_t Psi(0) = 0.

Cota de paso (R2, LITERAL): dt <= CFL [ 1/(dr*)^2 + max( 1/( r^2 (dtheta)^2 ) ) ]^(-1/2) , CFL <= 0.50.
FALLA CERRADO si CFL > 0.50. El dt efectivo se toma dt = T/ceil(T/dt_cota) para caer EXACTAMENTE en t = T
en las tres mallas (si no, cada malla evalua otro tiempo y el residuo compara objetos distintos).

Mallas NO ANIDADAS (ratificado D1): hr_k = Delta_0/2^k con offset delta_k = k * Delta_0 / 3 (formula
RATIFICADA). La formula SELLADA delta_k = k * Delta_k / 3 se cuenta viva aqui como TRAMPA: anida los
niveles 1 y 2 (200 nodos compartidos medidos con fracciones exactas). No se parchea: se cita.

Bordes (R3): theta en [0, pi/2]; polo t = 0 por L'Hopital discreto (paridad PAR): L2 u|_0 = -4(u_1-u_0)/h^2;
ecuador t = pi/2 con NEUMANN por fantasma par dentro de la forma de FLUJO. Radiales: Dirichlet homogeneo
forzado en las DOS filas extremas (el frente nunca los alcanza durante T: control C5 lo declara).

Interpolacion DECLARADA (medidor, no adorno): Lagrange de 6 puntos en r* sobre la malla de evaluacion. Su
error se MIDE comparando con Lagrange de 8 puntos y se exige error_interp < 0.05 * d1 (si no, p mide el
interpolador). No hay interpolacion angular: los nodos theta de la malla gruesa son nodos exactos de las finas.

Norma (D4 declarada): L2 con MEDIDA FISICA r^2 sin(theta) dr dtheta sobre la malla de evaluacion. La razon
d1/d2 es invariante a la normalizacion; se imprimen las dos (absoluta y relativa).

Controles: C1 (piso de redondeo UMBRAL_F3 = 100 eps, semantica del banco 1D l.108/l.393) . C2 (reduccion: dato
independiente de theta, rama l = 0, debe dar p ~ 2) . C3a (control negativo: radial a PRIMER ORDEN, debe dar
|p-2| > 0.05) . C3b (control negativo: angular a PRIMER ORDEN) . C4 (sonda de la cota: la cota R2 debe
REFUSAR CFL > 0.50) . C5 (distancia sonda-frontera > T).

Umbral del gate: |p - 2.00| <= 0.05 (ratificado D2 del dueno; la escalera sellada F9 fija 0.15). Dos umbrales
sobre UNA medicion: un ROJO de F2 con F9 verde no es contradiccion.
"""

import argparse
import hashlib
import math
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction

import numpy as np

HUELLA = "HUELLA-ARNES-RICHARDSON-2D-F2-20261013"

EPS = 2.220446049250313e-16
UMBRAL_F3 = 100.0 * EPS          # sim/driver_rw_zerilli_1d.py:108 -- semantica reusada en C1
CFL_SELLADO = 0.50               # R2, fail-closed
UMBRAL_P = 0.05                  # ratificado por el dueno (escalera sellada F9: 0.15)
P_ESPERADO = 2.00


# ------------------------------------------------------------------------------------------------
# Reloj, identidad
# ------------------------------------------------------------------------------------------------

def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_de(ruta):
    h = hashlib.sha256()
    try:
        with open(ruta, "rb") as fh:
            for bloque in iter(lambda: fh.read(1 << 16), b""):
                h.update(bloque)
    except OSError:
        return None
    return h.hexdigest()


def identidad_self():
    ruta = __file__
    txt = None
    try:
        with open(ruta, "r", encoding="utf-8") as fh:
            txt = fh.read()
    except OSError:
        pass
    return {
        "ruta": ruta,
        "sha256": sha256_de(ruta),
        "lineas": (txt.count("\n") if txt is not None else None),
        "cabezas": (txt.count("\n#") if txt is not None else None),
        "huella_en_self": (txt.count(HUELLA) if txt is not None else None),
    }


# ------------------------------------------------------------------------------------------------
# Malla 2D axisimetrica ratificada (r*, theta), theta en [0, pi/2] con polo y ecuador como NODOS
# ------------------------------------------------------------------------------------------------

class Malla2D(object):
    def __init__(self, rs_min, rs_max, nr0, nt0, cfl, nivel, modo_offset="ratificado"):
        if float(cfl) > CFL_SELLADO + 1e-12:
            raise SystemExit("R2 FAIL-CLOSED: CFL = %.10f > sellado %.10f (la cota no se rebaja)"
                             % (float(cfl), CFL_SELLADO))
        self.rs_min = float(rs_min)
        self.rs_max = float(rs_max)
        self.nivel = int(nivel)
        self.cfl = float(cfl)
        self.hr0 = (float(rs_max) - float(rs_min)) / float(nr0 - 1)
        self.nt0 = int(nt0)
        self.hr = self.hr0 / (2.0 ** self.nivel)
        if modo_offset == "ratificado":
            self.delta = self.nivel * self.hr0 / 3.0       # D1 ratificado: delta_k = k * Delta_0 / 3
        else:
            self.delta = self.nivel * self.hr / 3.0        # formula SELLADA (TRAMPA: anida 1 y 2)
        self.nr = int(math.floor((self.rs_max - self.rs_min - self.delta) / self.hr)) + 1
        self.rs = self.rs_min + self.delta + self.hr * np.arange(self.nr)
        self.nt = (self.nt0 - 1) * (2 ** self.nivel) + 1
        self.hth = 0.5 * np.pi / float(self.nt0 - 1)
        self.th = self.hth / (2.0 ** self.nivel) * np.arange(self.nt)
        self.r = self.rs.copy()                            # M = 0  =>  r(r*) = r*
        self.w_ang = 1.0 / self.r ** 2                     # (f/r^2) con f = 1
        a_r = 1.0 / self.hr ** 2
        a_th = float(np.max(1.0 / (self.r ** 2 * self.hth ** 2)))
        self.dt_cota = self.cfl / math.sqrt(a_r + a_th)     # R2 literal (sin f: f = 1)
        self.lam_r = self.hr

    def resumen(self):
        return ("nivel %d | nr=%d nt=%d | hr=%.10e delta=%.10e | r in [%.6f, %.6f] | dtheta=%.10e"
                " | dt_cota=%.10e" % (self.nivel, self.nr, self.nt, self.hr, self.delta,
                                      float(self.r[0]), float(self.r[-1]), self.hth, self.dt_cota))


def nodos_exactos_radiales(rs_min, rs_max, nr0, nivel, modo_offset):
    """Set de nodos radiales en aritmetica EXACTA (Fraction). Es el metro de no-anidamiento."""
    d0 = Fraction(int(round((rs_max - rs_min) * 10 ** 6)), int(nr0 - 1) * 10 ** 6)
    hr = d0 / (2 ** nivel)
    delta = (nivel * d0 / 3) if modo_offset == "ratificado" else (nivel * hr / 3)
    n = int((Fraction(int(round(rs_max * 10 ** 6)), 10 ** 6)
             - Fraction(int(round(rs_min * 10 ** 6)), 10 ** 6) - delta) // hr) + 1
    base = Fraction(int(round(rs_min * 10 ** 6)), 10 ** 6)
    return set(base + delta + hr * j for j in range(n)), hr, delta, n


def contar_compartidos(conj_a, conj_b):
    return len(conj_a & conj_b)


# ------------------------------------------------------------------------------------------------
# Operadores (R3 y radial). Escritos aqui desde la letra ratificada; NO importados del driver ajeno.
# ------------------------------------------------------------------------------------------------

def L2_theta(u, th, hth, orden=2):
    """L2_theta u = -(1/sin t) d_t ( sin t d_t u ).

    orden 2: forma de FLUJO conservativa (semiceldas), polo por L'Hopital discreto, ecuador con fantasma par.
    orden 1 (control negativo C3b): flujo con DIFERENCIA HACIA ADELANTE y divergencia hacia atras => O(hth).
    """
    nr, nt = u.shape
    out = np.zeros_like(u)
    u_p = np.empty((nr, nt))
    u_p[:, :-1] = u[:, 1:]
    u_p[:, -1] = u[:, -2]                     # ecuador: fantasma par (Neumann d_t u = 0)
    if orden == 2:
        fl_p = np.sin(th + 0.5 * hth)[None, :] * (u_p - u)
        fl_m = np.sin(th - 0.5 * hth)[None, :] * (u - np.roll(u, 1, axis=1))
        out[:, 1:] = -((fl_p[:, 1:] - fl_m[:, 1:]) / hth ** 2) / np.sin(th[1:])[None, :]
    else:
        fl = np.sin(th)[None, :] * (u_p - u) / hth          # flujo O(hth) (hacia adelante)
        fl[:, -1] = 0.0
        out[:, 1:] = -((fl[:, 1:] - fl[:, :-1]) / hth) / np.sin(th[1:])[None, :]
    out[:, 0] = -4.0 * (u[:, 1] - u[:, 0]) / hth ** 2       # polo: L'Hopital discreto (paridad PAR)
    return out


def d2r(u, hr, orden=2):
    """Segunda diferencia radial. Las dos filas extremas quedan en 0: las fuerza el borde (Dirichlet)."""
    out = np.zeros_like(u)
    if orden == 2:
        out[1:-1, :] = (u[2:, :] - 2.0 * u[1:-1, :] + u[:-2, :]) / hr ** 2
    else:                                                    # control negativo C3a: hacia adelante, O(hr)
        out[:-2, :] = (u[2:, :] - 2.0 * u[1:-1, :] + u[:-2, :]) / hr ** 2
    return out


def acel(m, u, orden_r=2, orden_th=2, nulo_ang=False):
    a = d2r(u, m.hr, orden_r)
    if not nulo_ang:
        a = a - m.w_ang[:, None] * L2_theta(u, m.th, m.hth, orden_th)
    return a


def certifica_L2(m):
    """Certifica R3 contra referencia ANALITICA EXTERNA: L2 P_2(cos t) = 6 P_2(cos t)."""
    p2 = 0.5 * (3.0 * np.cos(m.th) ** 2 - 1.0)
    u = np.tile(p2, (m.nr, 1))
    err = np.abs(L2_theta(u, m.th, m.hth, 2) - 6.0 * u)
    esc = float(np.max(np.abs(6.0 * u)))
    return {"residuo_rel_max": float(err.max() / esc),
            "error_polo_rel": float(err[:, 0].max() / esc),
            "error_ecuador_rel": float(err[:, -1].max() / esc)}


# ------------------------------------------------------------------------------------------------
# Integrador leapfrog escalonado
# ------------------------------------------------------------------------------------------------

def simula(m, dato, nsteps, dt, orden_r=2, orden_th=2, nulo_ang=False):
    u = dato(m).copy()
    u[0, :] = 0.0
    u[-1, :] = 0.0                                  # Dirichlet homogeneo forzado (declarado)
    v = 0.5 * dt * acel(m, u, orden_r, orden_th, nulo_ang)     # d_t Psi(0) = 0
    for _ in range(nsteps):
        v = v + dt * acel(m, u, orden_r, orden_th, nulo_ang)
        u = u + dt * v
        u[0, :] = 0.0
        u[-1, :] = 0.0
    return u


# ------------------------------------------------------------------------------------------------
# Dato: paquete gaussiano suave, asimetrico en r* y con contenido angular l >= 2 vivo
# ------------------------------------------------------------------------------------------------

def perfil_r(rs, rc, sr, tilt):
    return np.exp(-(rs - rc) ** 2 / (2.0 * sr ** 2)) * (1.0 + tilt * (rs - rc) / sr)


def perfil_ang(th, mix4):
    p2 = 0.5 * (3.0 * np.cos(th) ** 2 - 1.0)
    p4 = (35.0 * np.cos(th) ** 4 - 30.0 * np.cos(th) ** 2 + 3.0) / 8.0
    return p2 + mix4 * p4                            # l par => Neumann en pi/2 y paridad en el polo EXACTAS


def dato_2d(m, rc, sr, tilt, mix4):
    return perfil_r(m.rs, rc, sr, tilt)[:, None] * perfil_ang(m.th, mix4)[None, :]


def dato_reducido(m, rc, sr, tilt):
    return np.tile(perfil_r(m.rs, rc, sr, tilt)[:, None], (1, m.nt))   # rama l = 0 (independiente de theta)


# ------------------------------------------------------------------------------------------------
# Malla de evaluacion, interpolacion declarada y norma
# ------------------------------------------------------------------------------------------------

def malla_evaluacion(rs_min, rs_max, nr0, nt0, rc, sigma):
    d0 = (rs_max - rs_min) / float(nr0 - 1)
    dr = d0 / 4.0
    off = 7.0 * d0 / 24.0                                    # 7/24: no coincide con 0, 1/3, 2/3
    lo, hi = rc - 3.0 * sigma, rc + 3.0 * sigma
    nq = int(math.floor((hi - lo - off) / dr)) + 1
    rs_e = rs_min + off + dr * np.arange(nq)
    th_e = (0.5 * np.pi / float(nt0 - 1)) * np.arange(nt0)    # nodos de la malla GRUESA (exactos en las finas)
    return rs_e, th_e, dr, 0.5 * np.pi / float(nt0 - 1)


def matriz_pesos(x, xq, orden):
    """Filas: pesos de Lagrange de `orden` puntos sobre la malla uniforme x, evaluados en xq."""
    n = x.size
    h = float(x[1] - x[0])
    W = np.zeros((xq.size, n))
    for a, xa in enumerate(xq):
        i0 = int(round((xa - x[0]) / h)) - orden // 2
        i0 = max(0, min(i0, n - orden))
        idx = np.arange(i0, i0 + orden)
        xn = x[idx]
        w = np.ones(orden)
        for k in range(orden):
            num = np.delete(xa - xn, k)
            den = np.delete(xn[k] - xn, k)
            w[k] = float(np.prod(num) / np.prod(den))
        W[a, idx] = w
    return W


def interpola(U, W):
    return W @ U


def norma(Y, rs_e, th_e, dr, dth):
    w = (rs_e[:, None] ** 2) * np.sin(th_e)[None, :] * dr * dth
    return math.sqrt(float(np.sum(Y * Y * w)))


# ------------------------------------------------------------------------------------------------
# Terna no anidada + Richardson
# ------------------------------------------------------------------------------------------------

def terna(args, dato, orden_r=2, orden_th=2, nulo_ang=False):
    mall, sol = [], []
    for k in (0, 1, 2):
        m = Malla2D(args.rs_min, args.rs_max, args.nr0, args.nt0, args.cfl, k, args.modo_offset)
        nsteps = int(math.ceil(args.T / m.dt_cota))
        dt = args.T / float(nsteps)
        if dt > m.dt_cota * (1.0 + 1e-12):
            raise SystemExit("FALLO FAIL-CLOSED: dt efectivo excede la cota R2.")
        sol.append(simula(m, dato, nsteps, dt, orden_r, orden_th, nulo_ang))
        mall.append(m)
    return mall, sol


def evalua(mall, sol, rs_e, th_e, W6, W8, nt0):
    Y = []
    for m, U in zip(mall, sol):
        idx_th = np.arange(nt0) * (m.nt // nt0)          # nodos theta de la malla gruesa dentro de esta malla
        Y.append(interpola(U[:, idx_th], W6))
    return Y


def interp_metre(mall, sol, W6, W8, nt0):
    peor = 0.0
    for m, U in zip(mall, sol):
        idx_th = np.arange(nt0) * (m.nt // nt0)
        Uc = U[:, idx_th]
        peor = max(peor, float(np.max(np.abs((W6 - W8) @ Uc))))
    return peor


def orden_p(d1, d2, piso):
    if d1 < piso:
        return None, "C1: senal por debajo del piso de redondeo (ORDEN NO MEDIBLE)"
    if d2 == 0.0:
        return None, "d2 = 0 (ORDEN NO MEDIBLE)"
    r = d1 / d2
    if r <= 0.0:
        return None, "razon no positiva (ORDEN NO MEDIBLE)"
    return math.log(r, 2.0), "ok"


# ------------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Gate 2D-F2: Richardson 2D axisimetrico no anidado")
    ap.add_argument("--estricto", action="store_true")
    ap.add_argument("--stamp", default=None, help="instante para nombrar el crudo y su huella")
    ap.add_argument("--cfl", type=float, default=CFL_SELLADO)
    ap.add_argument("--T", type=float, default=8.0)
    ap.add_argument("--nr0", type=int, default=64)
    ap.add_argument("--nt0", type=int, default=33)
    ap.add_argument("--rs-min", dest="rs_min", type=float, default=2.0)
    ap.add_argument("--rs-max", dest="rs_max", type=float, default=42.0)
    ap.add_argument("--rc", type=float, default=22.0)
    ap.add_argument("--sigma", type=float, default=2.0)
    ap.add_argument("--tilt", type=float, default=0.35)
    ap.add_argument("--mix4", type=float, default=0.35)
    ap.add_argument("--modo-offset", dest="modo_offset", default="ratificado",
                    choices=["ratificado", "sellado"])
    ap.add_argument("--control-orden1-radial", dest="c3a", action="store_true")
    ap.add_argument("--control-orden1-angular", dest="c3b", action="store_true")
    args = ap.parse_args()

    t0 = time.time()
    ident = identidad_self()

    print("=" * 96)
    print("ARNES RICHARDSON 2D-F2 -- AUTOCONVERGENENCIA NO ANIDADA (GATE 2D-F2)")
    print("=" * 96)
    print("HUELLA DEL ARNES : %s" % HUELLA)
    if args.stamp:
        print("HUELLA-CRUDO-2D-F2-RICHARDSON-%s" % args.stamp)
        print("CRUDO DECLARADO : sim/data/crudo_2d_f2_richardson_%s.txt" % args.stamp)
    print("T_UTC_CORRIDA    : %s" % utc_now())
    print("IDENTIDAD SELF   : %s | sha256 %s | %s lineas | %s cabezas | huella en self %s veces"
          % (ident["ruta"].split("/")[-1], (ident["sha256"] or "?")[:16], ident["lineas"],
             ident["cabezas"], ident["huella_en_self"]))
    print()
    print("UNIVERSO DECLARADO : malla 2D axisimetrica RATIFICADA (r*, theta) con m = 0, theta en [0, pi/2],")
    print("                     r* en [%.6f, %.6f], nr0 = %d, nt0 = %d, M = 0 (r(r*) = r* exacto),"
          % (args.rs_min, args.rs_max, args.nr0, args.nt0))
    print("                     CFL = %.10f, T = %.10f, terna no anidada delta_k = k*Delta_0/3."
          % (args.cfl, args.T))
    print("QUEDA FUERA        : capa absorbente (F11 vedado) . potencial de Schwarzschild (M > 0) . extraccion")
    print("                     de sobretonos . frentes de reflexion y extractor (R6 bloqueados) . .git.")
    print("UNIDAD             : nodo / celda / paso temporal / linea.")
    print("UMBRAL DEL GATE    : |p - %.2f| <= %.2f  (ratificado; escalera sellada F9 fija 0.15)"
          % (P_ESPERADO, UMBRAL_P))
    print("NORMA              : L2 con medida fisica r^2 sin(theta) dr dtheta sobre la malla de evaluacion.")
    print("NULO/CONTROLES     : C1 piso UMBRAL_F3 = %.15e | C2 reduccion l = 0 | C3a radial 1er orden"
          % UMBRAL_F3)
    print("                     | C3b angular 1er orden | C4 la cota debe REFUSAR CFL > 0.50 | C5 margen > T.")
    print("COMANDO            : python3 -B sim/arnes_richardson_2d_f2.py --estricto")
    print()

    if args.cfl > CFL_SELLADO + 1e-12:
        raise SystemExit("FALLO FAIL-CLOSED: CFL %r > sellado %r (R2)" % (args.cfl, CFL_SELLADO))

    # ---- C4: sonda de la cota (la cota R2 debe REFUSAR CFL > 0.50) ----
    try:
        Malla2D(args.rs_min, args.rs_max, args.nr0, args.nt0, 0.750000, 0)
        c4 = "NO REFUSADA -- DEFECTO DEL MEDIDOR: la cota no bloquea"
    except SystemExit as exc:
        c4 = "REFUSADA: %s" % (exc,)
    print("[C4] SONDA DE LA COTA (R2, fail-closed): CFL = 0.750000 -> %s" % c4)
    print("     Respaldo medido del aviso: 0.707200 -> 4.869481e-06 | 0.750000 -> 2.922646e+24 (adenda 1, seccion 6).")
    print()

    # ---- Mallas, no-anidamiento medido con fracciones exactas ----
    print("[MALLAS] ternas y NO-ANIDAMIENTO medido en aritmetica EXACTA (Fraction)")
    mall_demo = [Malla2D(args.rs_min, args.rs_max, args.nr0, args.nt0, args.cfl, k, args.modo_offset)
                 for k in (0, 1, 2)]
    for m in mall_demo:
        print("   %s" % m.resumen())
    sets = {}
    for modo in ("ratificado", "sellado"):
        sets[modo] = [nodos_exactos_radiales(args.rs_min, args.rs_max, args.nr0, k, modo) for k in (0, 1, 2)]
        pares = [(0, 1), (0, 2), (1, 2)]
        cuentas = [contar_compartidos(sets[modo][a][0], sets[modo][b][0]) for a, b in pares]
        offs = ["%.6f" % float(sets[modo][k][2]) for k in (0, 1, 2)]
        print("   modo %-11s offsets = %s | nodos compartidos (0,1)=%d (0,2)=%d (1,2)=%d"
              % (modo, "/".join(offs), cuentas[0], cuentas[1], cuentas[2]))
    if args.modo_offset == "sellado":
        print("   TRAMPA VIVA: modo SELLADO elegido por argv -- los niveles 1 y 2 SE ANIDAN.")
    print("   TRAMPA (se cita, no se parchea): la formula sellada delta_k = k*Delta_k/3 declara que ningun nodo")
    print("   se comparte y anida los niveles 1 y 2 (offsets iguales). La ratificada es delta_k = k*Delta_0/3.")
    print()

    # ---- certificacion del operador angular contra la referencia analitica externa ----
    print("[COTEJO] OPERADOR ANGULAR R3 contra referencia ANALITICA EXTERNA (L2 P_2 = 6 P_2)")
    for m in mall_demo:
        c = certifica_L2(m)
        print("   nivel %d: residuo_rel_max = %.6e | error_polo_rel = %.6e | error_ecuador_rel = %.6e"
              % (m.nivel, c["residuo_rel_max"], c["error_polo_rel"], c["error_ecuador_rel"]))
    print()

    # ---- C5: margen sonda-frontera ----
    front = args.T
    marg = min(min(args.rc - 4.0 * args.sigma - float(m.r[0]),
                   float(m.r[-1]) - args.rc - 4.0 * args.sigma) for m in mall_demo)
    print("[C5] FRONTERA: frente de luz T = %.6f | margen sonda-frontera minimo = %.6f | %s"
          % (front, marg, "OK (margen > T)" if marg > front else "VIOLADO: resultado contaminado por frontera"))
    print()

    # ---- malla de evaluacion ----
    rs_e, th_e, dr_e, dth_e = malla_evaluacion(args.rs_min, args.rs_max, args.nr0, args.nt0, args.rc, args.sigma)
    W6 = matriz_pesos(mall_demo[0].rs, rs_e, 6)
    W8 = matriz_pesos(mall_demo[0].rs, rs_e, 8)
    ext = [nodos_exactos_radiales(args.rs_min, args.rs_max, args.nr0, k, args.modo_offset)[0] for k in (0, 1, 2)]
    print("[EVAL] malla de evaluacion: %d nodos r* en [%.6f, %.6f] (paso %.6f, offset 7*Delta_0/24) x %d nodos theta"
          % (rs_e.size, float(rs_e[0]), float(rs_e[-1]), dr_e, th_e.size))
    print("       interpolacion DECLARADA: Lagrange de 6 puntos en r*; error medido contra Lagrange de 8 puntos.")
    for k in (0, 1, 2):
        print("       nodos compartidos evaluacion vs malla %d = %d"
              % (k, contar_compartidos(set(Fraction(int(round(x * 10 ** 6)), 10 ** 6) for x in rs_e), ext[k])))
    print()

    # ---- corridas ----
    piso_ref = None

    def corre_terna(etiqueta, dato, orden_r=2, orden_th=2, nulo_ang=False):
        mall, sol = terna(args, dato, orden_r, orden_th, nulo_ang)
        Y = evalua(mall, sol, rs_e, th_e, W6, W8, args.nt0)
        e_interp = interp_metre(mall, sol, W6, W8, args.nt0)
        nY = [norma(Y[i], rs_e, th_e, dr_e, dth_e) for i in range(3)]
        d1 = norma(Y[0] - Y[1], rs_e, th_e, dr_e, dth_e)
        d2 = norma(Y[1] - Y[2], rs_e, th_e, dr_e, dth_e)
        mx = max(float(np.max(np.abs(Y[i]))) for i in range(3))
        piso = UMBRAL_F3 * mx
        p, causa = orden_p(d1, d2, piso)
        p_rel = (orden_p(d1 / max(nY[2], 1e-300), d2 / max(nY[2], 1e-300), UMBRAL_F3)[0]
                 if nY[2] > 0.0 else None)
        razon = (d1 / d2) if d2 > 0.0 else float("inf")
        veredicto = ("NO MEDIBLE" if p is None
                     else ("VERDE" if abs(p - P_ESPERADO) <= UMBRAL_P else "ROJO"))
        interp_ok = bool(e_interp < 0.05 * d1)
        print("--- %s" % etiqueta)
        for i, m in enumerate(mall):
            nsteps = int(math.ceil(args.T / m.dt_cota))
            print("    nivel %d: nr=%d nt=%d dt=%.10e pasos=%d" % (m.nivel, m.nr, m.nt, args.T / nsteps, nsteps))
        print("    d1 = ||Psi_2h - Psi_h||_L2      = %.6e" % d1)
        print("    d2 = ||Psi_h  - Psi_h/2||_L2    = %.6e" % d2)
        print("    razon d1/d2                     = %.6f   (esperado 2^p = %.4f)" % (razon, 2.0 ** (p or 0.0)))
        print("    p = log2(d1/d2)                 = %s" % ("NO MEDIBLE" if p is None else "%.6f" % p))
        print("    p relativo (normalizado por ||Psi_2||) = %s" % ("NO MEDIBLE" if p_rel is None else "%.6f" % p_rel))
        print("    ||Psi_2h||_L2 = %.6e | ||Psi_h||_L2 = %.6e | ||Psi_h/2||_L2 = %.6e"
              % (nY[0], nY[1], nY[2]))
        print("    piso de redondeo (C1) = %.6e  |  max|Psi| = %.6e" % (piso, mx))
        print("    error_interp medido = %.6e  |  0.05*d1 = %.6e  |  %s"
              % (e_interp, 0.05 * d1, "OK (el interpolador no manda)" if interp_ok else "EXCEDE: p mediria el interpolador"))
        print("    causa = %s" % causa)
        print("    VEREDICTO %s = %s" % (etiqueta, veredicto))
        print()
        return {"etiqueta": etiqueta, "d1": d1, "d2": d2, "razon": razon, "p": p, "veredicto": veredicto,
                "interp_ok": interp_ok, "e_interp": e_interp}

    dato = lambda m: dato_2d(m, args.rc, args.sigma, args.tilt, args.mix4)
    r_principal = corre_terna("F2 PRINCIPAL (angular vivo, l >= 2)", dato)

    dato_red = lambda m: dato_reducido(m, args.rc, args.sigma, args.tilt)
    r_reducido = corre_terna("C2 REDUCCION (dato independiente de theta, rama l = 0)", dato_red)

    print("[C2] PAR DE DOMINIO (p reducido | p con angular vivo) = (%s | %s)"
          % ("NO MEDIBLE" if r_reducido["p"] is None else "%.6f" % r_reducido["p"],
             "NO MEDIBLE" if r_principal["p"] is None else "%.6f" % r_principal["p"]))
    print()

    r_c3a = corre_terna("C3a CONTROL NEGATIVO (radial a PRIMER ORDEN)", dato, orden_r=1)
    r_c3b = corre_terna("C3b CONTROL NEGATIVO (angular a PRIMER ORDEN)", dato, orden_th=1)

    def discrimina(r):
        if r["p"] is None:
            return "NO MEDIBLE (no discrimina por ausencia de senal)"
        return ("DISCRIMINA (|p-2| = %.6f > %.2f)" % (abs(r["p"] - P_ESPERADO), UMBRAL_P)
                if abs(r["p"] - P_ESPERADO) > UMBRAL_P else
                "NO DISCRIMINA: este medidor no distingue primer de segundo orden")

    print("[C3] C3a %s" % discrimina(r_c3a))
    print("[C3] C3b %s" % discrimina(r_c3b))
    print()

    rojos = []
    if r_principal["veredicto"] != "VERDE":
        rojos.append("F2 PRINCIPAL: %s" % r_principal["veredicto"])
    if not r_principal["interp_ok"]:
        rojos.append("interpolador por encima de 0.05*d1")
    if not (marg > front):
        rojos.append("C5 frontera violada")
    if r_reducido["veredicto"] == "NO MEDIBLE":
        rojos.append("C2 reduccion NO MEDIBLE")
    if "DISCRIMINA" not in discrimina(r_c3a) and "DISCRIMINA" not in discrimina(r_c3b):
        rojos.append("ningun control negativo discrimina: F2 no certifica nada")

    print("[RESUMEN]")
    print("   p(F2) = %s   veredicto = %s" % ("NO MEDIBLE" if r_principal["p"] is None
                                              else "%.6f" % r_principal["p"], r_principal["veredicto"]))
    print("   p(C2) = %s | p(C3a) = %s | p(C3b) = %s"
          % ("NO MEDIBLE" if r_reducido["p"] is None else "%.6f" % r_reducido["p"],
             "NO MEDIBLE" if r_c3a["p"] is None else "%.6f" % r_c3a["p"],
             "NO MEDIBLE" if r_c3b["p"] is None else "%.6f" % r_c3b["p"]))
    print("   rojos = %d %s" % (len(rojos), ("| " + " ; ".join(rojos)) if rojos else ""))
    print("   T_UTC_FIN = %s | duracion = %.2f s" % (utc_now(), time.time() - t0))
    print("=" * 96)

    if args.estricto and rojos:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
