#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ARNES DEL POTENCIAL DE ZERILLI (M > 0) EN TORTUGA CON CAPAS F11 -- GATE 2D-F3.

HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261013

PADRE (append-only, NO se edita): sim/PREREGISTRO_GATE_2D_F3_ZERILLI_CURVATURA_20261013.md
ERRATA 1 (sellada en git):       sim/ERRATA_1_PREREGISTRO_GATE_2D_F3_20261013.md
CASA (sellos que se REUTILIZAN, no se re-implementan):
  * sim/arnes_capa_absorbente_2d_f11.py  -> f11.geometria, f11.damp_de, f11.Medidor,
                                            f11.acumular, f11.rdb_de, f11.ventanas, f11.control_C3
  * sim/arnes_richardson_2d_f2_v3.py     -> f2.Malla2D, f2.d2r, f2.L2_theta, f2.dato_reducido

FISICA CONGELADA (dictamen del dueno 13-Oct-2026 + errata §R1-§R5). Donde §R difiere de §B del
padre, MANDA §R:
  * 2M = 3.0 (M = 1.5);  l = 2;  lambda = (l-1)(l+2)/2 = 2.
  * r*(r) = r + 2M ln(r/2M - 1);   r(r*) = 2M [1 + W0(e^{r*/(2M) - 1})]   (Lambert W0 ESTRICTA,
    sin scipy: Halley vectorizado en numpy; el arnes no hereda la muleta del padre §E.0).
  * Operador diagonal (D2 / §R2):  U(r) = V_Zerilli(r) - (1 - 2M/r) * l(l+1)/r^2.
  * Peso angular (D2 / §R2): (1 - 2M/r)/r^2.  Con M = 0 vale exactamente 1/r^2, que es el peso
    sellado de F11 -> mismo operador, bit a bit. El factor metrico es la UNICA linea nueva del
    sector angular y la exige la resolucion; el total -f(1/r^2)L^2 - U = -V_Z coincide con la
    ecuacion de Zerilli estandar.
  * Capa F11 REUTILIZADA VERBATIM: n = 3, A = 25.0, L_frac = 0.25, ancho = 96.0,
    r*_sponge = 74.0, r* en [2.0, 98.0]. No se re-implementa un solo perfil.
  * Malla: la MISMA de F11 (nr0 = 384, nt0 = 33, CFL = 0.50, hr = 0.2506527415143603,
    dt_cota = 0.045706499624780135) via f2.Malla2D nivel 0.
    NOTA DECLARADA: dt_cota se toma con f = 1 (el de F11). Como f <= 1 en todo el dominio
    (r > 2M), el paso angular efectivo es <= el plano: el dt sellado es CONSERVADOR y no se
    recalcula la cota.
  * Arranque de Cauchy (misma familia que F11/F2): u^{-1} = u^0 - dt v^0 + 0.5 dt^2 a(u^0).
  * Dato de C2 (D5 / §R5): paquete gaussiano CON REPOSO INICIAL (v^0 = 0) centrado en r* = 10.0,
    sigma = 2.0, con contenido angular l = 2 EXACTO: u^0 = env(r*) * P_2(cos theta).
    El dato de F11 (saliente puro, theta-independiente) NO se reutiliza: era vacuo (D5).

MEDIDOR: REUTILIZADO VERBATIM de F11 (f11.Medidor / f11.acumular / f11.rdb_de / f11.ventanas).
  R_dB = 10 log10(E_vuelta / E_sal) EN ENERGIA; umbral HEREDADO -40.0 dB (no se mueve).
  El factor geometrico del medidor es r*^2 (el de F11), no r^2; se DECLARA: es constante en el
  anillo y cancela en la razon, que es lo unico que se mide. No se repara.

LO QUE ESTE ARNES DECLARA Y **NO** REPARA (defectos de la ORDEN hallados al implementar; se
imprimen con su cifra y su causa, y NO mueven ningun umbral):
  D6  C7 (eco prematuro). La banda sellada de F11 [r*_min, c_esponja - 6 sigma] = [2.0, 14.0]
      CONTIENE el dato de C2 (centrado en 10.0, soporte +-6 sigma = [-2.0, 22.0]): el ratio mide
      el propio dato, no un eco. Medida contra la banda del dato sale [r*_min, r*_dato - 6 sigma]
      = [2.0, -2.0] = VACIA. Familia D5: control que no puede diferir. C7 se reporta y NO entra
      en el veredicto hasta que el dueno lo adjudique.
  D7  El dato tiene DOS mitades. La mitad ENTRANTE choca con la pared interior Dirichlet
      (r* = 2.0) y regresa: su arribo al anillo testigo (t ~ 56.1) cae en la ventana MUERTA, y su
      propia reflexion de esponja (t ~ 91.9) cae DENTRO de la ventana de VUELTA. Cronologia
      analitica impresa + E_muerta medido. NO se re-ventanea ni se repara.

UNIVERSO DECLARADO: unicamente la malla sellada de F11 (r* en [2.0, 98.0], nr0 = 384, nt0 = 33),
el mapa tortuga con 2M = 3.0 sobre esa malla, el dato de C2 y las cifras analiticas de V_Z/U.
Fuera: mallas mas finas (eso es C5, no ordenado), horizonte, r* < 2.0, y toda re-base de la
geometria sellada.
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
import arnes_capa_absorbente_2d_f11 as f11

# --------------------------------------------------------------------------------------------
# Identidad de la pieza
# --------------------------------------------------------------------------------------------

HUELLA = "HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261013"
HUELLA_PREREGISTRO = "HUELLA-PREREGISTRO-GATE-2D-F3-ZERILLI-CURVATURA-20261013"
HUELLA_ERRATA = "HUELLA-ERRATA-1-PREREGISTRO-GATE-2D-F3-20261013"
HUELLA_F11 = "HUELLA-ARNES-CAPA-ABSORBENTE-2D-F11-20261013"
HUELLA_V3 = "HUELLA-ARNES-RICHARDSON-2D-F2-V3-20261013"
PREREGISTRO = "sim/PREREGISTRO_GATE_2D_F3_ZERILLI_CURVATURA_20261013.md"
ERRATA = "sim/ERRATA_1_PREREGISTRO_GATE_2D_F3_20261013.md"
ARNES_F11 = "sim/arnes_capa_absorbente_2d_f11.py"
ARNES_V3 = "sim/arnes_richardson_2d_f2_v3.py"

# --------------------------------------------------------------------------------------------
# Sellos (inmutables)
# --------------------------------------------------------------------------------------------

