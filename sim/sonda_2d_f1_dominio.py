#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# SONDA 2D-F1 -- DOMINIO DE EXACTITUD DEL GATE 2D-F1 (prueba nula de
#   d'Alembert 2D en espacio plano V=0, cfl optimo 2D = 1/sqrt(2))
# HUELLA-SONDA-2D-F1-DOMINIO-20261013
# ----------------------------------------------------------------------------
# PROCEDENCIA (no silenciosa):
#   v3 medida en /tmp/f4v3/sonda_2d_f1_v3_20261013.py  (147 l, sha256
#   634c33c4009622d999e79d5184adb77f043584d9c4bd63d3293e9940e4ca366b).
#   v4.a = v3 + cabecera impresa + gate --estricto. RETIRADA ANTES DE SELLAR:
#     su asercion de agudeza de CFL estaba INVERTIDA (enrojecia cuando el objeto
#     se comportaba bien). Identidad de la retirada: blob git 9d3445863ceb1d25e
#     d77cf81609742634d3db0b3, sha256 566c0bfb5fb6761474785bd94796c8b1017aa5e4
#     15bb52d0675484a4cf5d40dd, 239 l, 10522 B. Se conserva en
#     /tmp/f4v3/sonda_2d_f1_v4a_invertida_20261013.py con su crudo
#     /tmp/f4v3/crudo_v4a_invertido_20261013T191833Z.txt (73a53548d7ffc963c4962
#     bb5137b6b7f9c67b9dcb5bf842dd306eba49bbe0187).
#   v4.b = la de aqui: el predicado de agudeza se corrige a su direccion
#     (el desvio de CFL DEBE subir el residuo, no bajarlo) y el exceso se imprime.
#   CAMBIO DECLARADO: los renglones de DATOS de v4.b son los de v3 (verificado
#   con diff: 55 lineas identicas). Ninguna cifra fue re-tocada.
# ----------------------------------------------------------------------------
# UNIVERSO DECLARADO: malla 2D PERIODICA uniforme N x N (espaciamiento h en las
#   DOS direcciones), cfl = dt/h, modos EXACTOS de la malla
#   (kx = 2*pi*mx/L, ky = 2*pi*my/L, L = N*h, mx/my enteros).
#   QUEDA FUERA (no se mide aqui): frontera absorbente de perimetro · fondo
#   curvo M>0 · eje theta=0,pi (regularidad polar) · incidencia rasante
#   (ang -> 90 grados con celdas en theta) · no linealidad. Este instrumento mide
#   SOLO el dominio de exactitud del esquema en el caso plano V=0, periodico.
# UNIDAD: residuo L2 relativo  ||u_num - u_exacta|| / ||u_exacta||  (adimensional)
# VENTANA: T = 10.0 fijo; n = round(T/dt) pasos.  UMBRAL: 1e-13.
# CADENA DE METROS (cada uno aisla UNA pieza; no son el mismo metro):
#   dato  = 'cont' : v^{-1/2} = w*cos(ph)*sin(w*dt/2)            (medio paso CONTINUO)
#   dato  = 'disc' : v^{-1/2} = cos(ph)*(1-cos(xi))/dt, xi del SIMBOLO DISCRETO
#   ref   = 'cont' : se compara contra cos(ph)*cos(w*n*dt)
#   ref   = 'sim'  : se compara contra cos(ph)*cos(xi*n)
# DENOMINADOR Y NULO: el nulo de este gate es EL MISMO OPERADOR con dato='cont'
#   (medio paso continuo) sobre LA MISMA familia -> si el nulo bajara tanto como
#   el objeto, el gate no discriminaria nada. El control negativo son modos NO
#   diagonales (ang != 45 grados) al MISMO cfl: NO deben bajar de 1e-13, o el
#   umbral no tiene dominio.
# v1 media el defecto del DATO NO PERIODICO (kx no entero en el toro): defecto de METRO.
# v2 media el defecto del DATO de medio paso (O(theta^4) por paso): defecto de DATO.
# v3/v4 separan ESQUEMA de DATO: el gate va sobre (dato=disc, ref=cont).
# comando: python3 -B sim/sonda_2d_f1_dominio.py
# comando: python3 -B sim/sonda_2d_f1_dominio.py --estricto   (sale 1 si miente)
# ============================================================================
import hashlib
import math
import os
import sys
import time

import numpy as np

SQ2 = math.sqrt(2.0)
UMBRAL = 1e-13
HUELLA = "HUELLA-SONDA-2D-F1-DOMINIO-20261013"

ESTRICTO = "--estricto" in sys.argv[1:]


