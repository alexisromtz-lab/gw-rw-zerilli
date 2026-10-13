#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HUELLA-ARNES-RICHARDSON-2D-F2-V3-20261013
"""
ARNES INDEPENDIENTE -- GATE 2D-F2 v3: AUTOCONVERGENCIA DE RICHARDSON EN 2D AXISIMETRICO
========================================================================================

HUELLA-ARNES-RICHARDSON-2D-F2-V3-20261013

V3 = V2 + UNA LINEA (el ancla de la ventana). Causa MEDIDA del cambio: en las DOS ternas corridas con el
v2 (nr0 = 64 y nr0 = 128) el control C6 de contencion salio FALSO NEGATIVO por aritmetica EXACTA, no por
el motor: el offset off = 7*Delta_0/24 = 0.185185 se sumaba DENTRO del ancla, de modo que el primer nodo
de evaluacion caia en lo + off y quedaba a (7 - 6)*Delta_0/24 = Delta_0/24 = 0.026455 MAS ALLA de la
tolerancia dr = 6*Delta_0/24 del propio control (nr0 = 64: primer nodo 8.185185 contra borde 8.000000;
nr0 = 128: 8.091864 contra 8.000000). La seccion 2.2 de la orden del dueno ("Ajustar la ventana de
medicion a las coordenadas reales del paquete para evitar falsos negativos en los controles de borde") se
aplica en su termino: el ancla se corre hacia afuera por off (lo = rc - T - 3 sigma - off) y el primer
nodo cae EXACTAMENTE en el borde declarado de la banda del paquete. El techo hi, el paso dr y los offsets
nodo-a-nodo NO se tocan; UMBRAL_P = 0.05 y CFL_SELLADO = 0.50 quedan INMUTABLES. El v2 NO se parchea: se
cita, y su corrida queda como foto previa (su copia byte-identica es el commit 6a186ed de este arbol).

ORDEN QUE AUTORIZA ESTA PIEZA (dueno, 13-Oct-2026, contrato A2.1, seccion 2): «Se autoriza la
modificacion de sim/arnes_richardson_2d_f2.py (o la emision de su version corregida
sim/arnes_richardson_2d_f2_v2.py)». Se emite la V2. El v1 NO se toca: su blob de disco esta en
estado " M" por otra mano, su congelamiento sigue vigente y su identidad se imprime aqui.

UNIVERSO DECLARADO (7 piezas):
  1. este archivo (sim/arnes_richardson_2d_f2_v2.py), SIN RASTREAR al nacer;
  2. sim/arnes_richardson_2d_f2.py | 576 l | blob 48b5859e337984e21c4b07342faa234807ed535d |
     CONGELADO: fuente citada, NO mutada (la v2 es un instrumento aparte, no un parche in situ);
  3. sim/arnes_aislamiento_piso_2d.py | 593 l | SIN RASTREAR: la sonda que midio el arranque exacto;
  4. sim/data/crudo_aislamiento_piso_2d_20261013T200929Z.json | 246 l | RATIFICADO por la orden, §1;
  5. sim/PREREGISTRO_RICHARDSON_2D_F2_20261013.md | blob c91d8447 | SIN RASTREAR;
  6. sim/PREREGISTRO_FRENTE_2D_CQG_20261013.md | blob 2b2dd0fa | commit 2eebc3b;
  7. sim/ADENDA_1_RATIFICACION_SECCION_4_Y_ESQUEMA_2D_RATIFICADO_20261013.md | blob 94aa523d | commit 90759a8.
El .git del arbol queda FUERA del universo contado.
MOTOR: numpy (sin scipy, sin red, sin aleatoriedad, sin estado oculto): el mismo argv produce el
       mismo crudo.
UNIDAD: nodo / celda / paso temporal / linea / encabezado.
VENTANA: reloj UTC impreso en la cabecera.

LO QUE ESTA PIEZA PORTA -- TRES DELTAS, NI UNA MAS
  DELTA 1 (arranque exacto). El v1 sembraba la velocidad con medio paso de fuerza evaluada en
    t = 0, es decir v^{+1/2}, dentro de un bucle PATEAR-LUEGO-ARRASTRAR que espera v^{n-1/2}. Esa
    semilla inyecta dt^2 a(u^0) en el primer arrastre => error GLOBAL O(dt) => orden 1. Aqui se
    siembra v^{-1/2} desde la Cauchy simetrica u^{-1} = u^0 + 0.5 dt^2 a(u^0), con
    u_ddot^0 = grad^2 u^0 y d_t Psi(0) = 0: la misma formulacion que la sonda directa valido
    (sim/arnes_aislamiento_piso_2d.py, arranque "exacto"). El signo OPUESTO de ese termino
    (arranque "ajeno": u^{-1} = u^0 - 0.5 dt^2 a0) es el defecto del v1.
  DELTA 2 (ventana sincronizada). El v1 anclaba la malla de evaluacion en rs_min con
    lo = rc - 3 sigma y hi = rc + 3 sigma, o sea la ventana de la CONDICION INICIAL: a t = T el
    paquete ya no esta ahi (con M = 0 el frente se parte en dos mitades, centradas en rc - T y
    rc + T). Aqui el ancla son las coordenadas REALES del paquete a t = T:
    lo = rc - T - 3 sigma, hi = rc + T + 3 sigma. El offset 7*Delta_0/24 y el paso dr = Delta_0/4
    SE CONSERVAN: con ellos ningun nodo de evaluacion coincide con nodo de malla (se mide y se imprime).
  DELTA 3 (escritor de crudo). El v1 imprimia una huella de crudo y una ruta declarada
    (sim/data/crudo_2d_f2_richardson_<stamp>.txt) que NUNCA escribia. Aqui --json escribe de verdad
    y el archivo se relee para certificar lineas, bytes y sha256.

LO QUE NO CAMBIA (sellado, inmutable): ecuacion, operador angular R3, malla 2D, cota R2 con
CFL_SELLADO = 0.50, formula RATIFICADA de no-anidamiento delta_k = k*Delta_0/3 (la sellada
delta_k = k*Delta_k/3 se cita como TRAMPA, no se parchea), dato, norma, interpolacion declarada,
controles C1..C5, y el UMBRAL SELLADO |p - 2.00| <= 0.05. La v2 no rebaja ningun umbral: agrega un
control C6 de contencion que el v1 no tenia (el defecto que la v2 repara era precisamente invisible
sin ese control).

Los crudos que emite este arnes son SALIDA del instrumento, no escritura manual del agente.
"""