L_ANGO = 2                              # l = 2 sellado
LAM_Z = 2.0                             # lambda = (l-1)(l+2)/2  (D1 ratificado)
DOSM = 3.0                              # 2M = 3.0  (D3 ratificado); M = 1.5
RS0 = 10.0                              # centro del dato de C2 (D5 ratificado)
CFL_SELLADO = 0.50
ANCHO = 96.0
RS_MIN = 2.0
L_FRAC = 0.25
N_PERFIL = 3
A_ESPONJA = 25.0
SIGMA = 2.0
NR0 = 384
NT0 = 33
UMBRAL_R_DB = -40.0                     # EN ENERGIA (heredado de F11, no se mueve)
UMBRAL_C0_U = 1e-14
UMBRAL_C0_DIFF = 1e-13
UMBRAL_C1 = 1e-12
UMBRAL_C4 = 1e-13
UMBRAL_C6 = 1e-12
UMBRAL_C7 = 1e-2
UMBRAL_C9 = 1e-13
RS_REF_PICO = 2.851374906561190         # referencia SELLADA (errata §R3, 2M = 3.0)
R_REF_PICO = 4.648185966305973          # = 1.549395322101991 * 3 (ley de escala del padre)
LAMINAS_DECLARADAS = [
    "2M = 3.0, l = 2, lambda = 2",
    "U(r) = V_Zerilli(r) - (1 - 2M/r) * 6/r^2",
    "peso angular (1 - 2M/r)/r^2",
    "capa F11 verbatim (n=3, A=25.0, L_frac=0.25, ancho=96.0)",
    "malla sellada nr0=384 nt0=33 CFL=0.50 (f2.Malla2D nivel 0)",
    "dato de C2: gaussiana en r*-10 con sigma=2 y P_2(cos theta), v^0 = 0",
    "medidor, ventanas, acumulacion y R_dB verbatim de F11",
]

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
# Mapa tortuga: r*(r) y su inversa r(r*) por Lambert W0 (Halley, numpy puro, sin scipy)
# --------------------------------------------------------------------------------------------


def lambert_w0(z, n_iter=80):
    """Rama principal W0(z) por iteracion de Halley, vectorizada.

    Dominio de uso garantizado: z = exp(r*/(2M) - 1) con r* >= r*_min = 2.0 y 2M = 3.0
    => z >= exp(-1/3) = 0.7165. Nunca se toca z <= -1/e ni w -> -1.
    """
    z = np.asarray(z, dtype=float)
    w = np.log1p(z)
    for _ in range(int(n_iter)):
        ew = np.exp(w)
        f = w * ew - z
        wp1 = w + 1.0
        den = ew * wp1 - (w + 2.0) * f / (2.0 * wp1)
        w = w - f / den
    return w


def r_de_rs(rs, dosM):
    """r(r*) = 2M [1 + W0(e^{r*/(2M) - 1})].  Con 2M = 0 es la identidad (modo plano)."""
    rs = np.asarray(rs, dtype=float)
    if dosM == 0.0:
        return rs.copy()
    return dosM * (1.0 + lambert_w0(np.exp(rs / dosM - 1.0)))


def rs_de_r(r, dosM):
    """r*(r) = r + 2M ln(r/2M - 1).  Con 2M = 0 es la identidad."""
    r = np.asarray(r, dtype=float)
    if dosM == 0.0:
        return r.copy()
    return r + dosM * np.log(r / dosM - 1.0)


def punto_fijo_desnudo(rs_val, dosM, r0, n_iter=60):
    """Control NEGATIVO declarado: r_{k+1} = r* - 2M ln(r_k/2M - 1) NO contrae.

    |g'(r)| = 2M/(r - 2M) < 1 <=> r > 4M.  Como 4M = 6.0 > r*_min = 2.0, en el borde interior
    el punto fijo desnudo diverge: por eso el arnes usa Lambert W0 y no la iteracion directa.
    Se devuelve la traza (no se usa como solver).
    """
    r = float(r0)
    traza = []
    for _ in range(int(n_iter)):
        try:
            r = float(rs_val) - dosM * math.log(r / dosM - 1.0)
        except ValueError:
            traza.append(float("nan"))
            break
        traza.append(r)
    return traza


# --------------------------------------------------------------------------------------------
# Potencial de Zerilli y operador diagonal
# --------------------------------------------------------------------------------------------


def vz_de_r(r, dosM, lam=LAM_Z):
    """V_Zerilli(r) = (1 - 2M/r) [2 lam^2 (lam+1) r^3 + 6 lam^2 M r^2 + 18 lam M^2 r + 18 M^3]
                       / [ r^3 (lam r + 3M)^2 ].

    Se evalua SIEMPRE la formula general, tambien en M = 0: el cero analitico de
    U(M=0) queda entonces como un cero DE MAQUINA de la resta (errata §F, 4.440892e-16),
    y ese es justamente lo que C0 mide.  No se especializa el limite.
    """
    r = np.asarray(r, dtype=float)
    M = 0.5 * float(dosM)
    num = (2.0 * lam ** 2 * (lam + 1.0) * r ** 3
           + 6.0 * lam ** 2 * M * r ** 2
           + 18.0 * lam * M ** 2 * r
           + 18.0 * M ** 3)
    den = r ** 3 * (lam * r + 3.0 * M) ** 2
    return (1.0 - float(dosM) / r) * num / den


def vz_complejo(r, dosM, lam=LAM_Z):
    """Version compleja de V_Z (para la derivada por PASO COMPLEJO de C1a)."""
    r = np.asarray(r, dtype=complex)
    M = 0.5 * float(dosM)
    num = (2.0 * lam ** 2 * (lam + 1.0) * r ** 3
           + 6.0 * lam ** 2 * M * r ** 2
           + 18.0 * lam * M ** 2 * r
           + 18.0 * M ** 3)
    den = r ** 3 * (lam * r + 3.0 * M) ** 2
    return (1.0 - float(dosM) / r) * num / den


def u_de_r(r, dosM, l=L_ANGO):
    """Operador diagonal D2/§R2:  U(r) = V_Zerilli(r) - (1 - 2M/r) l(l+1)/r^2."""
    r = np.asarray(r, dtype=float)
    return vz_de_r(r, dosM) - (1.0 - float(dosM) / r) * (l * (l + 1.0)) / r ** 2


def campos_de_malla(m, dosM, l=L_ANGO):
    """Devuelve (r_nodos, f_nodos, U_nodos, w_ang_nodos) sobre la malla sellada (en r*).

    r_nodos = r(r*) por Lambert W0;  f = 1 - 2M/r;  U = V_Z - f*l(l+1)/r^2;
    w_ang = f/r^2  (peso angular metrico; con M = 0 vale 1/r^2, el sellado de F11).
    """
    r = r_de_rs(m.rs, dosM)
    f = 1.0 - float(dosM) / r
    pot = vz_de_r(r, dosM) - f * (l * (l + 1.0)) / r ** 2
    wang = f / r ** 2
    return r, f, pot, wang


# --------------------------------------------------------------------------------------------
# Dato de C2 (D5): gaussiana con reposo inicial y contenido l = 2 exacto
# --------------------------------------------------------------------------------------------


def perfil_p2(th):
    """P_2(cos theta) = (3 cos^2 theta - 1)/2: contenido angular l = 2, m = 0."""
    c = np.cos(np.asarray(th, dtype=float))
    return 0.5 * (3.0 * c * c - 1.0)


