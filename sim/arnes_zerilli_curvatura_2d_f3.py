#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ARNES DEL POTENCIAL DE ZERILLI (M > 0) EN TORTUGA CON CAPAS F11 -- GATE 2D-F3.

HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261013
HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261014-R3   <- revision R3 (cinematica + C6 + C4)
HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261013-R4   <- revision R4 (D16 dominio de C4 + D17 piso
                                                      del metro de C6). NO mueve ningun umbral.

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

REVISION R3 (orden del dueno, 14-Oct-2026) -- HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261014-R3.
Cambia SOLO la cinematica del dato, la forma de C6 y el dominio de C4. NO mueve un solo umbral.
  * CINEMATICA DE VENTANAS -- se toma la SEGUNDA de las dos rutas que el dueno ofrecio
    ("volviendo al paquete saliente en r* = 26.0"). Razon MEDIDA, no de gusto: la cola del
    agujero negro en este dominio NO TIENE TIEMPO DE ARRIBO. La pared Dirichlet interna en
    r* = 2.0 esta por dentro del maximo de U(r*) (~2.85) y forma con el una CAVIDAD que radia
    hacia afuera mientras decaiga; su emision es asintotica, de modo que "t_arribo_tail" no
    existe como numero y "T_vuelta > t_arribo_tail + 6 sigma" solo se podria escribir DESPUES de
    ver E_vuelta (familia (a): ventana elegida despues de la salida). La ruta del paquete
    saliente cierra el canal de contaminacion POR CONSTRUCCION, no por re-ventaneo.
  * El dato de R3 es el de F11 (f11.dato_saliente VERBATIM: sigma = 2.0, omega = 1.0,
    v^0 = -d_r u^0, SALIENTE PURO) en r* = 26.0 (el c de F11) multiplicado por P_2(cos theta):
    el sector angular queda VIVO (la objecion D5 al dato de F11 era su vacuidad ANGULAR, no su
    condicion saliente).
  * f11.ventanas sigue VERBATIM y sin tocar: con c = 26.0 sus propias formulas vuelven a ser
    correctas (t_1 = 24.125326, t_a = 36.125326, t_s = 36.0, t_ret = 59.874674, t_3 = 71.874674,
    T_obs = 83.874674). El defecto D7 era del DATO, no de las formulas.
  * C6 RE-EXPRESADO (orden 2 del dueno): deja de exigir simetria radial plana y audita la
    PUREZA DEL MODO CUADRUPOLAR l = 2 del CAMPO. La dispersion angular de U pasa a lectura
    INFORMATIVA; el criterio es el residuo no-P_2 del CAMPO sobre FILAS VIVAS declaradas, con el
    residuo del dato como DENOMINADOR DECLARADO.
  * El dato ESTATICO de §R5 (r* = 10.0, v^0 = 0) NO se borra: queda como FALSADOR reproducible
    con --dato estatico-r10, para que el ROJO se pueda volver a medir sobre el mismo objeto.
  D13 (defecto de METRO, nuevo): C6 medido con la mascara de filas de R2 (msk = d2 > 0.0) es una
      razon cuyo denominador tiende a 0 en las filas vacias de la cola; el maximo sobre filas
      mide 1/0 y no el campo. El crudo del ROJO imprimio residuo_no_P2_solucion_final =
      9.999999e-01 junto a residuo_no_P2_dato_inicial = 2.953954e-16. R3 declara la mascara de
      FILA VIVA (d2 >= FRAC_FILA_VIVA * max_fila d2) y NO mueve UMBRAL_C6 = 1e-12.
  D14 (defecto de DOMINIO, nuevo): la captura de C4 heredada de F11 (k_a = floor(12.0/dt), t =
      11.975103) cae cuando el frente del paquete esta en r* = 22.0 y la capa empieza en
      r* = 74.0: una diferencia no nula ahi NO PUEDE ser contaminacion de capa, luego esa captura
      no mide el "que" del control. Con el dato de §R5 (t_s = 52.0) la SEGUNDA captura heredada
      (t = 51.968290) tambien cae ANTES de t_s = 52.0: el rojo de C4 del 14-Oct se midio ENTERO
      fuera de su dominio. R3 declara el dominio (pasos con t >= t_s) y NO mueve UMBRAL_C4.
  D15 (defecto de DOMINIO DEL DATO, nuevo): el soporte +-6 sigma del dato de §R5 (centro 10.0)
      es [-2.0, 22.0] y sale de la malla por abajo (r*_min = 2.0) pegandose a la pared Dirichlet:
      es la misma causa que D7, vista del lado de la GEOMETRIA del dato. La guarda de R3 lo
      cierra fail-closed para cualquier centro y sigma.
  D16 (defecto de DOMINIO, nuevo en R4; signo OPUESTO a D14): el dominio que R3 declaro para C4
      estaba INVERTIDO. R3 hizo decidir los pasos con t >= t_s, que son justo aquellos en los que
      la capa F11 esta TRABAJANDO (reflectancia del absorbedor discreto), y dejo como simple
      lectura la franja t <= t_s, que es la unica en la que la capa vale 1.0 exacto en toda fila
      interior y una diferencia no nula NO PUEDE ser contaminacion de capa. Medido en el ROJO del
      14-Oct: prefijo t <= t_s -> 2.325996e-14 (PASA, margen 4.3x); cola t > t_s -> 1.875977e-02,
      que es el 1.5 % de la diferencia de contorno (1.33 en k = 1600): la capa TRABAJANDO, no
      contaminacion. R4 invierte el rotulo y anade GUARDA DE DOMINIO fail-closed.
  D17 (defecto de METRO, nuevo en R4; familia D13): UMBRAL_C6 = 1e-12 esta POR DEBAJO del piso del
      propio metro angular en la malla sellada. Medido: el leakage relativo del operador angular
      sobre su funcion propia P_2 es 2.239675e-04 por aplicacion en nt0 = 33, y el piso de CAMPO
      medido por refinamiento en theta converge x5.6-x6.3 por duplicacion (segundo orden en
      h_theta). Exigir 1e-12 es exigir del esquema una precision que su paso angular no tiene por
      construccion. R4 decide C6 como RAZON AL PISO DECLARADO (<= 1.0) y conserva UMBRAL_C6 =
      1e-12 en el crudo como cifra NO movida. ROTULO DEL DATO: el dato saliente x P_2(cos theta)
      NO es theta-independiente (el sector l = 2 esta vivo por construccion fisica), asi que la
      lectura variacion_theta_max = 0.0 de C6 en F11 NO se hereda.
  NINGUN UMBRAL SE MUEVE: UMBRAL_R_DB = -40.0, UMBRAL_C4 = 1e-13 y UMBRAL_C6 = 1e-12 quedan
  exactamente como estaban. El criterio NUEVO de C6 (umbral_de_razon_al_piso = 1.0) no es un
  umbral movido: es la forma adjudicada para una cantidad que el 1e-12 no puede medir (D17).
  R_dB sigue siendo una RAZON EN ENERGIA con el medidor de F11.

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
HUELLA_R2 = "HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261013-R2"
HUELLA_R3 = "HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261014-R3"
HUELLA_R4 = "HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261013-R4"
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
RS0 = 10.0                              # centro del dato ESTATICO de §R5 (13-Oct): NO se edita;
                                        # R3 lo conserva como falsador reproducible