def sha256_self():
    try:
        with open(os.path.abspath(__file__), "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except Exception:
        return "NO-MEDIBLE"


def simbolo(N, h, cfl, mx, my):
    L = float(N) * h
    kx = 2.0 * math.pi * float(mx) / L
    ky = 2.0 * math.pi * float(my) / L
    S = math.sin(0.5 * kx * h) ** 2 + math.sin(0.5 * ky * h) ** 2
    arg = cfl * math.sqrt(S)
    if arg > 1.0:
        return None
    xi = 2.0 * math.asin(arg)
    w = math.hypot(kx, ky)
    return xi, w, kx, ky


def corre(N, h, cfl, mx, my, T, dato, ref):
    r = simbolo(N, h, cfl, mx, my)
    if r is None:
        return None, None
    xi, w, kx, ky = r
    dt = cfl * h
    n = int(round(T / dt))
    x = np.arange(N) * h
    X, Y = np.meshgrid(x, x, indexing="ij")
    ph = kx * X + ky * Y
    u = np.cos(ph)
    if dato == "cont":
        vh = w * np.cos(ph) * math.sin(0.5 * w * dt)
    else:
        vh = np.cos(ph) * (1.0 - math.cos(xi)) / dt
    h2 = h * h
    for _ in range(n):
        lap = (np.roll(u, 1, 0) + np.roll(u, -1, 0)
               + np.roll(u, 1, 1) + np.roll(u, -1, 1) - 4.0 * u) / h2
        vh = vh + dt * lap
        u = u + dt * vh
    om = w * n * dt if ref == "cont" else xi * n
    ue = np.cos(ph) * math.cos(om)
    return np.linalg.norm(u - ue) / np.linalg.norm(ue), n


def corre_1d(N, h, cfl, m, T, dato, ref):
    L = float(N) * h
    k = 2.0 * math.pi * float(m) / L
    xi = 2.0 * math.asin(cfl * math.sin(0.5 * k * h))
    w = k
    dt = cfl * h
    n = int(round(T / dt))
    x = np.arange(N) * h
    ph = k * x
    u = np.cos(ph)
    if dato == "cont":
        vh = w * np.cos(ph) * math.sin(0.5 * w * dt)
    else:
        vh = np.cos(ph) * (1.0 - math.cos(xi)) / dt
    h2 = h * h
    for _ in range(n):
        lap = (np.roll(u, 1) + np.roll(u, -1) - 2.0 * u) / h2
        vh = vh + dt * lap
        u = u + dt * vh
    om = w * n * dt if ref == "cont" else xi * n
    ue = np.cos(ph) * math.cos(om)
    return np.linalg.norm(u - ue) / np.linalg.norm(ue), n


N, h, CFL, T = 128, 0.100, 1.0 / SQ2, 10.0
DIAG = (1, 2, 3, 4, 6, 8)

print("=" * 84)
print("SONDA 2D-F1 v4.b: esquema vs dato  (V=0, periodico, cfl=1/sqrt(2))")
print(HUELLA)
print("=" * 84)
print("UNIVERSO DECLARADO: malla 2D periodica %d x %d, h=%.6f, L=%.6f," % (N, N, h, N * h))
print("  cfl=%.10f (=1/sqrt(2)), T=%.3f, modos enteros (mx,my), residuo L2 relativo." % (CFL, T))
print("QUEDA FUERA: capa absorbente · M>0 · eje polar · angulo rasante · no linealidad.")
print("UMBRAL: %.1e   UNIDAD: residuo L2 relativo   NULO: mismo operador con dato=cont" % UMBRAL)
print("COMANDO: python3 -B sim/sonda_2d_f1_dominio.py%s" % (" --estricto" if ESTRICTO else ""))
print("INSTANTE UTC: %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("HUELLA DEL INSTRUMENTO: %s" % sha256_self())

print("")
print("[S] SIMBOLO (algebra, sin integrar): xi_disc vs w*dt  y  xi_disc vs el 1D equivalente")
print("     (mx,my)   ang_deg        |xi - w*dt|/w*dt")
for mx, my in ((2, 0), (3, 1), (2, 1), (3, 2), (1, 1), (2, 2), (3, 3), (1, 0)):
    r = simbolo(N, h, CFL, mx, my)
    if r is None:
        continue
    xi, w, _, _ = r
    print("     (%d,%d)   %6.2f      %.6e"
          % (mx, my, math.degrees(math.atan2(my, mx)), abs(xi - w * CFL * h) / (w * CFL * h)))

print("")
print("[A] ESQUEMA PURO  (dato=disc, ref=cont)  -- el residuo que queda ES la dispersion")
print("     (mx,my)   ang_deg    residuo(dato=disc)   residuo(dato=cont)")
for mx, my in ((2, 0), (3, 1), (2, 1), (3, 2), (1, 1), (2, 2), (3, 3), (1, 0)):
    rd, n = corre(N, h, CFL, mx, my, T, "disc", "cont")
    rc, _ = corre(N, h, CFL, mx, my, T, "cont", "cont")
    print("     (%d,%d)   %6.2f    %.6e        %.6e"
          % (mx, my, math.degrees(math.atan2(my, mx)), rd, rc))

print("")
print("[B] FAMILIA DIAGONAL PURA (mx == my, ang = 45 grados EXACTO), cfl=1/sqrt(2), T=10")
print("     m    residuo(dato=disc)   residuo(dato=cont)   residuo(disc,ref=sim)")
for m in DIAG:
    rd, _ = corre(N, h, CFL, m, m, T, "disc", "cont")
    rc, _ = corre(N, h, CFL, m, m, T, "cont", "cont")
    rs, _ = corre(N, h, CFL, m, m, T, "disc", "sim")
    print("     %d    %.6e        %.6e        %.6e" % (m, rd, rc, rs))

print("")
print("[C] REFINADO (mx=my=2, dato=disc) + control 1D equivalente (cfl=1/sqrt(2))")
print("     N      h       residuo(2D diag)   residuo(2D eje)   residuo(1D)")
for NN, hh in ((64, 0.200), (128, 0.100), (256, 0.050), (512, 0.025)):
    rd, _ = corre(NN, hh, CFL, 2, 2, T, "disc", "cont")
    re_, _ = corre(NN, hh, CFL, 2, 0, T, "disc", "cont")
    r1, _ = corre_1d(NN, hh, CFL, 2, T, "disc", "cont")
    print("     %3d   %.3f   %.6e     %.6e     %.6e" % (NN, hh, rd, re_, r1))

print("")
print("[D] CONTROL DE CFL SOBRE LA DIAGONAL (mx=my=2, dato=disc, N=128)")
for cfl in (0.5, 0.6, 0.7, 1.0 / SQ2, 0.7072, 0.75, 1.0):
    r, n = corre(N, h, cfl, 2, 2, T, "disc", "cont")
    print("     cfl=%.6f   residuo=%.6e   n=%d" % (cfl, r, n))
_rd2, _ = corre(N, h, CFL, 2, 2, T, "disc", "cont")
_rdet, _ = corre(N, h, 0.7072, 2, 2, T, "disc", "cont")
EXCESO_CFL = _rdet / max(_rd2, 1.0e-300)

print("")
print("[E] CONTROL NEGATIVO: modos NO diagonales a cfl optimo (dato=disc) -- NO deben caer")
print("     (2,1): %.6e" % corre(N, h, CFL, 2, 1, T, "disc", "cont")[0])
print("     (3,1): %.6e" % corre(N, h, CFL, 3, 1, T, "disc", "cont")[0])
print("     (0,2): %.6e" % corre(N, h, CFL, 0, 2, T, "disc", "cont")[0])

print("")
print("=" * 84)
print("GATE 2D-F1 (postura): dato=disc, ref=cont, familia mx==my a cfl=1/sqrt(2) -> residuo < 1e-13")
print("CONTROL: modos NO diagonales al MISMO cfl NO bajan de 1e-13 (el umbral tiene dominio)")
print("=" * 84)
print("")
print("AGUDEZA DEL CFL (fuera de la region de datos, v4.b): exceso del desvio")
print("  cfl=0.707200 sobre el optimo 1/sqrt(2): x%.3e   (%.6e vs %.6e)"
      % (EXCESO_CFL, _rdet, _rd2))

# ----------------------------------------------------------------------------
# GATE --estricto : causa impresa + codigo de salida (un gate sin assert detras
# informa, no protege). Se exigen las DOS direcciones: el objeto baja Y el
# control NO baja. Un caso que devuelve el codigo esperado por otro motivo no
# discrimina: por eso se imprime la CAUSA de cada rojo.
# ----------------------------------------------------------------------------
rojos = []
if ESTRICTO:
    for m in DIAG:
        rd, _ = corre(N, h, CFL, m, m, T, "disc", "cont")
        if not (rd < UMBRAL):
            rojos.append("OBJETO no baja: m=%d residuo=%.6e" % (m, rd))
    for m in DIAG:
        rc, _ = corre(N, h, CFL, m, m, T, "cont", "cont")
        if rc < UMBRAL:
            rojos.append("NULO baja como el objeto (no discrimina): m=%d residuo=%.6e" % (m, rc))
    for mx, my in ((2, 1), (3, 1), (0, 2)):
        rnd, _ = corre(N, h, CFL, mx, my, T, "disc", "cont")
        if rnd < UMBRAL:
            rojos.append("CONTROL negativo baja (umbral sin dominio): (%d,%d) residuo=%.6e"
                         % (mx, my, rnd))
    if not (EXCESO_CFL > 1.0):
        rojos.append("desvio de CFL no empeora el residuo: cfl=0.707200 %.6e vs optimo %.6e"
                     % (_rdet, _rd2))
    if not (EXCESO_CFL >= 1.0e6):
        rojos.append("desvio de CFL no separa al menos x1e6: exceso x%.3e" % EXCESO_CFL)

print("")
if ESTRICTO:
    if rojos:
        print("VEREDICTO 2D-F1 (--estricto): ROJO  rojos=%d" % len(rojos))
        for x in rojos:
            print("   ROJO: %s" % x)
        sys.exit(1)
    print("VEREDICTO 2D-F1 (--estricto): VERDE  objeto<%.1e en los %d modos diagonales"
          % (UMBRAL, len(DIAG)))
    print("   y el control (nulo · no diagonales · desvio de CFL x%.3e) NO baja de %.1e."
          % (EXCESO_CFL, UMBRAL))
    sys.exit(0)
print("(sin --estricto: no hay veredicto; el gate no se declara por default)")