def dato_f3(m, rs0, sigma, amp=1.0):
    """u^0(r*,theta) = amp * exp(-(r*-rs0)^2/(2 sigma^2)) * P_2(cos theta)."""
    env = float(amp) * np.exp(-(m.rs - float(rs0)) ** 2 / (2.0 * float(sigma) ** 2))
    return env[:, None] * perfil_p2(m.th)[None, :]


def dato_reducido_m0(m, rs0, sigma):
    """Dato theta-independiente (l = 0 radial): la familia que usa el C0 de F11."""
    return f2.dato_reducido(m, float(rs0), float(sigma), 0.35)


# --------------------------------------------------------------------------------------------
# Operador e integrador curvos (misma aritmetica de flujo que F11; unica linea nueva: pot y wang)
# --------------------------------------------------------------------------------------------


def acel_f3(m, u, pot=None, wang=None, orden_r=2, orden_th=2, nulo_ang=False):
    """a = d2r(u) - w_ang * L2_theta(u) - U * u  (DEVIACION DECLARADA del f2.acel plano).

    La unica diferencia con f2.acel es (i) el peso angular metrico wang (f/r^2) y (ii) el
    termino diagonal -U(r*)u.  Con dosM = 0: f = 1.0 exacto, wang = m.w_ang bit a bit y
    pot = cero de maquina => el operador se reduce al sellado y C0 lo mide.
    """
    a = f2.d2r(u, m.hr, orden_r)
    if not nulo_ang:
        w = m.w_ang if wang is None else wang
        a = a - w[:, None] * f2.L2_theta(u, m.th, m.hth, orden_th)
    if pot is not None:
        a = a - pot[:, None] * u
    return a


def simula_f3(m, u0, v0, damp, nsteps, dt, pot=None, wang=None, sonda=None):
    """Leapfrog escalonado con amortiguamiento, espejo de f11.simula_amortiguado.

    Arranque de Cauchy identico al de F11: u^{-1} = u^0 - dt v^0 + 0.5 dt^2 a(u^0).
    Con v^0 = 0 coincide con el arranque de v3.  Las filas extremas se fuerzan a 0.
    """
    u = np.array(u0, dtype=float, copy=True)
    u[0, :] = 0.0
    u[-1, :] = 0.0
    a0 = acel_f3(m, u, pot, wang)
    u_m1 = u - dt * v0 + 0.5 * dt * dt * a0
    u_m1[0, :] = 0.0
    u_m1[-1, :] = 0.0
    v = (u - u_m1) / dt
    for k in range(int(nsteps)):
        v = damp * v + dt * acel_f3(m, u, pot, wang)
        u = u + dt * v
        u[0, :] = 0.0
        u[-1, :] = 0.0
        if sonda is not None:
            sonda(k + 1, u, v)
    return u


# --------------------------------------------------------------------------------------------
# C0 -- limite plano: U(M = 0) ~ 0 y reduccion al arnes certificado F11
# --------------------------------------------------------------------------------------------


def control_C0(nr0=96, nt0=NT0, pasos_a=40, pasos_b=1200):
    m = f2.Malla2D(RS_MIN, RS_MIN + ANCHO, int(nr0), int(nt0), CFL_SELLADO, 0)
    dt = float(m.dt_cota)
    r_nod, f_nod, pot0, wang0 = campos_de_malla(m, 0.0)
    max_u = float(np.max(np.abs(pot0)))
    g = f11.geometria(RS_MIN, ANCHO, L_FRAC, N_PERFIL, A_ESPONJA)
    damp = f11.damp_de(m.rs, g, dt)[:, None]
    unos = np.ones((m.nr, 1))

    # (a) familia C0 de F11: dato reducido l = 0, esponja APAGADA, 40 pasos
    u0a = dato_reducido_m0(m, 22.0, SIGMA)
    v0a = np.zeros_like(u0a)
    ref_a = f11.simula_amortiguado(m, u0a, v0a, unos, int(pasos_a), dt, 2, 2, False, None)
    got_a = simula_f3(m, u0a, v0a, unos, int(pasos_a), dt, pot0, wang0, None)
    dif_a = float(np.max(np.abs(got_a - ref_a)))

    # (b) dato de F3 (l = 2), esponja ENCENDIDA, 1200 pasos
    u0b = dato_f3(m, RS0, SIGMA)
    v0b = np.zeros_like(u0b)
    ref_b = f11.simula_amortiguado(m, u0b, v0b, damp, int(pasos_b), dt, 2, 2, False, None)
    got_b = simula_f3(m, u0b, v0b, damp, int(pasos_b), dt, pot0, wang0, None)
    dif_b = float(np.max(np.abs(got_b - ref_b)))

    ok = bool(max_u <= UMBRAL_C0_U and dif_a <= UMBRAL_C0_DIFF and dif_b <= UMBRAL_C0_DIFF)
    causa = ("U(M=0) = %.6e <= %.0e : %s | diff vs F11 (a, l=0, sin esponja, %d pasos) = %.6e | "
             "diff vs F11 (b, l=2, con esponja, %d pasos) = %.6e <= %.0e : %s"
             % (max_u, UMBRAL_C0_U, "PASA" if max_u <= UMBRAL_C0_U else "ROJO",
                int(pasos_a), dif_a, int(pasos_b), dif_b, UMBRAL_C0_DIFF,
                "PASA" if max(dif_a, dif_b) <= UMBRAL_C0_DIFF else "ROJO"))
    return {
        "control": "C0",
        "que": "limite plano M = 0: el operador diagonal U es cero de maquina y la evolucion "
               "se reduce AL ARNES CERTIFICADO F11",
        "universo": "malla nr0=%d nt0=%d nivel 0 | %d y %d pasos | dato (a) l=0 en r*=22.0, "
                    "dato (b) l=2 en r*=%.1f" % (int(nr0), int(nt0), int(pasos_a), int(pasos_b), RS0),
        "max_abs_U_M0": max_u,
        "umbral_U": UMBRAL_C0_U,
        "diff_a_l0_sin_esponja": dif_a,
        "diff_b_l2_con_esponja": dif_b,
        "umbral_diff": UMBRAL_C0_DIFF,
        "dt": dt,
        "causa": causa,
        "ok": ok,
        "rc": 0 if ok else 1,
    }


# --------------------------------------------------------------------------------------------
# C1a -- pico analitico continuo (dos metodos independientes, sin scipy)
# --------------------------------------------------------------------------------------------