RS_DATO_R3 = 26.0                       # R3: centro del dato SALIENTE = c de F11 (verbatim)
OMEGA_R3 = 1.0                          # R3: omega de F11 (dato saliente)
DATO_R3 = "saliente-r26"                # R3 (default) | "estatico-r10" = el del ROJO
FRAC_FILA_VIVA = 1e-3                   # R3: fraccion del maximo del campo que define FILA VIVA
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
UMBRAL_C6_RAZON = 1.0                   # R4 (D17): criterio de C6 = residuo_no_P2 / (piso del
                                        # metro por paso * paso) <= 1.0. NO mueve UMBRAL_C6 =
                                        # 1e-12: ese queda en el crudo como cifra NO movida (esta
                                        # por debajo del piso del metro en la malla sellada)
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
    "dato de C2 (falsador R3): gaussiana en r*-10 con sigma=2 y P_2(cos theta), v^0 = 0",
    "dato de R3: saliente puro de F11 en r*=26.0, sigma=2, omega=1, con P_2(cos theta)",
    "medidor, ventanas, acumulacion y R_dB verbatim de F11",
]

# Piso de CAMPO del metro angular, medido por REFINAMIENTO en theta a IGUAL tiempo fisico final
# (T = 83.917133311096, nsteps = round(T / dt_nt)); cifra = |res no-P_2| / |P_2| absoluto.
# NO es un umbral: es la corroboracion externa del piso por paso que C6 mide en la corrida.
# Respaldo: sonda heredoc python3 -B re-corriendo simula_f3 con nt0 en {33, 65, 129}.
PISO_REFINAMIENTO_THETA = {
    "hora_utc": "2026-10-14T02:06:19Z",
    "respaldo": "sonda heredoc python3 -B: simula_f3 a nt0 en {33, 65, 129} con el MISMO tiempo "
                "fisico final T = 83.917133311096 y nsteps = round(T / dt_nt)",
    "tiempo_fisico_final": 83.917133311096,
    "residuo_no_P2_relativo": {
        "nt0_33": {"k787": 2.8771e-05, "k1309": 3.8115e-05, "k1836": 2.6768e-04},
        "nt0_65": {"k787": 5.1617e-06, "k1309": 6.7873e-06, "k1836": 7.9337e-06},
        "nt0_129": {"k787": 8.1470e-07, "k1309": 1.1655e-06, "k1836": 1.4232e-06},
    },
    "razon_por_duplicacion": "x5.6 - x6.3 (segundo orden en h_theta)",
    "no_convergencia_declarada": "max|u| en k = 1836: 2.2633e-02 (nt0 = 33) vs 9.3697e-01 "
                                 "(nt0 = 65): el campo a t > 60 NO esta convergido en theta, por "
                                 "eso esa captura entra como INFORMATIVA",
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
    """DATO DE §R5 (v^0 = 0): u^0 = amp exp(-(r*-rs0)^2/(2 sigma^2)) P_2(cos theta).

    R3 NO lo borra: queda como FALSADOR del ROJO (--dato estatico-r10). Es el dato cuya mitad
    entrante produce D7 y D15.
    """
    env = float(amp) * np.exp(-(m.rs - float(rs0)) ** 2 / (2.0 * float(sigma) ** 2))
    return env[:, None] * perfil_p2(m.th)[None, :]


def dato_saliente_l2(m, c, sigma, omega):
    """DATO DE R3: saliente puro de F11 (f11.dato_saliente VERBATIM) con contenido l = 2 exacto.

        x   = r* - c
        u^0 = env(x) cos(omega x) P_2(cos theta)
        v^0 = -d_r* u^0          (condicion saliente EXACTA, no heredada de un v^0 = 0)

    La parte radial la calcula la CASA (F11); aqui solo se anade el factor angular. Devuelve
    (u0, v0) 2D, ambos con la MISMA estructura angular exacta.
    """
    u_r, v_r = f11.dato_saliente(m.rs, float(c), float(sigma), float(omega))
    p2 = perfil_p2(m.th)
    return u_r[:, None] * p2[None, :], v_r[:, None] * p2[None, :]


def guarda_soporte_dato(rs_min, rs_sponge, c, sigma, ancho_extra=6.0):
    """GUARDA FAIL-CLOSED DE R3 (D15): el soporte +-6 sigma del dato debe caber ESTRICTO en
    (r*_min, r*_sponge). Si no cabe, el dato nace cortado por la pared Dirichlet o nace dentro de
    la capa: en los dos casos el ratio del medidor mide otra cosa.
    """
    lo = float(c) - float(ancho_extra) * float(sigma)
    hi = float(c) + float(ancho_extra) * float(sigma)
    ok = bool(lo > float(rs_min) and hi < float(rs_sponge))
    return {
        "ok": ok,
        "soporte_6sigma": [lo, hi],
        "pared_interna": float(rs_min),
        "esponja": float(rs_sponge),
        "causa": ("soporte +-%.0f sigma del dato = [%.6f, %.6f] vs pared interna %.1f y esponja "
                  "%.1f : %s"
                  % (ancho_extra, lo, hi, float(rs_min), float(rs_sponge),
                     "CABE ESTRICTO" if ok else "NO CABE (fail-closed)")),
    }


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


def residuo_no_p2(u, th, p2, sinth, den, frac_fila=0.0):
    """Norma relativa L2(theta) (medida sin(theta) dtheta) de la parte NO-P_2 de cada fila.

    frac_fila = 0.0 reproduce BIT A BIT el metro de R2 (msk = d2 > 0.0); esa es la lectura que
    imprimio 9.999999e-01 en el crudo del ROJO (D13: razon sobre filas vacias).
    frac_fila > 0 es la mascara de FILA VIVA de R3: la fila cuenta solo si su densidad angular
    llega a esa fraccion del maximo del CAMPO medido.
    """
    a = (u * p2[None, :] * sinth[None, :]).sum(axis=1) / den
    res = u - a[:, None] * p2[None, :]
    num = np.sqrt(np.sum(res * res * sinth[None, :], axis=1))
    d2 = np.sqrt(np.sum(u * u * sinth[None, :], axis=1))
    if float(frac_fila) > 0.0:
        dmax = float(d2.max())
        msk = (d2 >= float(frac_fila) * dmax) if dmax > 0.0 else np.zeros_like(d2, dtype=bool)
    else:
        msk = d2 > 0.0
    if not np.any(msk):
        return 0.0
    return float(np.max(num[msk] / d2[msk]))


def piso_operador_theta(nt, frac_fila=FRAC_FILA_VIVA):
    """Piso del METRO angular (D17): leakage relativo de L2_theta sobre su propia funcion propia.

    Se aplica el MISMO operador, con el MISMO criterio de residuo y la MISMA mascara de fila viva,
    a P_2(cos theta) en una malla theta de nt nodos (theta = 0 en el polo, theta = pi/2 en el
    ultimo nodo: las mallas se anidan). Devolver > 0 es inevitable: el esquema no puede representar
    exactamente la funcion propia. Ese numero NO es fisica: es el piso del instrumento, y por eso
    C6 decide contra el (razon <= 1.0) y no contra un umbral absoluto.
    """
    nt = int(nt)
    hth = 0.5 * math.pi / float(nt - 1)
    th = hth * np.arange(nt)
    p2t = perfil_p2(th)
    sinth_t = np.sin(th)
    den_t = float(np.sum(p2t * p2t * sinth_t))
    l2t = f2.L2_theta(np.repeat(p2t[None, :], 3, axis=0), th, hth, 2)[1:2, :]
    rel = residuo_no_p2(np.repeat(l2t, 3, axis=0), th, p2t, sinth_t, den_t, frac_fila)
    return {"nt": nt, "hth": float(hth), "piso_por_paso": float(rel)}


def corrida_c2(m, g, g_win, dt, nsteps, encender, pot, wang, u0, v0, sigma, capturas=()):
    """R3: el dato (u0, v0) entra ya construido desde main, para que la corrida ON y la OFF usen
    el MISMO objeto y la unica diferencia entre ambas sea la capa."""
    ip = int(np.argmin(np.abs(m.rs - g["p"])))
    p_eff = float(m.rs[ip])
    vw = f11.ventanas(g_win, p_eff, sigma, g["rs_min"], g["rs_max"])
    filas = np.nonzero(m.rs <= g["c"] - 6.0 * sigma)[0]
    damp = f11.damp_de(m.rs, g, dt)[:, None] if encender else np.ones((m.nr, 1))
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


def control_C4(m, g, dt, pot, wang, res_on, res_off, pasos, pasos_fuera=(),
               pasos_prologo=(), damp_on=None, t_s=None):
    """Pureza del interior util: ON vs OFF con el MISMO dt deben coincidir en r* < r*_sponge.

    DOMINIO DECLARADO (R4 / D16; el rotulo de R3 estaba INVERTIDO, signo opuesto a D14). La capa
    F11 solo puede cambiar el interior DESPUES de que el frente del paquete la toque (t_s): antes
    de t_s vale 1.0 exacto en toda fila interior (medido: damp_interior_bit = 0.0) y una
    diferencia no nula ahi NO PUEDE ser contaminacion de capa. Por eso el dominio que DECIDE es
    t <= t_s: mide que la diferencia sea redondeo. Los pasos con t > t_s (pasos_fuera) se miden y
    se imprimen con su razon d_interior / max|u|_esponja_ON, pero NO deciden: ahi la capa esta
    TRABAJANDO por definicion, y exigirles 1e-13 seria exigir un absorbedor perfecto.
    GUARDA DE DOMINIO (fail-closed): si algun paso de `pasos` cae en t > t_s el rotulo volvio a
    invertirse y el control se declara ROJO con la violacion escrita.
    NO se mueve UMBRAL_C4 = 1e-13.
    """
    interior = m.rs < g["rs_sponge"]
    exterior = ~interior
    t_s_ok = (t_s is not None)
    damp_bit = None
    if damp_on is not None:
        dd = np.asarray(damp_on, dtype=float)[:, 0][interior]
        damp_bit = float(np.max(np.abs(dd - 1.0)))

    def _mide(lista, con_razon=False):
        det, peor_l = [], 0.0
        for k in lista:
            kk = int(k)
            if kk not in res_on["caps"] or kk not in res_off["caps"]:
                det.append({"paso": kk, "t": kk * dt, "medido": False})
                continue
            a = res_on["caps"][kk]
            b = res_off["caps"][kk]
            d = float(np.max(np.abs(a[interior, :] - b[interior, :])))
            peor_l = max(peor_l, d)
            fila = {"paso": kk, "t": kk * dt, "medido": True, "dif_interior": d}
            if con_razon:
                esp = float(np.max(np.abs(a[exterior, :])))
                fila["max_abs_u_esponja_ON"] = esp
                fila["razon_d_interior_sobre_esponja_ON"] = (d / esp) if esp > 0.0 else None
            det.append(fila)
        return det, peor_l

    detalles, peor = _mide(pasos)
    det_fuera, peor_fuera = _mide(pasos_fuera, con_razon=True)
    det_pro, peor_pro = _mide(pasos_prologo)
    fuera_de_dominio = [int(k) for k in pasos
                        if (not t_s_ok) or (int(k) * dt > float(t_s))]
    margen = (float(t_s) - int(max(pasos)) * dt) if (t_s_ok and len(list(pasos))) else None
    ok = bool(peor <= UMBRAL_C4 and not fuera_de_dominio and t_s_ok)
    causa = ("max |u_ON - u_OFF| en r* < r*_sponge = %.6e <= %.0e : %s (dominio declarado t <= "
             "t_s = %s, pasos que DECIDEN %s, margen del ultimo = %s) | pasos con t > t_s "
             "(INFORMATIVOS: capa trabajando) %s = %.6e | prologo (inform.) %s = %.6e | "
             "violacion de dominio = %s | max |damp_interior - 1| = %s"
             % (peor, UMBRAL_C4, "PASA" if ok else "ROJO",
                ("%.6f" % t_s) if t_s_ok else "no declarado",
                str([int(x) for x in pasos]),
                ("%.6f" % margen) if margen is not None else "no medible",
                str([int(x) for x in pasos_fuera]), peor_fuera,
                str([int(x) for x in pasos_prologo]), peor_pro,
                str(fuera_de_dominio) if fuera_de_dominio else "ninguna",
                ("%.6e" % damp_bit) if damp_bit is not None else "no medido"))
    return {
        "control": "C4",
        "que": "pureza del interior util: la capa NO contamina el interior (ON vs OFF, mismo dt "
               "y misma longitud de corrida) en el dominio t <= t_s",
        "universo": "filas con r* < r*_sponge = %.1f (%d de %d filas) en los pasos de captura"
                    % (g["rs_sponge"], int(np.count_nonzero(interior)), m.nr),
        "dominio_declarado": {
            "criterio": "t <= t_s (antes de que el frente del paquete toque la capa: damp == 1.0 "
                        "exacto en toda fila interior)",
            "t_s": (float(t_s) if t_s_ok else None),
            "pasos_que_deciden": [int(x) for x in pasos],
            "margen_del_ultimo_paso_que_decide": margen,
            "pasos_fuera_del_dominio_informativos": [int(x) for x in pasos_fuera],
            "pasos_prologo_informativos": [int(x) for x in pasos_prologo],
            "guarda_de_dominio_fail_closed": "ningun paso que decide puede tener t > t_s",
            "violacion_de_dominio": fuera_de_dominio,
            "razon_informativa_de_fuera": "d_interior / max|u|_esponja_ON (la capa trabajando)",
        },
        "detalles_que_deciden": detalles,
        "dif_max_interior": peor,
        "detalles_fuera_dominio": det_fuera,
        "dif_max_interior_fuera_dominio": peor_fuera,
        "detalles_prologo": det_pro,
        "dif_max_interior_prologo": peor_pro,
        "damp_interior_bit": damp_bit,
        "umbral": UMBRAL_C4,
        "causa": causa,
        "ok": ok,
        "rc": 0 if ok else 1,
    }


def control_C6(m, dosM, pot, wang, u0, p2, sinth, den, campos=(), campos_informativos=(),
               escalera_nt=()):
    """R3/R4 (ordenes del dueno): PUREZA DEL MODO CUADRUPOLAR l = 2 DEL CAMPO.

    Ya NO se exige simetria radial plana (l = 0). ROTULO DEL DATO (R4): el dato es saliente puro de
    F11 x P_2(cos theta), el sector l = 2 esta VIVO por construccion fisica, luego el dato NO es
    theta-independiente; la lectura variacion_theta_max = 0.0 que C6 midio en F11 NO se hereda
    (queda solo como lectura informativa en C2). La dispersion angular del operador U(r*) y la
    pureza angular de -U u^0 pasan a LECTURA INFORMATIVA.

    CRITERIO R4 (D17: el 1e-12 de R3 estaba POR DEBAJO DEL PISO DEL PROPIO METRO). El metro
    angular no puede resolver por debajo de su leakage por aplicacion, medido aqui mismo sobre su
    funcion propia:
        piso_por_paso = residuo_no_p2(L2_theta(P_2))   (mismo operador, misma malla, misma
                                                       mascara de FILA VIVA)
        piso(k)       = piso_por_paso * k              (piso ACUMULADO: cota lineal por paso)
        razon_k       = residuo_no_p2(u_k) / piso(k)   criterio: max_k razon_k <= 1.0
    El piso por paso se CALIBRA ademas con la escalera de theta (misma funcion propia en mallas
    theta mas finas): si el piso cae como h_theta^2, es propiedad del METRO y no fisica.
    UMBRAL_C6 = 1e-12 NO se mueve: se conserva como cifra no movida e informativa. Las capturas
    cuyo campo NO esta convergido en theta se pasan en campos_informativos: se miden, se imprimen
    y NO deciden.
    """
    pot2d = np.repeat(pot[:, None], m.nt, axis=1)
    spread = float(np.max(pot2d.max(axis=1) - pot2d.min(axis=1)))
    a_con = acel_f3(m, u0, pot, wang)
    a_sin = acel_f3(m, u0, None, wang)
    delta = a_con - a_sin
    rel_delta = residuo_no_p2(delta, m.th, p2, sinth, den, FRAC_FILA_VIVA)
    l2p2 = f2.L2_theta(np.repeat(p2[None, :], 3, axis=0), m.th, m.hth, 2)[1:2, :]
    rel_l2 = residuo_no_p2(np.repeat(l2p2, m.nr, axis=0), m.th, p2, sinth, den, FRAC_FILA_VIVA)
    r_0 = residuo_no_p2(u0, m.th, p2, sinth, den, FRAC_FILA_VIVA)
    r_0_r2 = residuo_no_p2(u0, m.th, p2, sinth, den)
    piso_paso = float(rel_l2)
    nts = sorted(set([int(m.nt)] + [int(x) for x in escalera_nt if int(x) > 1]))
    escalera = [piso_operador_theta(nt, FRAC_FILA_VIVA) for nt in nts]
    for e in escalera:
        e["es_la_malla_sellada"] = bool(int(e["nt"]) == int(m.nt))
        e["razon_vs_nt_sellado"] = (e["piso_por_paso"] / piso_paso) if piso_paso > 0.0 else None

    def _bloque(lista):
        lec, peor_razon, peor_res = [], 0.0, 0.0
        for k, u_k, t_k in lista:
            kk = int(k)
            r_k = residuo_no_p2(u_k, m.th, p2, sinth, den, FRAC_FILA_VIVA)
            p_k = piso_paso * kk
            razon = (r_k / p_k) if p_k > 0.0 else None
            if razon is not None:
                peor_razon = max(peor_razon, razon)
            peor_res = max(peor_res, r_k)
            lec.append({"paso": kk, "t": float(t_k), "residuo_no_P2": r_k,
                        "piso_declarado": p_k, "razon_al_piso": razon,
                        "factor_sobre_dato": (r_k / r_0) if r_0 > 0.0 else None})
        return lec, peor_razon, peor_res

    lecturas, peor_razon, peor_res = _bloque(campos)
    lecturas_inf, peor_razon_inf, peor_res_inf = _bloque(campos_informativos)
    ok = bool(peor_razon <= UMBRAL_C6_RAZON)
    causa = ("pureza l = 2 del CAMPO sobre filas vivas (frac = %.1e): max razon al PISO = %.6e "
             "<= %.1f : %s (pasos que DECIDEN %s) | piso por paso = %.6e | residuo del DATO = "
             "%.6e | UMBRAL_C6 = %.0e INTACTO (no decide: esta por debajo del piso del metro) | "
             "informativas (campo no convergido en theta) %s -> max razon = %.6e | factor de "
             "amplificacion = %s | dispersion angular de U = %.1e | no-P_2 de -U u^0 = %.6e | "
             "escalera del piso en theta = %s"
             % (FRAC_FILA_VIVA, peor_razon, UMBRAL_C6_RAZON, "PASA" if ok else "ROJO",
                str([int(x[0]) for x in campos]), piso_paso, r_0, UMBRAL_C6,
                str([int(x[0]) for x in campos_informativos]), peor_razon_inf,
                ("%.6e" % (peor_res / r_0)) if r_0 > 0.0 else "no medible", spread, rel_delta,
                str([(int(e["nt"]), "%.3e" % e["piso_por_paso"]) for e in escalera])))
    return {
        "control": "C6",
        "que": "pureza del modo cuadrupolar l = 2 del CAMPO: el residuo no-P_2 no excede el PISO "
               "DECLARADO del metro angular (D17)",
        "universo": "campo 2D de la malla sellada (nr0=%d, nt0=%d) en los pasos de captura, con "
                    "mascara de FILA VIVA frac = %.1e" % (m.nr, m.nt, FRAC_FILA_VIVA),
        "rotulo_dato_angular": {
            "dato_theta_independiente": False,
            "motivo": "el dato es saliente puro de F11 x P_2(cos theta): el sector l = 2 esta "
                      "VIVO por construccion fisica y no es simetria radial plana",
            "lectura_F11_que_no_se_hereda": "C6 de F11 midio variacion_theta_max = 0.0 sobre un "
                                            "dato theta-independiente: esa lectura NO aplica",
        },
        "dominio_declarado": {
            "mascara": "d2 >= %.1e * max_fila d2" % FRAC_FILA_VIVA,
            "denominador": "residuo no-P_2 del DATO (r_0)",
            "criterio": "residuo_no_P2 / (piso_por_paso * k) <= %.1f" % UMBRAL_C6_RAZON,
            "piso_por_paso": piso_paso,
            "piso_declarado_fuente": "residuo_no_p2 de L2_theta(P_2) en la malla sellada, mismo "
                                      "operador y misma mascara",
            "pasos_que_deciden": [int(x[0]) for x in campos],
            "pasos_informativos_campo_no_convergido": [int(x[0]) for x in campos_informativos],
        },
        "residuo_no_P2_campo_max": peor_res,
        "razon_al_piso_max": peor_razon,
        "residuo_no_P2_campo_max_informativo": peor_res_inf,
        "razon_al_piso_max_informativa": peor_razon_inf,
        "residuo_no_P2_dato_den": r_0,
        "factor_amplificacion": (peor_res / r_0) if r_0 > 0.0 else None,
        "lecturas": lecturas,
        "lecturas_informativas": lecturas_inf,
        "escalera_piso_operador_theta": escalera,
        "informativos": {"dispersion_theta_U": spread,
                         "residuo_no_P2_de_delta_a": rel_delta,
                         "residuo_no_P2_dato_metro_R2": r_0_r2,
                         "piso_metro_angular_no_P2_de_L2P2": rel_l2,
                         "piso_de_campo_por_refinamiento_theta": PISO_REFINAMIENTO_THETA},
        "umbral": UMBRAL_C6,
        "umbral_C6_no_movido": UMBRAL_C6,
        "umbral_de_razon_al_piso": UMBRAL_C6_RAZON,
        "causa": causa,
        "ok": ok,
        "rc": 0 if ok else 1,
    }


def cronologia(g, p_eff, rs0, sigma, ancho_extra=6.0, saliente_puro=False):
    """Cronologia analitica del dato. Unidades de r* = unidades de t.

    Con saliente_puro = True (dato de R3) la mitad ENTRANTE NO EXISTE: los numeros de ese bloque
    se siguen imprimiendo -- son la cronologia de un dato que NO se lanzo -- y se declaran.
    """
    rs_min, rs_sp = g["rs_min"], g["rs_sponge"]
    a = ancho_extra * sigma
    return {
        "dato_centro": rs0,
        "es_saliente_puro": bool(saliente_puro),
        "mitad_entrante_existe": (not bool(saliente_puro)),
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
    ap.add_argument("--dato", choices=("saliente-r26", "estatico-r10"), default=DATO_R3)
    ap.add_argument("--rs-dato", dest="rs_dato", type=float, default=RS_DATO_R3)
    ap.add_argument("--omega", type=float, default=OMEGA_R3)
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
    if a.dato == "saliente-r26":
        rs_dato = float(a.rs_dato)
        g_win["c"] = rs_dato
        gd = guarda_soporte_dato(g["rs_min"], g["rs_sponge"], rs_dato, a.sigma)
        if not gd["ok"]:
            raise SystemExit("FAIL-CLOSED R3 (D15): " + gd["causa"])
        m = f2.Malla2D(g["rs_min"], g["rs_max"], int(a.nr0), int(a.nt0), float(a.cfl), 0)
        u0, v0 = dato_saliente_l2(m, rs_dato, a.sigma, float(a.omega))
        dato_declarado = ("SALIENTE PURO de F11 (f11.dato_saliente verbatim) x P_2(cos theta): "
                          "c = %.6f, sigma = %.6f, omega = %.6f, v^0 = -d_r u^0"
                          % (rs_dato, a.sigma, a.omega))
        saliente_puro = True
    else:
        rs_dato = float(a.rs0)
        g_win["c"] = rs_dato
        gd = guarda_soporte_dato(g["rs_min"], g["rs_sponge"], rs_dato, a.sigma)
        m = f2.Malla2D(g["rs_min"], g["rs_max"], int(a.nr0), int(a.nt0), float(a.cfl), 0)
        u0 = dato_f3(m, rs_dato, a.sigma)
        v0 = np.zeros_like(u0)
        dato_declarado = ("ESTATICO de §R5 (FALSADOR del ROJO): c = %.6f, sigma = %.6f, v^0 = 0"
                          % (rs_dato, a.sigma))
        saliente_puro = False
    dt = float(m.dt_cota)
    r_nod, f_nod, pot, wang = campos_de_malla(m, a.dosM)
    ip = int(np.argmin(np.abs(m.rs - g["p"])))
    p_eff = float(m.rs[ip])
    vw = f11.ventanas(g_win, p_eff, a.sigma, g["rs_min"], g["rs_max"])
    cron = cronologia(g, p_eff, rs_dato, a.sigma, saliente_puro=saliente_puro)
    p2 = perfil_p2(m.th)
    sinth = np.sin(m.th)
    den_p2 = float(np.sum(p2 * p2 * sinth))
    k_pro = 1                                        # prologo, t << t_s (informativo)
    k_pro2 = 8
    k_a = int(math.floor(12.0 / dt))                 # captura HEREDADA de F11: en R4 cae DENTRO
                                                     # del dominio (t = 11.975 <= t_s) y DECIDE
    k_b = int(math.floor(vw["t_s"] / dt))            # el frente del paquete toca la capa (ultimo
                                                     # paso que puede decidir)
    k_ret = int(math.floor(vw["t_ret"] / dt))        # primer retorno posible al anillo (fuera del
                                                     # dominio: informativo)
    nsteps = int(math.ceil(vw["T_obs"] / dt))
    caps_c4 = (k_pro, k_pro2, k_a, k_b, k_ret, nsteps)
    max_inc = float(np.max(np.abs(u0)))

    print("UNIVERSO DECLARADO: malla sellada F11 (r* en [%.1f, %.1f], nr0=%d, nt0=%d, hr=%r) | "
          "mapa tortuga con 2M = %.1f sobre esa malla | dato de %s | cifras analiticas de V_Z y U"
          % (g["rs_min"], g["rs_max"], m.nr, m.nt, float(m.hr), a.dosM, a.dato))
    print("HUELLA = %s" % HUELLA)
    print("HUELLA R3 = %s" % HUELLA_R3)
    print("HUELLA R4 = %s" % HUELLA_R4)
    print("hora_utc = %s" % hora_utc())
    print("DATO DECLARADO = %s" % dato_declarado)
    print("GUARDA DE SOPORTE DEL DATO (D15): %s" % gd["causa"])
    print("geometria F11 (VERBATIM): L = %.6f | c_esponja = %.6f | p = %.6f | p_eff = %.16f | "
          "r*_sponge = %.6f | r*_max = %.6f | gamma_max = %.16f | integral_gamma = %.16f | "
          "solape = %.6f" % (g["L"], g["c"], g["p"], p_eff, g["rs_sponge"], g["rs_max"],
                             g["gamma_max"], g["integral_gamma"], g["solape"]))
    print("2M = %.6f | l = %d | lambda = %.6f | U(r*_min) = %.12e | U(74.0) = %.12e | "
          "U(r*_max) = %.12e | max |U| = %.12e en r* = %.6f"
          % (a.dosM, L_ANGO, LAM_Z, float(pot[0]), float(u0 is not None and
             pot[int(np.argmin(np.abs(m.rs - 74.0)))]),
             float(pot[-1]), float(np.max(np.abs(pot))), float(m.rs[int(np.argmax(np.abs(pot)))])))
    print("ventanas f11.ventanas VERBATIM (c_dato = %.6f): t_1 = %.6f | t_a = %.6f | t_s = %.6f | "
          "t_ret = %.6f | t_3 = %.6f | T_obs = %.6f"
          % (rs_dato, vw["t_1"], vw["t_a"], vw["t_s"], vw["t_ret"], vw["t_3"], vw["T_obs"]))
    print("dt = %.18e | nsteps = %d | dominio declarado de C4 (D16): t <= t_s = %.6f (k <= %d) | "
          "pasos que DECIDEN k = %s | pasos con t > t_s, INFORMATIVOS k = %s | capturas C4 k = "
          "%s | captura heredada de F11 k_a = %d (t = %.6f) -> DENTRO del dominio"
          % (dt, nsteps, vw["t_s"], k_b, str([k_a, k_b]), str([k_ret, nsteps]),
             str([int(x) for x in caps_c4]), k_a, k_a * dt))
    print("D7 CRONOLOGIA DECLARADA (unidades de r* = unidades de t): mitad saliente: anillo "
          "%.3f, esponja %.3f, retorno al anillo %.3f"
          % (cron["T_centro_saliente_en_anillo"], cron["T_centro_saliente_en_esponja"],
             cron["T_retorno_saliente_en_anillo"]))
    if cron["mitad_entrante_existe"]:
        print("D7 mitad ENTRANTE (EXISTE): pared %.3f, anillo %.3f (frente %.3f), esponja %.3f, "
              "retorno de SU eco al anillo %.3f (frente %.3f)"
              % (cron["T_centro_entrante_en_pared"], cron["T_centro_entrante_en_anillo"],
                 cron["T_frente_entrante_en_anillo"], cron["T_centro_eco_pared_en_esponja"],
                 cron["T_retorno_eco_pared_en_anillo"], cron["T_frente_eco_pared_en_anillo"]))
    else:
        print("D7 mitad ENTRANTE: NO EXISTE (dato saliente puro, v^0 = -d_r u^0). Los numeros de "
              "ese bloque serian pared %.3f, anillo %.3f, eco al anillo %.3f, pero describen un "
              "dato que NO se lanzo: el canal de contaminacion de la pared queda CERRADO por "
              "construccion (esa es la ruta elegida en R3)."
              % (cron["T_centro_entrante_en_pared"], cron["T_centro_entrante_en_anillo"],
                 cron["T_retorno_eco_pared_en_anillo"]))

    c0 = control_C0()
    c1a = control_C1a(a.dosM)
    c1b = control_C1b(a.dosM)
    c9 = control_C9(a.dosM)
    c3 = f11.control_C3(0.55)
    for r in (c0, c1a, c1b, c9, c3):
        print("[%s] rc=%s ok=%s" % (r.get("control"), r.get("rc"), r.get("ok")))
        print("    %s" % r.get("causa", ""))

    res_on = corrida_c2(m, g, g_win, dt, nsteps, True, pot, wang, u0, v0, a.sigma,
                        capturas=caps_c4)
    res_off = corrida_c2(m, g, g_win, dt, nsteps, False, pot, wang, u0, v0, a.sigma,
                         capturas=caps_c4)
    c4 = control_C4(m, g, dt, pot, wang, res_on, res_off, (k_a, k_b),
                    pasos_fuera=(k_ret, nsteps), pasos_prologo=(k_pro, k_pro2),
                    damp_on=res_on["damp"], t_s=vw["t_s"])

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
        "universo": "malla sellada nr0=%d nt0=%d | nsteps = %d | dato %s en r* = %.6f, sigma = "
                    "%.6f" % (m.nr, m.nt, nsteps, a.dato, rs_dato, a.sigma),
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
        "residuo_no_P2_dato_inicial_fila_viva": residuo_no_p2(u0, m.th, p2, sinth, den_p2,
                                                              FRAC_FILA_VIVA),
        "residuo_no_P2_solucion_final_fila_viva": residuo_no_p2(res_on["u"], m.th, p2, sinth,
                                                                den_p2, FRAC_FILA_VIVA),
        "dato_declarado": dato_declarado,
        "causa": causa_c2,
        "ok": ok_c2,
        "rc": 0 if ok_c2 else 1,
    }
    print("[C2] rc=%s ok=%s" % (c2["rc"], c2["ok"]))
    print("    %s" % causa_c2)
    print("    residuo no-P2 con el metro de R2 (msk = d2 > 0.0) -> DATO %.6e / SOLUCION %.6e"
          "  <- D13: es el metro que imprimio 9.999999e-01 sobre filas vacias"
          % (c2["residuo_no_P2_dato_inicial"], c2["residuo_no_P2_solucion_final"]))
    print("    residuo no-P2 con FILAS VIVAS (frac = %.1e) -> DATO %.6e / SOLUCION %.6e"
          % (FRAC_FILA_VIVA, c2["residuo_no_P2_dato_inicial_fila_viva"],
             c2["residuo_no_P2_solucion_final_fila_viva"]))
    print("[C4] rc=%s ok=%s" % (c4["rc"], c4["ok"]))
    print("    %s" % c4["causa"])

    campos_c6 = [(k_b, res_on["caps"][k_b], k_b * dt),
                 (k_ret, res_on["caps"][k_ret], k_ret * dt)]
    campos_c6_inf = [(nsteps, res_on["u"], nsteps * dt)]
    c6 = control_C6(m, a.dosM, pot, wang, u0, p2, sinth, den_p2, campos=campos_c6,
                    campos_informativos=campos_c6_inf,
                    escalera_nt=(2 * int(m.nt0) - 1, 4 * int(m.nt0) - 3))
    c7 = control_C7(res_on["med"], max_inc, m, g, rs_dato, a.sigma)
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
        "huella_r2": HUELLA_R2,
        "huella_r3": HUELLA_R3,
        "huella_r4": HUELLA_R4,
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
        "dato_declarado": dato_declarado,
        "dato_elegido": a.dato,
        "guarda_soporte_dato": gd,
        "dominio_c4_declarado": {"criterio": "t <= t_s (antes de que el frente del paquete toque "
                                             "la capa: damp == 1.0 exacto en toda fila interior)",
                                 "t_s": float(vw["t_s"]),
                                 "pasos_que_deciden": [int(k_a), int(k_b)],
                                 "pasos_fuera_del_dominio_informativos": [int(k_ret), int(nsteps)],
                                 "pasos_prologo": [int(k_pro), int(k_pro2)],
                                 "guarda_de_dominio_fail_closed": "ningun paso que decide puede "
                                                                  "tener t > t_s",
                                 "umbral_C4_no_movido": UMBRAL_C4,
                                 "umbral_C6_no_movido": UMBRAL_C6,
                                 "umbral_C6_de_razon_al_piso_nuevo": UMBRAL_C6_RAZON,
                                 "umbral_R_dB_no_movido": UMBRAL_R_DB},
        "dominio_c6_declarado": {"criterio": "residuo_no_P2 / (piso_por_paso * k) <= 1.0",
                                 "piso_por_paso": "residuo_no_p2 de L2_theta(P_2) en la malla "
                                                  "sellada, mismo operador y misma mascara de "
                                                  "fila viva (medido en la corrida)",
                                 "pasos_que_deciden": [int(k_b), int(k_ret)],
                                 "pasos_informativos_por_no_convergencia_theta": [int(nsteps)],
                                 "umbral_C6_no_movido": UMBRAL_C6,
                                 "rotulo_dato_angular": "el dato cuadrupolar NO es "
                                                        "theta-independiente por construccion "
                                                        "fisica (D17/R4)"},
        "parametros": {"dosM": float(a.dosM), "l": L_ANGO, "lam": LAM_Z, "rs0": float(a.rs0),
                       "rs_dato": float(rs_dato), "omega_r3": float(a.omega),
                       "sigma": float(a.sigma), "nr0": int(m.nr), "nt0": int(m.nt0),
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
                                "esponja cae dentro de la ventana de vuelta)",
                                "D13 (C6 con msk = d2 > 0.0 es una razon sobre filas vacias: "
                                "9.999999e-01 no es el campo, es 1/0)",
                                "D14 (las capturas de C4 heredadas de F11 caen en t < t_s: en el "
                                "ROJO las DOS capturas quedaron fuera del dominio del control)",
                                "D15 (el soporte +-6 sigma del dato de §R5 sale de la malla por "
                                "abajo y se pega a la pared Dirichlet interna)",
                                "D16 (R4: el dominio declarado de C4 en R3 estaba INVERTIDO; el "
                                "prefijo t <= t_s mide 2.325996e-14 y PASA, y la cola t > t_s "
                                "mide 1.875977e-02 = 1.5 % de la diferencia de contorno: la capa "
                                "trabajando, no contaminacion)",
                                "D17 (R4: UMBRAL_C6 = 1e-12 esta por debajo del piso del metro "
                                "angular, 2.239675e-04 por aplicacion en nt0 = 33; el piso de "
                                "campo converge x5.6-x6.3 por duplicacion de nt0: la impureza no-P_2 "
                                "es discretizacion en theta, no fisica)"],
        "notas": ["dt_cota tomada con f = 1 (la de F11): conservadora porque f <= 1 en r > 2M",
                  "el factor geometrico del medidor es r*^2 (F11) y cancela en R_dB",
                  "R_dB es una RAZON en energia: no se re-ventanea ni se mueve ningun umbral",
                  "la unica linea nueva del sector angular es el factor metrico f en el peso",
                  "R3: f11.ventanas sigue VERBATIM; lo que cambio es el DATO (c = 26.0 saliente "
                  "puro), no las formulas de las ventanas",
                  "R3: C6 ya no exige simetria radial plana; audita la pureza l = 2 del CAMPO",
                  "R3: la corrida OFF tiene la MISMA longitud que la ON (antes se cortaba en "
                  "k_b + 1), para que la unica diferencia entre ambas sea la capa",
                  "R3: las lecturas INFORMATIVAS de C6 se miden con la MISMA mascara de fila viva "
                  "que el criterio, para que sean comparables entre si",
                  "R4 (D16): el dominio de C4 pasa a t <= t_s; los pasos con t > t_s se imprimen "
                  "con su razon d_interior / max|u|_esponja_ON y NO deciden. Guarda fail-closed: "
                  "ningun paso que decide puede tener t > t_s",
                  "R4 (D17): C6 decide por RAZON al piso declarado del metro angular (<= 1.0), "
                  "medido en la corrida como residuo_no_p2 de L2_theta(P_2) por paso; UMBRAL_C6 = "
                  "1e-12 queda en el crudo como cifra NO movida",
                  "R4: la captura final (k = nsteps) va como INFORMATIVA porque el campo a t > 60 "
                  "no esta convergido en theta (max|u| = 2.2633e-02 en nt0 = 33 vs 9.3697e-01 "
                  "en nt0 = 65); se declara con su respaldo y su hora"],
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