import argparse
import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction

import numpy as np

HUELLA = "HUELLA-ARNES-RICHARDSON-2D-F2-V3-20261013"
HUELLA_V2_CITADA = "HUELLA-ARNES-RICHARDSON-2D-F2-V2-20261013"   # v2: foto previa (commit 6a186ed)
HUELLA_V1 = "HUELLA-ARNES-RICHARDSON-2D-F2-20261013"

EPS = 2.220446049250313e-16
UMBRAL_F3 = 100.0 * EPS          # sim/driver_rw_zerilli_1d.py:108 -- semantica reusada en C1
CFL_SELLADO = 0.50               # R2, fail-closed (SELLADO, inmutable)
UMBRAL_P = 0.05                  # SELLADO por el dueno (escalera sellada F9 fija 0.15)
P_ESPERADO = 2.00

REF_PISO_F2 = 1.081241e-02       # piso medido por el v1 (h-independiente), citado como referencia
REF_D2_EXACTO = 4.224460e-04     # d2 del arranque exacto con observable TOTAL (sonda de aislamiento)

SITIOS_CORREGIDOS = [
    "simula(): arranque v^{+1/2} -> v^{-1/2} por Cauchy simetrica (u^{-1} = u^0 + 0.5 dt^2 a0)",
    "malla_evaluacion(): ancla rs_min -> ancla en las coordenadas reales del paquete (rc -+ T -+ 3 sigma)",
    "main(): escritor de crudo JSON real (el v1 declaraba un crudo que no escribia)",
    "main(): control C6 de contencion ventana <-> paquete (el v1 no lo tenia)",
    "malla_evaluacion(): DELTA 4 -- el ancla INCLUYE el offset (lo = rc - T - 3 sigma - off): el primer nodo cae EXACTO en el borde declarado de la banda del paquete (en v2 quedaba a Delta_0/24 fuera)",
]


# ------------------------------------------------------------------------------------------------
# Reloj, identidad
# ------------------------------------------------------------------------------------------------