def raiz_pico_metodo_A(dosM, n_barrido=400001):
    """Raiz de dV_Z/dr por Newton-biseccion con derivada de PASO COMPLEJO (h = 1e-20).

    El paso complejo NO resta: Im[V_Z(x + i h)]/h = dV_Z/dx con precision de maquina.
    Se listan TODOS los cambios de signo del barrido (el conteo se imprime).
    """
    h = 1e-20
    xs = np.linspace(float(dosM) * (1.0 + 1e-9), 200.0 * float(dosM), int(n_barrido))
    d = np.imag(vz_complejo(xs.astype(complex) + 1j * h, dosM)).astype(float) / h

    def dv(x):
        return float(np.imag(vz_complejo(complex(float(x), h), dosM))) / h

    idx = np.nonzero(np.sign(d[:-1]) != np.sign(d[1:]))[0]
    raices = []
    for i in idx:
        a, b = float(xs[i]), float(xs[i + 1])
        fa = dv(a)
        for _ in range(200):
            mid = 0.5 * (a + b)
            if mid <= a or mid >= b:
                break
            fm = dv(mid)
            if fm == 0.0:
                a = b = mid
                break
            if (fa < 0.0) == (fm < 0.0):
                a, fa = mid, fm
            else:
                b = mid
        raices.append(0.5 * (a + b))
    return raices, int(idx.size), float(xs[0]), float(xs[-1])


def raiz_pico_metodo_B(dosM):
    """Raices del numerador POLINOMICO EXACTO de dV_Z/dr (numpy.roots).

    V_Z = (r-2M) N / (r D);  V_Z' = (A'B - A B')/B^2 con A = (r-2M)N, B = r D.
    Se devuelven las raices reales con r > 2M, ordenadas por V_Z descendente.
    """
    lam, M = LAM_Z, 0.5 * float(dosM)
    Nc = np.array([2.0 * lam ** 2 * (lam + 1.0), 6.0 * lam ** 2 * M,
                   18.0 * lam * M ** 2, 18.0 * M ** 3])
    unor = np.array([1.0, 0.0, 0.0, 0.0])
    l3m = np.array([lam, 3.0 * M])
    Dc = np.polymul(np.polymul(unor, l3m), l3m)
    A = np.polymul(np.array([1.0, -float(dosM)]), Nc)
    B = np.polymul(np.array([1.0, 0.0]), Dc)
    P = np.polyadd(np.polymul(np.polyder(A), B), -np.polymul(A, np.polyder(B)))
    rr = np.roots(P)
    buenas = [float(z.real) for z in rr
              if abs(z.imag) <= 1e-9 * abs(z.real) and z.real > float(dosM) * (1.0 + 1e-9)]
    buenas.sort(key=lambda x: -float(vz_de_r(np.array([x]), dosM)[0]))
    return buenas, int(len(rr)), P


def control_C1a(dosM=DOSM, ref=RS_REF_PICO):
    raA, n_cambios, lo, hi = raiz_pico_metodo_A(dosM)
    raB, n_raices, _P = raiz_pico_metodo_B(dosM)
    if not raA or not raB:
        return {"control": "C1a", "ok": False, "rc": 1,
                "causa": "sin raiz real en el barrido (A: %d, B: %d)" % (len(raA), len(raB))}
    rA = max(raA, key=lambda x: float(vz_de_r(np.array([x]), dosM)[0]))
    rB = float(raB[0])
    rsA = float(rs_de_r(np.array([rA]), dosM)[0])
    rsB = float(rs_de_r(np.array([rB]), dosM)[0])
    dA, dB, dAB = abs(rsA - ref), abs(rsB - ref), abs(rsA - rsB)
    ok = bool(dA <= UMBRAL_C1 and dB <= UMBRAL_C1 and dAB <= UMBRAL_C1)
    causa = ("|r*_A - ref| = %.6e | |r*_B - ref| = %.6e | |r*_A - r*_B| = %.6e <= %.0e : %s "
             "(ref sellada = %.15f; cambios de signo del barrido = %d; raices reales del "
             "polinomio = %d)"
             % (dA, dB, dAB, UMBRAL_C1, "PASA" if ok else "ROJO", ref, n_cambios, n_raices))
    return {
        "control": "C1a",
        "que": "pico analitico continuo: raiz de dV_Z/dr* = 0 por DOS metodos independientes",
        "universo": "A: barrido %.3f..%.3f (400001 puntos) + biseccion 200 | B: raices del "
                    "numerador polinomico exacto (numpy.roots)" % (lo, hi),
        "metodo_A_paso_complejo_r": rA,
        "metodo_B_polinomio_r": rB,
        "r_star_A": rsA,
        "r_star_B": rsB,
        "r_star_ref_sellada": float(ref),
        "dif_A_ref": dA,
        "dif_B_ref": dB,
        "dif_A_B": dAB,
        "umbral": UMBRAL_C1,
        "n_cambios_signo": n_cambios,
        "n_raices_polinomio": n_raices,
        "vz_en_pico_A": float(vz_de_r(np.array([rA]), dosM)[0]),
        "r_ref_escala": R_REF_PICO,
        "causa": causa,
        "ok": ok,
        "rc": 0 if ok else 1,
    }


# --------------------------------------------------------------------------------------------
# C1b -- pico discreto: el argmax de rejilla debe caer a media celda del pico teorico
# --------------------------------------------------------------------------------------------


def control_C1b(dosM=DOSM, ref=RS_REF_PICO, nr0=NR0, nt0=NT0):
    m = f2.Malla2D(RS_MIN, RS_MIN + ANCHO, int(nr0), int(nt0), CFL_SELLADO, 0)
    r = r_de_rs(m.rs, dosM)
    vz = vz_de_r(r, dosM)
    i = int(np.argmax(vz))
    rsg = float(m.rs[i])
    tol = 0.5 * float(m.hr)
    d = abs(rsg - ref)
    ok = bool(d <= tol)
    causa = "|r*_rejilla_max - r*_teorico| = %.6e <= 0.5 hr = %.6e : %s" % (
        d, tol, "PASA" if ok else "ROJO")
    return {
        "control": "C1b",
        "que": "pico discreto: argmax de V_Z sobre la malla sellada a media celda del teorico",
        "universo": "malla nr0=%d nt0=%d nivel 0 (hr = %.16f)" % (int(nr0), int(nt0), float(m.hr)),
        "r_star_rejilla_max": rsg,
        "r_star_teorico": float(ref),
        "r_en_rejilla": float(r[i]),
        "vz_max_rejilla": float(vz[i]),
        "hr": float(m.hr),
        "tol_media_celda": tol,
        "dif": d,
        "causa": causa,
        "ok": ok,
        "rc": 0 if ok else 1,
    }


# --------------------------------------------------------------------------------------------
# C9 -- ida y vuelta del mapa tortuga (Lambert W0) + control negativo del punto fijo desnudo
# --------------------------------------------------------------------------------------------


def control_C9(dosM=DOSM, n=200001, ref_pf=RS_MIN):
    g = np.linspace(RS_MIN, RS_MIN + ANCHO, int(n))
    r = r_de_rs(g, dosM)
    back = rs_de_r(r, dosM)
    err = float(np.max(np.abs(back - g)))
    z = np.exp(g / dosM - 1.0)
    w = lambert_w0(z)
    ident = float(np.max(np.abs(dosM * (1.0 + w + np.log(w)) - g)))
    m = f2.Malla2D(RS_MIN, RS_MIN + ANCHO, NR0, NT0, CFL_SELLADO, 0)
    r_nod = r_de_rs(m.rs, dosM)
    err_nodos = float(np.max(np.abs(rs_de_r(r_nod, dosM) - m.rs)))
    traza = punto_fijo_desnudo(ref_pf, dosM, 0.5 * (RS_MIN + 4.0 * dosM / 3.0), 60)
    finito = [x for x in traza if x == x]
    err_pf = abs(finito[-1] - float(r_de_rs(np.array([ref_pf]), dosM)[0])) if finito else float("nan")
    ok = bool(err <= UMBRAL_C9)
    causa = ("max |r*(r(r*)) - r*| = %.6e <= %.0e : %s (n = %d puntos) | identidad analitica "
             "2M(1+W+lnW) = r*: %.6e | nodos de la malla: %.6e | punto fijo desnudo en r* = %.1f "
             "tras 60 pasos: r = %.6f (err %.3e) => NO contrae, Lambert W0 es obligatoria"
             % (err, UMBRAL_C9, "PASA" if ok else "ROJO", int(n), ident, err_nodos,
                float(ref_pf), (finito[-1] if finito else float("nan")), err_pf))
    return {
        "control": "C9",
        "que": "ida y vuelta del mapa tortuga r* -> r -> r* con Lambert W0 estricta",
        "universo": "%d puntos uniformes en r* en [%.1f, %.1f] + los %d nodos de la malla "
                    "sellada" % (int(n), RS_MIN, RS_MIN + ANCHO, m.nr),
        "err_max_ida_vuelta": err,
        "err_max_identidad_analitica": ident,
        "err_max_nodos_malla": err_nodos,
        "umbral": UMBRAL_C9,
        "punto_fijo_desnudo_r": (finito[-1] if finito else float("nan")),
        "punto_fijo_desnudo_err": err_pf,
        "r_star_sonda_punto_fijo": float(ref_pf),
        "causa": causa,
        "ok": ok,
        "rc": 0 if ok else 1,
    }


# --------------------------------------------------------------------------------------------
# C2 -- la corrida: dispersion por U(r*) + absorcion en la capa F11 exterior
# --------------------------------------------------------------------------------------------


def residuo_no_p2(u, th, p2, sinth, den):
    """Norma relativa L2(theta) (medida sin(theta) dtheta) de la parte NO-P_2 de cada fila."""
    a = (u * p2[None, :] * sinth[None, :]).sum(axis=1) / den
    res = u - a[:, None] * p2[None, :]
    num = np.sqrt(np.sum(res * res * sinth[None, :], axis=1))
    d2 = np.sqrt(np.sum(u * u * sinth[None, :], axis=1))
    msk = d2 > 0.0
    if not np.any(msk):
        return 0.0
    return float(np.max(num[msk] / d2[msk]))


def corrida_c2(m, g, g_win, dt, nsteps, encender, pot, wang, rs0, sigma, capturas=()):
    ip = int(np.argmin(np.abs(m.rs - g["p"])))
    p_eff = float(m.rs[ip])
    vw = f11.ventanas(g_win, p_eff, sigma, g["rs_min"], g["rs_max"])
    filas = np.nonzero(m.rs <= g["c"] - 6.0 * sigma)[0]
    damp = f11.damp_de(m.rs, g, dt)[:, None] if encender else np.ones((m.nr, 1))
    u0 = dato_f3(m, rs0, sigma)
    v0 = np.zeros_like(u0)
    caps = {}
    pedidos = set(int(x) for x in capturas)
    med = f11.Medidor(m, ip, m.hr, m.th, m.hth, filas, ())

    def sonda(k, u, v):
        med(k, u, v)
        if k in pedidos:
            caps[int(k)] = u.copy()

    u = simula_f3(m, u0, v0, damp, int(nsteps), dt, pot, wang, sonda)
    acc = f11.acumular(med, dt, vw["t_a"], vw["t_ret"])
    rdb = f11.rdb_de(acc)
    return {"u": u, "u0": u0, "med": med, "acc": acc, "rdb": rdb, "ip": ip, "p_eff": p_eff,
            "ventanas": vw, "filas_testigo": filas, "caps": caps, "dt": dt,
            "nsteps": int(nsteps), "encender": bool(encender), "damp": damp}


def control_C4(m, g, dt, pot, wang, res_on, res_off, pasos):
    """Pureza del interior util: ON vs OFF con el MISMO dt deben coincidir en r* < r*_sponge."""
    interior = m.rs < g["rs_sponge"]
    detalles = []
    peor = 0.0
    for k in pasos:
        kk = int(k)
        if kk not in res_on["caps"] or kk not in res_off["caps"]:
            detalles.append({"paso": kk, "t": kk * dt, "medido": False})
            continue
        a = res_on["caps"][kk]
        b = res_off["caps"][kk]
        d = float(np.max(np.abs(a[interior, :] - b[interior, :])))
        peor = max(peor, d)
        detalles.append({"paso": kk, "t": kk * dt, "medido": True, "dif_interior": d})
    ok = bool(peor <= UMBRAL_C4)
    causa = ("max |u_ON - u_OFF| en r* < r*_sponge = %.6e <= %.0e : %s (pasos %s)"
             % (peor, UMBRAL_C4, "PASA" if ok else "ROJO", str([int(x) for x in pasos])))
    return {
        "control": "C4",
        "que": "pureza del interior util: la esponja NO contamina el interior (ON vs OFF, mismo dt)",
        "universo": "filas con r* < r*_sponge = %.1f (%d de %d filas) en los pasos de captura"
                    % (g["rs_sponge"], int(np.count_nonzero(interior)), m.nr),
        "detalles": detalles,
        "dif_max_interior": peor,
        "umbral": UMBRAL_C4,
        "causa": causa,
        "ok": ok,
        "rc": 0 if ok else 1,
    }


def control_C6(m, dosM, pot, wang, u0, p2, sinth, den):
    """C6 REDEFINIDO para l = 2 (padre §D): U no puede romper m.

    (i) el operador diagonal U(r*) es theta-independiente por construccion: su dispersion en
        theta es 0.0 exacto;
    (ii) el termino que U agrega a la aceleracion, delta = a_con_U(u0) - a_sin_U(u0) = -U u0,
        debe ser PROPORCIONAL a P_2 (componente no-P_2 <= 1e-12). Si alguien implementara un U
        con dependencia angular, este control lo caza.
    (iii) INFORMATIVO (no criterio): el piso del metro angular, residuo no-P_2 de L2_theta(P_2).
    """
    pot2d = np.repeat(pot[:, None], m.nt, axis=1)
    spread = float(np.max(pot2d.max(axis=1) - pot2d.min(axis=1)))
    a_con = acel_f3(m, u0, pot, wang)
    a_sin = acel_f3(m, u0, None, wang)
    delta = a_con - a_sin
    rel_delta = residuo_no_p2(delta, m.th, p2, sinth, den)
    l2p2 = f2.L2_theta(np.repeat(p2[None, :], 3, axis=0), m.th, m.hth, 2)[1:2, :]
    rel_l2 = residuo_no_p2(np.repeat(l2p2, m.nr, axis=0), m.th, p2, sinth, den)
    ok = bool(spread == 0.0 and rel_delta <= UMBRAL_C6)
    causa = ("dispersion theta de U = %.1e (esperado 0.0) | componente no-P_2 de -U u0 = %.6e "
             "<= %.0e : %s | PISO del metro angular (no-P_2 de L2 P_2) = %.6e (informativo)"
             % (spread, rel_delta, UMBRAL_C6, "PASA" if ok else "ROJO", rel_l2))
    return {
        "control": "C6",
        "que": "invariancia angular REDEFINIDA para l = 2: U(r*) no puede romper m",
        "universo": "operador 2D de la malla sellada (nr0=%d, nt0=%d) y el dato de C2" % (m.nr, m.nt),
        "dispersion_theta_U": spread,
        "residuo_no_P2_de_delta_a": rel_delta,
        "piso_metro_angular_no_P2_de_L2P2": rel_l2,
        "umbral": UMBRAL_C6,
        "causa": causa,
        "ok": ok,
        "rc": 0 if ok else 1,
    }