def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp_utc():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


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
    if txt is None:
        return {"ruta": ruta, "sha256": sha256_de(ruta), "lineas": None, "cabezas": None,
                "encabezados": None, "huella_en_self": None, "bytes": None}
    return {
        "ruta": ruta,
        "sha256": sha256_de(ruta),
        "bytes": len(txt.encode("utf-8")),
        "lineas": txt.count("\n"),
        "cabezas": txt.count("\n#"),                       # mismo metro del v1 (continuidad de identidad)
        "encabezados": sum(1 for ln in txt.splitlines() if ln.startswith("#")),
        "huella_en_self": txt.count(HUELLA),
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
        self.hth_0 = 0.5 * np.pi / float(self.nt0 - 1)
        self.hth = self.hth_0 / (2.0 ** self.nivel)   # paso LOCAL del nivel (el paso de la malla 0 NO sirve)
        self.th = self.hth * np.arange(self.nt)
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
# Integrador leapfrog escalonado -- DELTA 1
# ------------------------------------------------------------------------------------------------

def simula(m, dato, nsteps, dt, orden_r=2, orden_th=2, nulo_ang=False):
    """PATEAR-LUEGO-ARRASTRAR con la velocidad escalonada en n-1/2 (invariante de la reparacion de F1).

    DELTA 1: el arranque. El v1 sembraba la velocidad con medio paso de fuerza evaluada en t = 0
    (v^{+1/2}) dentro de un bucle que espera v^{n-1/2}: esa semilla inyecta dt^2 a(u^0) en el primer
    arrastre => error GLOBAL O(dt) => el orden medido cae a 1. Aqui se siembra v^{-1/2} desde la
    Cauchy SIMETRICA u^{-1} = u^0 + 0.5 dt^2 a(u^0), con u_ddot^0 = grad^2 u^0 (d_t Psi(0) = 0).
    """
    u = dato(m).copy()
    u[0, :] = 0.0
    u[-1, :] = 0.0                                  # Dirichlet homogeneo forzado (declarado)
    a0 = acel(m, u, orden_r, orden_th, nulo_ang)    # u_ddot^0 = grad^2 u^0 (d_t Psi(0) = 0)
    u_m1 = u + 0.5 * dt * dt * a0                   # u^{-1} de segundo orden SIMETRICO
    u_m1[0, :] = 0.0
    u_m1[-1, :] = 0.0
    v = (u - u_m1) / dt                             # v^{-1/2}: lo que el bucle PATEAR-LUEGO-ARRASTRAR espera
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
# Ventana: lo declarado por el v1, lo real del paquete -- DELTA 2
# ------------------------------------------------------------------------------------------------

def ventana_declarada(rc, sigma, T):
    """Devuelve las tres bandas radiales que el control C6 distingue.

    (a) DECLARADA (v1): la condicion inicial, rc -+ 3 sigma.
    (b) PAQUETE a t = T: las DOS mitades del frente (M = 0 parte el paquete en rc - T y rc + T),
        soporte rc -+ T -+ 3 sigma.
    (c) MITAD ENTRANTE a t = T: rc - T -+ 3 sigma.
    """
    return {"declarada": (rc - 3.0 * sigma, rc + 3.0 * sigma),
            "paquete": (rc - T - 3.0 * sigma, rc + T + 3.0 * sigma),
            "entrante": (rc - T - 3.0 * sigma, rc - T + 3.0 * sigma)}


def contiene(rs, lo, hi, tol=0.0):
    """True si la malla de evaluacion cubre la banda [lo, hi] (con tolerancia declarada)."""
    return bool(float(rs[0]) <= lo + tol and float(rs[-1]) >= hi - tol)


def malla_evaluacion(rs_min, rs_max, nr0, nt0, rc, sigma, T):
    """Malla de evaluacion ANCLADA A LAS COORDENADAS REALES DEL PAQUETE A t = T.

    DELTA 2: el v1 anclaba en rs_min + off (extremo izquierdo del dominio) y con lo = rc - 3 sigma,
    hi = rc + 3 sigma; la ventana efectiva caia en [2.09, 13.98] (nr0 = 128) y NO contenia al
    paquete: el observable medido no era el declarado. Aqui el ancla es lo = rc - T - 3 sigma y el
    techo hi = rc + T + 3 sigma. El offset 7*Delta_0/24 y el paso dr = Delta_0/4 se conservan.

    DELTA 4 (v3): el offset off = 7*Delta_0/24 se aplica FUERA del ancla (lo = rc - T - 3 sigma - off), de
    modo que rs_e[0] = lo + off = rc - T - 3 sigma EXACTO: el primer nodo cae sobre el borde declarado del
    paquete y el criterio de C6 (tolerancia dr) se mide contra la construccion, no contra ella misma corrida
    por Delta_0/24. El v2 aplicaba el offset dentro del ancla y su C6 salia falso negativo en las dos ternas.
    """
    d0 = (rs_max - rs_min) / float(nr0 - 1)
    dr = d0 / 4.0
    off = 7.0 * d0 / 24.0                                    # 7/24: no coincide con 0, 1/3, 2/3
    lo = rc - T - 3.0 * sigma - off                         # DELTA 4: el ancla INCLUYE el offset
    hi = rc + T + 3.0 * sigma
    nq = int(math.floor((hi - lo - off) / dr)) + 1
    rs_e = lo + off + dr * np.arange(nq)                    # rs_e[0] = rc - T - 3 sigma EXACTO
    th_e = (0.5 * np.pi / float(nt0 - 1)) * np.arange(nt0)    # nodos de la malla GRUESA (exactos en las finas)
    return rs_e, th_e, dr, 0.5 * np.pi / float(nt0 - 1), lo, hi


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


def indices_theta(m, nt0):
    """Nodos theta de la malla gruesa (nivel 0) DENTRO de la malla m: el paso se reduce 2^nivel."""
    return np.arange(nt0) * ((m.nt - 1) // (nt0 - 1))


def coherencia_theta(m, th_e, nt0):
    """Residuo relativo entre los nodos theta elegidos y los de la malla gruesa (debe ser 0)."""
    return float(np.max(np.abs(m.th[indices_theta(m, nt0)] - th_e)) / (0.5 * np.pi))


def evalua(mall, sol, rs_e, nt0):
    """Pesos de Lagrange POR MALLA: la matriz de pesos vive en los nodos de origen, no en la malla 0."""
    Y = []
    for m, U in zip(mall, sol):
        W = matriz_pesos(m.rs, rs_e, 6)
        Y.append(interpola(U[:, indices_theta(m, nt0)], W))
    return Y


def interp_metre(mall, sol, rs_e, nt0):
    peor = 0.0
    for m, U in zip(mall, sol):
        Uc = U[:, indices_theta(m, nt0)]
        W6 = matriz_pesos(m.rs, rs_e, 6)
        W8 = matriz_pesos(m.rs, rs_e, 8)
        peor = max(peor, float(np.max(np.abs((W6 - W8) @ Uc))))
    return peor


def orden_p(d1, d2, piso):
    """C1 ANTES de la identidad: una identidad aritmetica no es un gate."""
    if d1 < piso:
        return None, "C1: senal por debajo del piso de redondeo (ORDEN NO MEDIBLE)"
    if d2 == 0.0:
        return None, "d2 = 0 (ORDEN NO MEDIBLE)"
    r = d1 / d2
    if r <= 0.0:
        return None, "razon no positiva (ORDEN NO MEDIBLE)"
    return math.log(r, 2.0), "ok"


# ------------------------------------------------------------------------------------------------
# Diagnostico de la transferencia (que del v1 esta citado y que se porto)
# ------------------------------------------------------------------------------------------------

def diagnostico_transferencia():
    aqui = os.path.dirname(os.path.abspath(__file__))
    ruta_v1 = os.path.join(aqui, "arnes_richardson_2d_f2.py")
    d = {"ruta_v1": ruta_v1, "existe_v1": os.path.isfile(ruta_v1)}
    if not d["existe_v1"]:
        return d
    with open(ruta_v1, "r", encoding="utf-8") as fh:
        t1 = fh.read()
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as fh:
        t2 = fh.read()
    patron_defecto_1 = "v = 0.5 * dt * acel"
    patron_defecto_2 = "rs_e = rs_min + off"
    d["sha256_v1"] = sha256_de(ruta_v1)
    d["lineas_v1"] = t1.count("\n")
    d["huella_v1_en_v1"] = t1.count(HUELLA_V1)
    d["defecto_1_en_v1"] = t1.count(patron_defecto_1)
    d["defecto_2_en_v1"] = t1.count(patron_defecto_2)
    d["defecto_1_en_v2"] = t2.count(patron_defecto_1)   # la sonda se cuenta a si misma: 1 = solo la sonda
    d["defecto_2_en_v2"] = t2.count(patron_defecto_2)   # idem
    d["correccion_1_en_v2"] = t2.count("u_m1 = u + 0.5 * dt * dt * a0")
    d["correccion_2_en_v2"] = t2.count("rs_e = lo + off + dr * np.arange(nq)")
    d["escritor_en_v2"] = t2.count("json.dump(")
    return d


# ------------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Gate 2D-F2 v3: Richardson 2D axisimetrico no anidado")
    ap.add_argument("--estricto", action="store_true")
    ap.add_argument("--stamp", default=None, help="instante (UTC compacto) para nombrar el crudo")
    ap.add_argument("--json", default=None,
                    help="ruta del crudo JSON de salida, o 'auto' para "
                         "sim/data/crudo_2d_f2_richardson_post_arranque_v3_nr0_<nr0>_<stamp>.json")
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
    stamp = args.stamp or stamp_utc()

    ruta_json = None
    if args.json:
        if args.json == "auto":
            ruta_json = os.path.join("sim", "data",
                                     "crudo_2d_f2_richardson_post_arranque_v3_nr0_%d_%s.json"
                                     % (args.nr0, stamp))
        else:
            ruta_json = args.json
        padre = os.path.dirname(os.path.abspath(ruta_json))
        if not os.path.isdir(padre):
            raise SystemExit("FAIL-CLOSED: el directorio del crudo no existe: %s" % padre)

    print("=" * 96)
    print("ARNES RICHARDSON 2D-F2 v3 -- AUTOCONVERGENENCIA NO ANIDADA (GATE 2D-F2)")
    print("=" * 96)
    print("HUELLA DEL ARNES : %s" % HUELLA)
    print("HUELLA v1 CITADA : %s (CONGELADO, NO mutado)" % HUELLA_V1)
    print("T_UTC_CORRIDA    : %s" % utc_now())
    print("IDENTIDAD SELF   : %s | sha256 %s | %d l | %d B | cabezas(nl#) %s | encabezados(#) %s | huella en self %s"
          % (ident["ruta"].split("/")[-1], (ident["sha256"] or "?")[:16], ident["lineas"], ident["bytes"],
             ident["cabezas"], ident["encabezados"], ident["huella_en_self"]))
    print("COMANDO REAL     : %s" % " ".join(sys.argv))
    print()
    print("UNIVERSO DECLARADO : malla 2D axisimetrica RATIFICADA (r*, theta) con m = 0, theta en [0, pi/2],")
    print("                     r* en [%.6f, %.6f], nr0 = %d, nt0 = %d, M = 0 (r(r*) = r* exacto),"
          % (args.rs_min, args.rs_max, args.nr0, args.nt0))
    print("                     CFL = %.10f, T = %.10f, terna no anidada delta_k = k*Delta_0/3."
          % (args.cfl, args.T))
    print("QUEDA FUERA        : capa absorbente (F11 vedado) . potencial de Schwarzschild (M > 0) . extraccion")
    print("                     de sobretonos . frentes de reflexion y extractor (R6 bloqueados) . .git.")
    print("UNIDAD             : nodo / celda / paso temporal / linea.")
    print("UMBRAL DEL GATE    : |p - %.2f| <= %.2f  (SELLADO, inmutable; escalera sellada F9 fija 0.15)"
          % (P_ESPERADO, UMBRAL_P))
    print("NORMA              : L2 con medida fisica r^2 sin(theta) dr dtheta sobre la malla de evaluacion.")
    print("NULO/CONTROLES     : C1 piso UMBRAL_F3 = %.15e | C2 reduccion l = 0 | C3a radial 1er orden"
          % UMBRAL_F3)
    print("                     | C3b angular 1er orden | C4 la cota debe REFUSAR CFL > 0.50 | C5 margen > T")
    print("                     | C6 contencion ventana-paquete (NUEVO en v2; ancla corregida en v3).")
    print("DELTA 1 ARRANQUE   : v^{-1/2} desde u^{-1} = u^0 + 0.5 dt^2 a(u^0)  [v1: v^{+1/2}, orden 1]")
    print("DELTA 2 VENTANA    : ancla lo = rc - T - 3 sigma, hi = rc + T + 3 sigma  [v1: lo = rc - 3 sigma]")
    print("DELTA 3 CRUDO      : %s" % (ruta_json if ruta_json else "(sin --json: no se escribira crudo)"))
    print("DELTA 4 ANCLA v3   : lo = rc - T - 3 sigma - off  [primer nodo EXACTO en el borde del paquete]")
    print()

    # ---- diagnostico de la transferencia (v1 citado vs v2 emitido) ----
    dt_info = diagnostico_transferencia()
    print("[TRANSFERENCIA] v1 citado: %s" % dt_info["ruta_v1"].split("/")[-1])
    if dt_info["existe_v1"]:
        print("   v1: %d l | sha256 %s | huella v1 presente %d veces"
              % (dt_info["lineas_v1"], (dt_info["sha256_v1"] or "?")[:16], dt_info["huella_v1_en_v1"]))
        print("   patron del defecto 1 (arranque v^{+1/2}) en v1 = %d | en este arnes = %d (1 = solo la propia sonda)"
              % (dt_info["defecto_1_en_v1"], dt_info["defecto_1_en_v2"]))
        print("   patron del defecto 2 (ancla en rs_min)   en v1 = %d | en este arnes = %d (1 = solo la propia sonda)"
              % (dt_info["defecto_2_en_v1"], dt_info["defecto_2_en_v2"]))
        print("   correccion 1 (Cauchy simetrica) = %d | correccion 2 (ancla paquete) = %d | escritor de crudo = %d"
              % (dt_info["correccion_1_en_v2"], dt_info["correccion_2_en_v2"], dt_info["escritor_en_v2"]))
    for s in SITIOS_CORREGIDOS:
        print("   DELTA: %s" % s)
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
    cuentas = {}
    offs = {}
    for modo in ("ratificado", "sellado"):
        sets[modo] = [nodos_exactos_radiales(args.rs_min, args.rs_max, args.nr0, k, modo) for k in (0, 1, 2)]
        pares = [(0, 1), (0, 2), (1, 2)]
        cuentas[modo] = [contar_compartidos(sets[modo][a][0], sets[modo][b][0]) for a, b in pares]
        offs[modo] = ["%.6f" % float(sets[modo][k][2]) for k in (0, 1, 2)]
        print("   modo %-11s offsets = %s | nodos compartidos (0,1)=%d (0,2)=%d (1,2)=%d"
              % (modo, "/".join(offs[modo]), cuentas[modo][0], cuentas[modo][1], cuentas[modo][2]))
    if args.modo_offset == "sellado":
        print("   TRAMPA VIVA: modo SELLADO elegido por argv -- los niveles 1 y 2 SE ANIDAN.")
    print("   TRAMPA (se cita, no se parchea): la formula sellada delta_k = k*Delta_k/3 declara que ningun nodo")
    print("   se comparte y anida los niveles 1 y 2 (offsets iguales). La ratificada es delta_k = k*Delta_0/3.")
    print()

    # ---- certificacion del operador angular contra la referencia analitica externa ----
    print("[COTEJO] OPERADOR ANGULAR R3 contra referencia ANALITICA EXTERNA (L2 P_2 = 6 P_2)")
    cotejo = []
    for m in mall_demo:
        c = certifica_L2(m)
        cotejo.append(c)
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

    # ---- malla de evaluacion + C6 contencion ----
    rs_e, th_e, dr_e, dth_e, lo_e, hi_e = malla_evaluacion(args.rs_min, args.rs_max, args.nr0, args.nt0,
                                                           args.rc, args.sigma, args.T)
    bandas = ventana_declarada(args.rc, args.sigma, args.T)
    ext = [nodos_exactos_radiales(args.rs_min, args.rs_max, args.nr0, k, args.modo_offset)[0] for k in (0, 1, 2)]
    coh_th = [coherencia_theta(m, th_e, args.nt0) for m in mall_demo]
    print("[EVAL] malla de evaluacion ANCLADA AL PAQUETE: %d nodos r* en [%.6f, %.6f] (paso %.6f; offset 7*Delta_0/24 FUERA del ancla)"
          % (rs_e.size, float(rs_e[0]), float(rs_e[-1]), dr_e))
    print("       banda DECLARADA por el v1 (condicion inicial) = [%.6f, %.6f]"
          % (bandas["declarada"][0], bandas["declarada"][1]))
    print("       banda REAL del paquete a t = T (dos mitades)  = [%.6f, %.6f]"
          % (bandas["paquete"][0], bandas["paquete"][1]))
    print("       banda REAL de la mitad ENTRANTE a t = T      = [%.6f, %.6f]"
          % (bandas["entrante"][0], bandas["entrante"][1]))
    c6_decl = contiene(rs_e, bandas["declarada"][0], bandas["declarada"][1], dr_e)
    c6_paq = contiene(rs_e, bandas["paquete"][0], bandas["paquete"][1], dr_e)
    c6_ent = contiene(rs_e, bandas["entrante"][0], bandas["entrante"][1], dr_e)
    print("[C6] CONTENCION (NUEVO): evaluacion cubre declarada = %s | cubre paquete = %s | cubre mitad entrante = %s"
          % (c6_decl, c6_paq, c6_ent))
    print("     criterio: la malla de evaluacion debe cubrir el PAQUETE a t = T (tolerancia = dr). El v1 no tenia")
    print("     este control y su ventana efectiva media otro objeto que el declarado (falso negativo de borde).")
    print("       interpolacion DECLARADA: Lagrange de 6 puntos en r*, pesos POR MALLA; error medido contra Lagrange de 8.")
    for k in (0, 1, 2):
        print("       nodos compartidos evaluacion vs malla %d = %d"
              % (k, contar_compartidos(set(Fraction(int(round(x * 10 ** 6)), 10 ** 6) for x in rs_e), ext[k])))
    for k in (0, 1, 2):
        print("       coherencia theta nivel %d: paso = 2^%d nodos gruesos | residuo relativo = %.3e | %s"
              % (k, k, coh_th[k], "OK" if coh_th[k] <= 1e-12 else "DEFECTO DEL MEDIDOR"))
    print()

    # ---- corridas ----
    celdas = {}

    def corre_terna(etiqueta, dato, orden_r=2, orden_th=2, nulo_ang=False):
        mall, sol = terna(args, dato, orden_r, orden_th, nulo_ang)
        Y = evalua(mall, sol, rs_e, args.nt0)
        e_interp = interp_metre(mall, sol, rs_e, args.nt0)
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
        dts, pasos = [], []
        for i, m in enumerate(mall):
            nsteps = int(math.ceil(args.T / m.dt_cota))
            dts.append(args.T / nsteps)
            pasos.append(nsteps)
            print("    nivel %d: nr=%d nt=%d dt=%.10e pasos=%d" % (m.nivel, m.nr, m.nt, args.T / nsteps, nsteps))
        print("    d1 = ||Psi_2h - Psi_h||_L2      = %.6e" % d1)
        print("    d2 = ||Psi_h  - Psi_h/2||_L2    = %.6e   (%.6f x piso v1 = %.6e)"
              % (d2, d2 / REF_PISO_F2, REF_PISO_F2))
        print("    razon d1/d2                     = %.6f   (esperado 2^p = %.4f para p = %.2f)"
              % (razon, 2.0 ** P_ESPERADO, P_ESPERADO))
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
        celda = {"etiqueta": etiqueta, "d1": d1, "d2": d2, "razon": razon, "p": p, "veredicto": veredicto,
                 "interp_ok": interp_ok, "e_interp": e_interp, "piso": piso, "max_abs": mx,
                 "nY": nY, "dt": dts, "pasos": pasos, "causa": causa, "p_rel": p_rel,
                 "d2_rel_piso_v1": d2 / REF_PISO_F2, "d2_rel_exacto_sonda": d2 / REF_D2_EXACTO}
        celdas[etiqueta] = celda
        return celda

    dato = lambda m: dato_2d(m, args.rc, args.sigma, args.tilt, args.mix4)
    r_principal = corre_terna("F2 PRINCIPAL", dato)

    dato_red = lambda m: dato_reducido(m, args.rc, args.sigma, args.tilt)
    r_reducido = corre_terna("C2 REDUCCION", dato_red)

    print("[C2] PAR DE DOMINIO (p reducido | p con angular vivo) = (%s | %s)"
          % ("NO MEDIBLE" if r_reducido["p"] is None else "%.6f" % r_reducido["p"],
             "NO MEDIBLE" if r_principal["p"] is None else "%.6f" % r_principal["p"]))
    print()

    r_c3a = corre_terna("C3a RADIAL ORDEN 1", dato, orden_r=1)
    r_c3b = corre_terna("C3b ANGULAR ORDEN 1", dato, orden_th=1)

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
    if max(coh_th) > 1e-12:
        rojos.append("coherencia theta de la malla de evaluacion (el interpolador lee otro tramo)")
    if not c6_paq:
        rojos.append("C6 contencion: la malla de evaluacion no cubre las coordenadas reales del paquete")
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

    veredicto_gate = "VERDE" if not rojos else "ROJO"

    print("[RESUMEN] nr0 = %d | arranque = Cauchy exacta | ventana = paquete" % args.nr0)
    print("   p(F2) = %s   veredicto = %s" % ("NO MEDIBLE" if r_principal["p"] is None
                                              else "%.6f" % r_principal["p"], r_principal["veredicto"]))
    print("   p(C2) = %s | p(C3a) = %s | p(C3b) = %s"
          % ("NO MEDIBLE" if r_reducido["p"] is None else "%.6f" % r_reducido["p"],
             "NO MEDIBLE" if r_c3a["p"] is None else "%.6f" % r_c3a["p"],
             "NO MEDIBLE" if r_c3b["p"] is None else "%.6f" % r_c3b["p"]))
    print("   rojos = %d %s" % (len(rojos), ("| " + " ; ".join(rojos)) if rojos else ""))
    print("   VEREDICTO GATE 2D-F2 = %s" % veredicto_gate)
    print("   T_UTC_FIN = %s | duracion = %.2f s" % (utc_now(), time.time() - t0))
    print("=" * 96)

    # ---- DELTA 3: escritor de crudo real ----
    if ruta_json:
        crudo = {
            "huella": HUELLA,
            "huella_v1_citada": HUELLA_V1,
            "huella_v2_citada": HUELLA_V2_CITADA,
            "hora_utc": utc_now(),
            "stamp": stamp,
            "identidad_self": ident,
            "comando": sys.argv,
            "arranque": "exacto: u^{-1} = u^0 + 0.5 dt^2 a(u^0), v = (u^0 - u^{-1})/dt",
            "deltas": SITIOS_CORREGIDOS,
            "transferencia": dt_info,
            "umbrales": {"p_esperado": P_ESPERADO, "umbral_p": UMBRAL_P, "cfl_sellado": CFL_SELLADO,
                         "c1_umbral_f3": UMBRAL_F3, "ref_piso_f2": REF_PISO_F2,
                         "ref_d2_exacto_sonda": REF_D2_EXACTO},
            "parametros": {"T": args.T, "nr0": args.nr0, "nt0": args.nt0, "rc": args.rc,
                           "sigma": args.sigma, "tilt": args.tilt, "mix4": args.mix4,
                           "modo_offset": args.modo_offset, "rs_min": args.rs_min, "rs_max": args.rs_max},
            "mallas": [{"nivel": m.nivel, "nr": m.nr, "nt": m.nt, "hr": m.hr, "delta": m.delta,
                        "dtheta": m.hth, "r_min": float(m.r[0]), "r_max": float(m.r[-1]),
                        "dt_cota": m.dt_cota} for m in mall_demo],
            "no_anidamiento": {"ratificado": {"compartidos_01_02_12": cuentas["ratificado"],
                                              "offsets": offs["ratificado"]},
                               "sellado": {"compartidos_01_02_12": cuentas["sellado"],
                                           "offsets": offs["sellado"]}},
            "cotejo_L2": cotejo,
            "c4": c4,
            "c5": {"T": front, "margen_min": marg, "ok": bool(marg > front)},
            "c6": {"banda_declarada": bandas["declarada"], "banda_paquete": bandas["paquete"],
                   "banda_entrante": bandas["entrante"], "cubre_declarada": c6_decl,
                   "cubre_paquete": c6_paq, "cubre_entrante": c6_ent, "tolerancia": dr_e},
            "ventana": {"lo": lo_e, "hi": hi_e, "rs_e_ini": float(rs_e[0]), "rs_e_fin": float(rs_e[-1]),
                        "nq": int(rs_e.size), "dr": dr_e, "n_theta": int(th_e.size),
                        "coherencia_theta": coh_th},
            "celdas": celdas,
            "veredicto": veredicto_gate,
            "rojos": rojos,
            "segundos": time.time() - t0,
        }
        with open(ruta_json, "w", encoding="utf-8") as fh:
            json.dump(crudo, fh, indent=1, sort_keys=True)
        with open(ruta_json, "rb") as fh:
            datos = fh.read()
        print("[CRUDO] %s | %d lineas | %d bytes | sha256 %s"
              % (ruta_json, datos.count(b"\n"), len(datos), hashlib.sha256(datos).hexdigest()))

    if args.stamp:
        print("[STAMP] crudo -> %s" % (ruta_json if ruta_json else "(sin --json: no se escribio crudo)"))

    if args.estricto and rojos:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