def cronologia(g, p_eff, rs0, sigma, ancho_extra=6.0):
    """Cronologia analitica de las DOS mitades del dato (D7). Unidades de r* = unidades de t."""
    rs_min, rs_sp = g["rs_min"], g["rs_sponge"]
    a = ancho_extra * sigma
    return {
        "dato_centro": rs0,
        "dato_soporte_6sigma": [rs0 - a, rs0 + a],
        "pared_interna": rs_min,
        "anillo_testigo_p_eff": p_eff,
        "esponja": rs_sp,
        # mitad SALIENTE (hacia la esponja)
        "T_centro_saliente_en_anillo": p_eff - rs0,
        "T_centro_saliente_en_esponja": rs_sp - rs0,
        "T_retorno_saliente_en_anillo": (rs_sp - rs0 - a) + (rs_sp - p_eff),
        # mitad ENTRANTE (hacia la pared interna Dirichlet)
        "T_centro_entrante_en_pared": rs0 - rs_min,
        "T_centro_entrante_en_anillo": (rs0 - rs_min) + (p_eff - rs_min),
        "T_frente_entrante_en_anillo": (rs0 - rs_min) + (p_eff - rs_min) - a,
        "T_centro_eco_pared_en_esponja": (rs0 - rs_min) + (p_eff - rs_min) + (rs_sp - p_eff),
        "T_retorno_eco_pared_en_anillo": (rs0 - rs_min) + (p_eff - rs_min) + 2.0 * (rs_sp - p_eff),
        "T_frente_eco_pared_en_anillo": (rs0 - rs_min) + (p_eff - rs_min) - a + 2.0 * (rs_sp - p_eff),
    }


def control_C7(med, max_inc, m, g, rs0, sigma, umbral=UMBRAL_C7):
    """C7 con su defecto DECLARADO (D6). No entra en el veredicto hasta dictamen del dueno."""
    eco = float(np.max(med.eco)) if med.eco else 0.0
    filas_selladas = np.nonzero(m.rs <= g["c"] - 6.0 * sigma)[0]
    b_lo, b_hi = float(m.rs[filas_selladas[0]]) if filas_selladas.size else float("nan"), \
        float(m.rs[filas_selladas[-1]]) if filas_selladas.size else float("nan")
    lim_dato = float(rs0) - 6.0 * sigma
    ratio_sellada = (eco / max_inc) if max_inc > 0.0 else None
    return {
        "control": "C7",
        "que": "eco prematuro en la banda de testigos (herencia F11)",
        "aplicable": False,
        "entra_en_veredicto": False,
        "banda_sellada_r": [b_lo, b_hi],
        "banda_del_dato_r": [float(g["rs_min"]), lim_dato],
        "banda_del_dato_vacia": bool(lim_dato <= float(g["rs_min"])),
        "eco_max_medido": eco,
        "max_inc": max_inc,
        "ratio_banda_sellada": ratio_sellada,
        "umbral": umbral,
        "causa": ("D6 DECLARADO: la banda sellada [%.1f, %.1f] CONTIENE el dato de C2 (centrado "
                  "en %.1f, soporte +-6 sigma = [%.1f, %.1f]); el maximo de la banda es el propio "
                  "dato. Medida contra la banda del dato sale [%.1f, %.1f] = %s. Control que no "
                  "puede diferir (familia D5): se reporta la cifra y NO se adjudica."
                  % (b_lo, b_hi, rs0, rs0 - 6.0 * sigma, rs0 + 6.0 * sigma,
                     float(g["rs_min"]), lim_dato,
                     "VACIA" if lim_dato <= float(g["rs_min"]) else "NO VACIA")),
        "ok": None,
        "rc": None,
    }


def control_C8(m, g, p_eff, sigma):
    """Informativo (leccion F11): el anillo debe estar a mas de 6 sigma de la pared interna."""
    d = p_eff - g["rs_min"]
    ok = bool(d > 6.0 * sigma)
    return {
        "control": "C8",
        "que": "contencion informativa del anillo testigo",
        "entra_en_veredicto": False,
        "p_eff": p_eff,
        "p_eff_menos_rs_min": d,
        "6_sigma": 6.0 * sigma,
        "interior_util_frac": g["interior_util_frac"],
        "causa": "p_eff - r*_min = %.6f > 6 sigma = %.1f : %s" % (d, 6.0 * sigma,
                                                                  "PASA" if ok else "ROJO"),
        "ok": ok,
        "rc": None,
    }


# --------------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Arnes del potencial de Zerilli (M>0) en tortuga con capas F11 -- Gate 2D-F3")
    ap.add_argument("--dosM", type=float, default=DOSM)
    ap.add_argument("--rs0", type=float, default=RS0)
    ap.add_argument("--sigma", type=float, default=SIGMA)
    ap.add_argument("--nr0", type=int, default=NR0)
    ap.add_argument("--nt0", type=int, default=NT0)
    ap.add_argument("--cfl", type=float, default=CFL_SELLADO)
    ap.add_argument("--ancho", type=float, default=ANCHO)
    ap.add_argument("--rs-min", dest="rs_min", type=float, default=RS_MIN)
    ap.add_argument("--L-frac", dest="L_frac", type=float, default=L_FRAC)
    ap.add_argument("--n", type=int, default=N_PERFIL)
    ap.add_argument("--A", type=float, default=A_ESPONJA)
    ap.add_argument("--solo-controles", dest="solo", default=None)
    ap.add_argument("--json", dest="json_ruta", default="auto")
    ap.add_argument("--estricto", action="store_true")
    ap.add_argument("--stamp", action="store_true")
    a = ap.parse_args(argv)

    if a.cfl > CFL_SELLADO + 1e-12:
        raise SystemExit("FAIL-CLOSED: CFL = %.10f > sellado %.10f (la cota no se rebaja)"
                         % (a.cfl, CFL_SELLADO))
    if int(a.n) != N_PERFIL:
        raise SystemExit("FAIL-CLOSED: perfil n = %d fuera de la familia sellada (F11: n = 3)"
                         % int(a.n))

    t0 = utc_now()

    # ---------------- modo banco de controles (paso 4 del protocolo del dueno) ----------------
    if a.solo:
        lista = [x.strip().upper() for x in a.solo.split(",") if x.strip()]
        out = {"hora_utc": hora_utc(), "universo_declarado": LAMINAS_DECLARADAS,
               "huella": HUELLA, "modo": "solo-controles", "controles_pedidos": lista,
               "controles": []}
        for c in lista:
            if c == "C0":
                r = control_C0()
            elif c == "C1A":
                r = control_C1a(a.dosM)
            elif c == "C1B":
                r = control_C1b(a.dosM)
            elif c == "C9":
                r = control_C9(a.dosM)
            elif c == "C3":
                r = f11.control_C3(0.55)
            else:
                r = {"control": c, "ok": False, "rc": 2,
                     "causa": "control no disponible en modo --solo-controles (requiere la "
                              "evolucion de C2)"}
            out["controles"].append(r)
            print("[%s] rc=%s ok=%s" % (r.get("control"), r.get("rc"), r.get("ok")))
            print("    %s" % r.get("causa", ""))
        rc = 0 if all(x.get("ok") for x in out["controles"]) else 1
        out["rc_global"] = rc
        print("RC_GLOBAL_SOLO_CONTROLES = %d" % rc)
        return rc

    # ---------------- corrida completa ----------------
    g = f11.geometria(a.rs_min, a.ancho, a.L_frac, int(a.n), a.A)
    g_win = dict(g)
    g_win["c"] = float(a.rs0)
    m = f2.Malla2D(g["rs_min"], g["rs_max"], int(a.nr0), int(a.nt0), float(a.cfl), 0)
    dt = float(m.dt_cota)
    r_nod, f_nod, pot, wang = campos_de_malla(m, a.dosM)
    ip = int(np.argmin(np.abs(m.rs - g["p"])))
    p_eff = float(m.rs[ip])
    vw = f11.ventanas(g_win, p_eff, a.sigma, g["rs_min"], g["rs_max"])
    cron = cronologia(g, p_eff, a.rs0, a.sigma)
    p2 = perfil_p2(m.th)
    sinth = np.sin(m.th)
    den_p2 = float(np.sum(p2 * p2 * sinth))
    k_a = int(math.floor(12.0 / dt))
    k_b = int(math.floor(vw["t_s"] / dt))
    nsteps = int(math.ceil(vw["T_obs"] / dt))
    u0 = dato_f3(m, a.rs0, a.sigma)
    max_inc = float(np.max(np.abs(u0)))

    print("UNIVERSO DECLARADO: malla sellada F11 (r* en [%.1f, %.1f], nr0=%d, nt0=%d, hr=%r) | "
          "mapa tortuga con 2M = %.1f sobre esa malla | dato de C2 | cifras analiticas de V_Z y U"
          % (g["rs_min"], g["rs_max"], m.nr, m.nt, float(m.hr), a.dosM))
    print("HUELLA = %s" % HUELLA)
    print("hora_utc = %s" % hora_utc())
    print("geometria F11 (VERBATIM): L = %.6f | c_esponja = %.6f | p = %.6f | p_eff = %.16f | "
          "r*_sponge = %.6f | r*_max = %.6f | gamma_max = %.16f | integral_gamma = %.16f | "
          "solape = %.6f" % (g["L"], g["c"], g["p"], p_eff, g["rs_sponge"], g["rs_max"],
                             g["gamma_max"], g["integral_gamma"], g["solape"]))
    print("2M = %.6f | l = %d | lambda = %.6f | U(r*_min) = %.12e | U(74.0) = %.12e | "
          "U(r*_max) = %.12e | max |U| = %.12e en r* = %.6f"
          % (a.dosM, L_ANGO, LAM_Z, float(pot[0]), float(u0 is not None and
             pot[int(np.argmin(np.abs(m.rs - 74.0)))]),
             float(pot[-1]), float(np.max(np.abs(pot))), float(m.rs[int(np.argmax(np.abs(pot)))])))
    print("ventanas (c_dato = %.1f): t_1 = %.6f | t_a = %.6f | t_s = %.6f | t_ret = %.6f | "
          "t_3 = %.6f | T_obs = %.6f" % (a.rs0, vw["t_1"], vw["t_a"], vw["t_s"], vw["t_ret"],
                                         vw["t_3"], vw["T_obs"]))
    print("dt = %.18e | nsteps = %d | capturas C4 en k = %d (t = %.6f) y k = %d (t = %.6f)"
          % (dt, nsteps, k_a, k_a * dt, k_b, k_b * dt))
    print("D7 CRONOLOGIA DECLARADA (unidades de r* = unidades de t): mitad saliente: anillo "
          "%.3f, esponja %.3f, retorno al anillo %.3f | mitad entrante: pared %.3f, anillo "
          "%.3f (frente %.3f), esponja %.3f, retorno de SU eco al anillo %.3f (frente %.3f)"
          % (cron["T_centro_saliente_en_anillo"], cron["T_centro_saliente_en_esponja"],
             cron["T_retorno_saliente_en_anillo"], cron["T_centro_entrante_en_pared"],
             cron["T_centro_entrante_en_anillo"], cron["T_frente_entrante_en_anillo"],
             cron["T_centro_eco_pared_en_esponja"], cron["T_retorno_eco_pared_en_anillo"],
             cron["T_frente_eco_pared_en_anillo"]))

    c0 = control_C0()
    c1a = control_C1a(a.dosM)
    c1b = control_C1b(a.dosM)
    c9 = control_C9(a.dosM)
    c3 = f11.control_C3(0.55)
    for r in (c0, c1a, c1b, c9, c3):
        print("[%s] rc=%s ok=%s" % (r.get("control"), r.get("rc"), r.get("ok")))
        print("    %s" % r.get("causa", ""))

    res_on = corrida_c2(m, g, g_win, dt, nsteps, True, pot, wang, a.rs0, a.sigma,
                        capturas=(k_a, k_b, nsteps))
    res_off = corrida_c2(m, g, g_win, dt, k_b + 1, False, pot, wang, a.rs0, a.sigma,
                         capturas=(k_a, k_b))
    c4 = control_C4(m, g, dt, pot, wang, res_on, res_off, (k_a, k_b))

    rdb = res_on["rdb"]
    acc = res_on["acc"]
    ok_c2 = bool(rdb is not None and rdb <= UMBRAL_R_DB)
    if rdb is None:
        causa_c2 = ("R_dB NO MEDIBLE: E_sal = %.6e, E_vuelta = %.6e (la razon no existe)"
                    % (acc["E_sal"], acc["E_vuelta"]))
    else:
        causa_c2 = ("R_dB = %.12f dB <= %.1f dB : %s | E_sal = %.6e | E_muerta = %.6e | "
                    "E_vuelta = %.6e | E_entrante = %.6e"
                    % (rdb, UMBRAL_R_DB, "PASA" if ok_c2 else "ROJO",
                       acc["E_sal"], acc["E_muerta"], acc["E_vuelta"], acc["E_entrante"]))
    c2 = {
        "control": "C2",
        "que": "dispersion por U(r*) con el dato en reposo y absorcion de la senal saliente en "
               "la capa F11 exterior",
        "universo": "malla sellada nr0=%d nt0=%d | nsteps = %d | dato l=2 en r* = %.1f, sigma = "
                    "%.1f, v^0 = 0" % (m.nr, m.nt, nsteps, a.rs0, a.sigma),
        "R_dB": rdb,
        "umbral_R_dB": UMBRAL_R_DB,
        "E_sal": acc["E_sal"],
        "E_muerta": acc["E_muerta"],
        "E_vuelta": acc["E_vuelta"],
        "E_entrante": acc["E_entrante"],
        "t_a": vw["t_a"],
        "t_ret": vw["t_ret"],
        "T_obs": vw["T_obs"],
        "amax": float(res_on["med"].amax),
        "eco_max": float(np.max(res_on["med"].eco)) if res_on["med"].eco else 0.0,
        "var_theta_max": float(np.max(res_on["med"].var_theta)) if res_on["med"].var_theta else 0.0,
        "residuo_no_P2_dato_inicial": residuo_no_p2(u0, m.th, p2, sinth, den_p2),
        "residuo_no_P2_solucion_final": residuo_no_p2(res_on["u"], m.th, p2, sinth, den_p2),
        "causa": causa_c2,
        "ok": ok_c2,
        "rc": 0 if ok_c2 else 1,
    }
    print("[C2] rc=%s ok=%s" % (c2["rc"], c2["ok"]))
    print("    %s" % causa_c2)
    print("    residuo no-P2 (DATO inicial / SOLUCION final) = %.6e / %.6e (informativo: mide el "
          "piso del metro angular y, separado, el objeto)"
          % (c2["residuo_no_P2_dato_inicial"], c2["residuo_no_P2_solucion_final"]))
    print("[C4] rc=%s ok=%s" % (c4["rc"], c4["ok"]))
    print("    %s" % c4["causa"])

    c6 = control_C6(m, a.dosM, pot, wang, u0, p2, sinth, den_p2)
    c7 = control_C7(res_on["med"], max_inc, m, g, a.rs0, a.sigma)
    c8 = control_C8(m, g, p_eff, a.sigma)
    for r in (c6, c7, c8):
        print("[%s] rc=%s ok=%s aplicable=%s" % (r.get("control"), r.get("rc"), r.get("ok"),
                                                 r.get("aplicable", True)))
        print("    %s" % r.get("causa", ""))

    gating = [c0, c1a, c1b, c2, c3, c4, c6, c9]
    informativos = [c7, c8]
    rojos = [x["control"] for x in gating if not x.get("ok")]
    veredicto = "VERDE" if not rojos else "ROJO"
    print("CONTROLES QUE DECIDEN: %s" % ", ".join(x["control"] for x in gating))
    print("CONTROLES INFORMATIVOS (no deciden): %s" % ", ".join(x["control"] for x in informativos))
    print("VEREDICTO = %s | rojos = %s" % (veredicto, rojos if rojos else "ninguno"))

    crudo = {
        "huella": HUELLA,
        "huella_preregistro": HUELLA_PREREGISTRO,
        "huella_errata": HUELLA_ERRATA,
        "huella_f11": HUELLA_F11,
        "huella_v3": HUELLA_V3,
        "huella_dueno_en_crudo": 0,
        "preregistro": PREREGISTRO,
        "errata": ERRATA,
        "casa_f11": ARNES_F11,
        "casa_v3": ARNES_V3,
        "identidad_self": identidad_self(),
        "hora_inicio_utc": t0.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "hora_fin_utc": hora_utc(),
        "universo_declarado": LAMINAS_DECLARADAS,
        "laminas_declaradas": LAMINAS_DECLARADAS,
        "parametros": {"dosM": float(a.dosM), "l": L_ANGO, "lam": LAM_Z, "rs0": float(a.rs0),
                       "sigma": float(a.sigma), "nr0": int(m.nr0), "nt0": int(m.nt0),
                       "cfl": float(m.cfl), "nivel": int(m.nivel), "n": int(a.n),
                       "A": float(a.A), "L_frac": float(a.L_frac), "ancho": float(a.ancho),
                       "rs_min": float(a.rs_min)},
        "geometria_f11": {k: (float(v) if isinstance(v, (int, float)) else v) for k, v in g.items()},
        "malla": {"nr": int(m.nr), "nt": int(m.nt), "hr": float(m.hr), "hth": float(m.hth),
                  "dt": dt, "rs_min": float(m.rs[0]), "rs_max": float(m.rs[-1]),
                  "nsteps": int(nsteps), "ip": int(ip), "p_eff": p_eff},
        "ventanas": {k: (list(map(float, v)) if isinstance(v, list) else float(v))
                     for k, v in vw.items()},
        "cronologia_D7": cron,
        "campos": {"U_r_min": float(pot[0]), "U_r_max": float(pot[-1]),
                   "max_abs_U": float(np.max(np.abs(pot))),
                   "r_star_en_max_abs_U": float(m.rs[int(np.argmax(np.abs(pot)))]),
                   "r_min_de_rs_min": float(r_nod[0]),
                   "r_max_de_rs_max": float(r_nod[-1])},
        "controles": {x["control"]: x for x in gating + informativos},
        "controles_gating": [x["control"] for x in gating],
        "controles_informativos": [x["control"] for x in informativos],
        "rojos": rojos,
        "veredicto": veredicto,
        "rc": 0 if veredicto == "VERDE" else 1,
        "defectos_declarados": ["D6 (C7 no aplicable: la banda sellada contiene el dato)",
                                "D7 (la mitad entrante regresa de la pared interna y su eco de "
                                "esponja cae dentro de la ventana de vuelta)"],
        "notas": ["dt_cota tomada con f = 1 (la de F11): conservadora porque f <= 1 en r > 2M",
                  "el factor geometrico del medidor es r*^2 (F11) y cancela en R_dB",
                  "R_dB es una RAZON en energia: no se re-ventanea ni se mueve ningun umbral",
                  "la unica linea nueva del sector angular es el factor metrico f en el peso"],
    }
    ruta = a.json_ruta
    if ruta == "auto":
        os.makedirs(os.path.join(_AQUI, "data"), exist_ok=True)
        nm = "crudo_2d_f3_zerilli_%s.json" % stamp_utc()
        ruta = os.path.join(_AQUI, "data", nm)
    info = f11.escribir_crudo(crudo, ruta)
    print("crudo: %s | lineas = %d | bytes = %d | sha256 = %s"
          % (info["ruta"], info["lineas"], info["bytes"], info["sha256"]))

    if a.estricto and rojos:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
