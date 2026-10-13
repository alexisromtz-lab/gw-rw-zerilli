#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# HUELLA-DRIVER-RW-ZERILLI-2D-AXISIMETRICO-20261013
"""
BANCO 2D AXISIMETRICO (r*, theta) -- DRIVER LEAPFROG EN COORDENADA DE TORTUGA
=============================================================================

HUELLA-DRIVER-RW-ZERILLI-2D-AXISIMETRICO-20261013

UNIVERSO DECLARADO : este archivo (1 pieza) + sim/PREREGISTRO_FRENTE_2D_CQG_20261013.md (1 pieza,
                     blob 2b2dd0fa) + sim/ADENDA_1_RATIFICACION_SECCION_4_Y_ESQUEMA_2D_RATIFICADO_20261013.md
                     (1 pieza, blob 94aa523d). Total 3 piezas del frente.
MOTOR              : numpy + scipy (spherical_jn). Sin red, sin aleatoriedad, sin estado oculto:
                     el mismo argv produce el mismo crudo.
UNIDAD             : nodo / celda / paso temporal / linea / encabezado.
VENTANA            : reloj UTC impreso en la cabecera del crudo.

Ecuacion maestra RATIFICADA (adenda 1, R1/R2/R3; m = 0, f = 1 - 2M/r):

    d2_t Psi = d2_{r*} Psi - (f/r^2) L2_theta Psi - (2M f/r^3) Psi
    L2_theta = -(1/sin t) d_t ( sin t d_t Psi )

Esquema: leapfrog escalonado (campo en n entero, velocidad en n+1/2) -- el mismo del banco 1D
certificado. Mallas radiales no anidadas hr_k = hr_0/2^k con offset d_k = k*hr_k/3.

Bordes angulares (R3):
  polo    t = 0    : L'Hopital discreto con paridad PAR  ->  L2 u|_0 = -4 (u_1 - u_0)/h^2
  ecuador t = pi/2 : NEUMANN d_t u = 0 por fantasma par (u_nt = u_nt-2) dentro de la forma de FLUJO.
  Control declarado: con u = P_2(cos t) el polo da 6 = l(l+1) EXACTO en el limite continuo y O(h^2)
  en la malla; el nodo ecuatorial da -3 = l(l+1) P_2(pi/2). Se mide contra la referencia analitica
  (externo al bucle), no contra una copia del propio operador.

Cota de paso (R2, LITERAL, evaluada en la celda peor del dominio):

    dt = CFL * [ 1/(dr*)^2 + max( 1/( r(r*)^2 (dtheta)^2 ) ) ]^(-1/2) ,  CFL <= 0.50

Se imprime el PAR: la cota ratificada (literal, sin f) y la cota del simbolo discreto (con f).
La ratificada manda y es <= la del simbolo fuera del horizonte, asi que se corre conservador.
DECLARADO: es una cota GLOBAL (un solo dt para todo el dominio) y por eso paga el radio mas chico de
la malla; con r* muy negativo el factor 1/r^2 crece y dt se encoge. No es defecto del simbolo: es el
precio declarado de la malla polar con dt global. La malla LOGARITMICA en r (que lo abarata) no entra
en este esqueleto: se propone, no se escribe.

GATES
  F1 (nombre del dueno: "Gate 2D-F1") = el nulo N-2D-0 sellado: espacio plano M = 0, V = 0, CFL
     constante. Publica su umbral CON SU DOMINIO (adenda 1, seccion 5), medido en el sandbox antes de
     disparar el gate:
       F1.a EXACTITUD  : dominio = dato independiente de theta (rama l = 0). Referencia EXTERNA: el
                         modo discreto del propio simbolo radial, con sin(xi/2) = lambda sin(k hr/2).
                         Umbral 1e-13. No es tautologia: la referencia es algebra, no el bucle.
       F1.b DISPERSION : dominio = perfil angular l = 2 vivo. Solucion manufacturada exacta
                         Psi = r j_2(omega r) P_2(cos t) cos(omega t), con ambos radios forzados.
                         NO se reclama exactitud: se mide ORDEN (>= 1.80) y su control negativo.
       F1.c PAR DE DOMINIO : (exacto ~1e-15 | vivo ~1e-2) impresos juntos. Un umbral sin su dominio
                         es un verde falso.
  F8 .. F14 : declarados, NO implementados aqui (abortan imprimiendo su umbral y su dominio).
       F8 usa subproceso al instrumento 1D CERTIFICADO: jamas una copia del bucle 1D en este archivo.
"""

import argparse
import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np

try:
    from scipy.special import spherical_jn
except Exception as exc:  # pragma: no cover
    raise SystemExit("FALLO FAIL-CLOSED: scipy requerido para la solucion manufacturada: %r" % (exc,))

HUELLA = "HUELLA-DRIVER-RW-ZERILLI-2D-AXISIMETRICO-20261013"

CFL_SELLADO = 0.50
EPS = 2.220446049250313e-16

# Cada umbral viaja CON SU DOMINIO (adenda 1, seccion 5). Un umbral sin dominio es un verde falso.
UMBRAL_F1A_EXACTO = 1.0e-13      # dominio: dato independiente de theta, M = 0, V = 0
ORDEN_MIN_F1B = 1.80             # dominio: perfil angular l = 2 vivo; NO es umbral de exactitud
CTRL_F1B_MIN = 1.0e-02           # el control (termino angular apagado) NO debe bajar de aqui

GATES_DECLARADOS = {
    "f8": ("N-2D-0 / nulo de reduccion 2D->1D", "umbral 1e-12; dominio: rama independiente de theta; "
           "comparador EXTERNO por subproceso al driver 1D certificado, nunca copia local del bucle"),
    "f9": ("orden del esquema 2D", "|p - 2| <= 0.15; dominio: interior, bordes radiales forzados"),
    "f10": ("fuga modal del enrejado angular", "falla si > -60 dB; dominio: m = 0 puro"),
    "f11": ("ley de la capa absorbente 2D", "re-medida; si diverge de la ley 1D -1.3936 mas alla del "
            "residuo 3.0 por ciento => DIVERGE y manda la ley 2D"),
    "f12": ("sobretono n = 1 contra Leaver", "|delta| > 5e-2 = divergencia declarada; dominio: "
            "extractor bloqueado"),
    "f13": ("sesgo parametrico a bajo SNR", "200 realizaciones; |sesgo| > 2 SE falla el titular; "
            "dominio: arnes bloqueado"),
    "f14": ("regularidad en los polos", "residuo en t = 0 y en t = pi/2; dominio: bordes R3 activos"),
}


# --------------------------------------------------------------------------------------------
# Reloj, identidad
# --------------------------------------------------------------------------------------------

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


def identidad_self(ruta):
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
        "cabezas_hash": (txt.count("\n#") if txt is not None else None),
    }


# --------------------------------------------------------------------------------------------
# Coordenada de tortuga: r*(r) y su inversa por Newton-Raphson (R4)
# --------------------------------------------------------------------------------------------

def rstar_of_r(r, M):
    r = np.asarray(r, dtype=float)
    return r + 2.0 * M * np.log(r / (2.0 * M) - 1.0)


def r_of_rstar_newton(rs, M, tol=1e-15, itmax=90):
    """r(r*) por Newton-Raphson, MONOTONA y verificada (R4).

        f(r)  = r + 2M ln(r/2M - 1) - r*
        f'(r) = r / (r - 2M)

    Arranque: r0 = r* si r* > 4M; si no, 2M (1 + exp(min(r*/2M, 40))).
    Verifica residuo, monotonia estricta y r > 2M. FAIL-CLOSED si algo no se cumple.
    Devuelve (r, info). Con M = 0 es identidad exacta, declarada.
    """
    rs = np.asarray(rs, dtype=float)
    if M == 0.0:
        return rs.copy(), {"metodo": "identidad (M = 0): r(r*) = r*", "iters": 0,
                           "resid_max": 0.0, "monotono": True, "r_sobre_2M_min": float("inf")}
    r = np.where(rs > 4.0 * M, rs, 2.0 * M * (1.0 + np.exp(np.minimum(rs / (2.0 * M), 40.0))))
    piso = 2.0 * M * (1.0 + 1.0e-15)
    iters = 0
    for _ in range(itmax):
        f = r + 2.0 * M * np.log(r / (2.0 * M) - 1.0) - rs
        paso = f / (r / (r - 2.0 * M))
        r = np.maximum(piso, r - paso)
        iters += 1
        if np.all(np.abs(paso) <= tol * np.maximum(1.0, np.abs(r))):
            break
    f = r + 2.0 * M * np.log(r / (2.0 * M) - 1.0) - rs
    info = {"metodo": "Newton-Raphson", "iters": int(iters),
            "resid_max": float(np.max(np.abs(f))),
            "monotono": bool(np.all(np.diff(r) > 0.0)) if r.size > 1 else True,
            "r_sobre_2M_min": float(np.min(r) / (2.0 * M))}
    if info["resid_max"] > 1.0e-9 or not info["monotono"]:
        raise SystemExit("FALLO FAIL-CLOSED: inversion de tortuga no verificada: %r" % (info,))
    return r, info


# --------------------------------------------------------------------------------------------
# Malla 2D y cota de paso
# --------------------------------------------------------------------------------------------

class Malla2D(object):
    """Malla axisimetrica (r*, theta), theta en [0, pi/2] con polo y ecuador como NODOS.

    Convencion de mallas NO ANIDADAS IDENTICA a la del banco 1D CERTIFICADO
    (build_mesh, driver_rw_zerilli_1d.py l.170): h_k = d0/2^k, offset delta_k = k*h_k/3
    (formula LITERAL sellada), n = floor((rsmax - rsmin - delta)/h) + 1, rs = rsmin + delta + h*arange(n).
    El dominio [rs_min+delta_k, ~rs_max] es el MISMO en los tres niveles: sin eso, el residuo de F1.b
    compara objetos distintos y el orden no se mide.
    Angular: nt_k = (nt_0 - 1)*2^k + 1 conserva [0, pi/2] con polo y ecuador como nodos.
    """

    def __init__(self, M, rs_min, rs_max, nr, nt, cfl, nivel=0):
        self.M = float(M)
        self.cfl = float(cfl)
        self.nivel = int(nivel)
        self.rs_min = float(rs_min)
        self.rs_max = float(rs_max)
        self.hr0 = (float(rs_max) - float(rs_min)) / float(nr - 1)
        self.nt0 = int(nt)
        self.hr = self.hr0 / (2.0 ** self.nivel)
        self.delta = self.nivel * self.hr / 3.0          # offset no anidado, formula literal
        self.nr = int(math.floor((self.rs_max - self.rs_min - self.delta) / self.hr)) + 1
        self.rs = self.rs_min + self.delta + self.hr * np.arange(self.nr)
        self.nt = (self.nt0 - 1) * (2 ** self.nivel) + 1
        self.th = np.linspace(0.0, 0.5 * np.pi, self.nt)
        self.hth = float(self.th[1] - self.th[0])
        self.r, self.info_tortuga = r_of_rstar_newton(self.rs, self.M)
        self.f = 1.0 - 2.0 * self.M / self.r
        self.w_ang = self.f / (self.r ** 2)              # (f/r^2)
        self.w_pot = 2.0 * self.M * self.f / (self.r ** 3)
        # cota LITERAL ratificada (sin f) y cota del simbolo (con f): se imprime el par
        a_r = 1.0 / self.hr ** 2
        a_th_rat = float(np.max(1.0 / (self.r ** 2 * self.hth ** 2)))
        a_th_rig = float(np.max(self.f / self.r ** 2)) / self.hth ** 2
        self.dt_rat = self.cfl / math.sqrt(a_r + a_th_rat)
        self.dt_rig = self.cfl / math.sqrt(a_r + a_th_rig)
        self.dt = self.dt_rat                            # MANDA la ratificada
        self.lam_r = self.dt / self.hr
        if self.cfl > CFL_SELLADO + 1e-12:
            raise SystemExit("FALLO FAIL-CLOSED: CFL %r > sellado %r" % (self.cfl, CFL_SELLADO))
        if self.dt > self.dt_rig * (1.0 + 1e-12):
            raise SystemExit("FALLO FAIL-CLOSED: la cota ratificada excede la del simbolo discreto.")

    def resumen(self):
        return {
            "M": self.M, "nivel": self.nivel,
            "nr": self.nr, "nt": self.nt,
            "hr": self.hr, "hr0": self.hr0, "offset_delta": self.delta,
            "hth": self.hth, "rs_min": float(self.rs[0]), "rs_max": float(self.rs[-1]),
            "r_min": float(self.r[0]), "r_max": float(self.r[-1]),
            "cfl": self.cfl, "dt": self.dt,
            "dt_cota_ratificada_literal": self.dt_rat,
            "dt_cota_simbolo_con_f": self.dt_rig,
            "cota_ratificada_es_menor_o_igual": bool(self.dt_rat <= self.dt_rig * (1.0 + 1e-12)),
            "lam_r": self.lam_r,
            "tortuga": self.info_tortuga,
            "nota_cota": "cota GLOBAL: un solo dt paga el radio mas chico de la malla",
        }


# --------------------------------------------------------------------------------------------
# Operador angular (R3) y laplaciano radial
# --------------------------------------------------------------------------------------------

def L2_theta(u, th, hth):
    """L2_theta u = -(1/sin t) d_t ( sin t d_t u ) en forma de FLUJO conservativa.

    j = 0 (polo)     : -4 (u_1 - u_0)/h^2           (L'Hopital discreto, paridad PAR)
    j = nt-1 (ecuador): fantasma par u_nt = u_nt-2; sin(t_{eq+-1/2}) = cos(h/2) los DOS,
                        y el flujo NO se anula: da -2 cos(h/2)(u_eq-1 - u_eq)/h^2.
    """
    nr, nt = u.shape
    out = np.zeros_like(u)
    sh_menos = np.sin(th - 0.5 * hth)
    sh_mas = np.sin(th + 0.5 * hth)
    u_mas = np.empty((nr, nt))
    u_mas[:, :-1] = u[:, 1:]
    u_mas[:, -1] = u[:, -2]                 # j = nt-1 -> u_nt := u_nt-2  (Neumann par)
    interior = (sh_mas[1:] * (u_mas[:, 1:] - u[:, 1:])
                - sh_menos[1:] * (u[:, 1:] - u[:, :-1])) / hth ** 2
    out[:, 1:] = -interior / np.sin(th[1:])
    out[:, 0] = -4.0 * (u[:, 1] - u[:, 0]) / hth ** 2
    return out


def d2r_en_rstar(u, hr):
    """Segunda diferencia centrada en r*. Los dos nodos extremos quedan en 0: los fuerza el borde."""
    out = np.zeros_like(u)
    out[1:-1, :] = (u[2:, :] - 2.0 * u[1:-1, :] + u[:-2, :]) / hr ** 2
    return out


def aceleracion(malla, u, nulo_ang=False):
    """d2_t u segun la ecuacion ratificada (parte espacial)."""
    a = d2r_en_rstar(u, malla.hr)
    if not nulo_ang:
        a = a - malla.w_ang[:, None] * L2_theta(u, malla.th, malla.hth)
    a = a - malla.w_pot[:, None] * u
    return a


def certifica_L2(malla):
    """Certifica R3 contra la referencia ANALITICA externa P_2(cos t): L2 P_2 = 6 P_2.

    Devuelve residuo relativo, la fila del nodo peor, el error en el polo y el error en el ecuador.
    """
    th = malla.th
    p2 = 0.5 * (3.0 * np.cos(th) ** 2 - 1.0)
    u = np.tile(p2, (malla.nr, 1))
    r = L2_theta(u, th, malla.hth)
    ref = 6.0 * u
    err = np.abs(r - ref)
    escala = float(np.max(np.abs(ref)))
    j = int(np.argmax(err.max(axis=0)))
    return {
        "referencia": "analitica externa: L2 P_2 = l(l+1) P_2 = 6 P_2",
        "residuo_rel_max": float(err.max() / escala),
        "nodo_peor_t": float(th[j]),
        "error_polo_rel": float(err[:, 0].max() / escala),
        "error_ecuador_rel": float(np.abs(r[:, -1] + 3.0).max() / 3.0),
        "nt": malla.nt, "hth": malla.hth,
        "nota": "orden espacial O(h^2); el polo da 6 = l(l+1) exacto en el limite continuo",
    }


# --------------------------------------------------------------------------------------------
# Bucle (arrastrar-luego-patear) y verificaciones F1
# --------------------------------------------------------------------------------------------

def corre(malla, u0, v0, nsteps, forzador=None, ref=None, cheqs=(), nulo_ang=False):
    """Bucle ARRASTRAR-LUEGO-PATEAR escalonado.

    forzador(n, u) fuerza los dos bordes RADIALES con la referencia exacta (Dirichlet).
    Si ref no es None, se mide el residuo relativo max|u - ref(n)| / max|ref(n)| en los cheqs.
    """
    u = np.array(u0, dtype=float)
    v = np.array(v0, dtype=float)
    dt = malla.dt
    if forzador is not None:
        forzador(0, u)
    cheqs = set(int(c) for c in cheqs)
    resid = []
    for n in range(int(nsteps)):
        v = v + dt * aceleracion(malla, u, nulo_ang=nulo_ang)
        u = u + dt * v
        if forzador is not None:
            forzador(n + 1, u)
        if (n + 1) in cheqs and ref is not None:
            e = ref(n + 1)
            num = float(np.max(np.abs(u - e)))
            den = max(float(np.max(np.abs(e))), 1e-300)
            resid.append({"n": n + 1, "t": (n + 1) * dt, "residuo_rel": num / den})
    return u, v, resid


def f1a_modo_discreto(malla, T, celdas_media_onda):
    """F1.a EXACTITUD -- dominio: dato independiente de theta (rama l = 0).

    Dato: u_j^n = cos(k (r_j - r_0)) cos(xi n), con sin(xi/2) = lam_r sin(k hr/2).
    Referencia EXTERNA (algebra, no el bucle). Los bordes radiales se fuerzan con la MISMA formula:
    el modo discreto satisface la recursion interior EXACTAMENTE, asi que el residuo es redondeo.
    """
    k = (2.0 * math.pi / float(celdas_media_onda)) / malla.hr
    lam = malla.lam_r
    sin_media = lam * math.sin(k * malla.hr / 2.0)
    if abs(sin_media) >= 1.0:
        raise SystemExit("FALLO FAIL-CLOSED: modo no propagante (sin(xi/2) = %r)" % (sin_media,))
    xi = 2.0 * math.asin(sin_media)
    r0 = float(malla.rs[0])
    base = np.cos(k * (malla.rs - r0))[:, None] * np.ones((malla.nr, malla.nt))
    nsteps = int(round(float(T) / malla.dt))

    def ref(n):
        return base * math.cos(xi * n)

    u0 = ref(0)
    # v esta escalonada en n-1/2: v^{-1/2} = (u^0 - u^{-1})/dt = (1 - cos xi)/dt
    v0 = base * (1.0 - math.cos(xi)) / malla.dt

    def forzador(n, u):
        e = ref(n)
        u[0, :] = e[0, :]
        u[-1, :] = e[-1, :]

    cheqs = sorted(set([nsteps // 4, nsteps // 2, (3 * nsteps) // 4, nsteps]))
    u, v, resid = corre(malla, u0, v0, nsteps, forzador=forzador, ref=ref, cheqs=cheqs)
    rmax = max(r["residuo_rel"] for r in resid) if resid else float("nan")
    return {
        "dominio": "dato independiente de theta (rama l = 0), M = 0, V = 0",
        "celdas_media_onda": float(celdas_media_onda), "k_hr": k * malla.hr,
        "xi": xi, "lam_r": lam, "nsteps": nsteps,
        "referencia": "modo discreto del simbolo radial (algebra externa al bucle)",
        "cheqs": resid, "residuo_rel_max": rmax,
        "umbral": UMBRAL_F1A_EXACTO,
        "veredicto": "VERDE" if (rmax <= UMBRAL_F1A_EXACTO) else "ROJO",
    }


def _manufacturada(r, th, t, omega):
    R, T = np.meshgrid(r, th, indexing="ij")
    p2 = 0.5 * (3.0 * np.cos(T) ** 2 - 1.0)
    return (R * spherical_jn(2, omega * R)) * p2 * math.cos(omega * t)


def f1b_manufacturada(malla_base, T, omega, niveles, nulo_ang=False):
    """F1.b DISPERSION -- dominio: perfil angular l = 2 vivo.

    Solucion manufacturada exacta de la ecuacion CON termino angular:
        Psi = r j_2(omega r) P_2(cos t) cos(omega t)
    porque A(r) = r j_2(omega r) cumple A'' + (omega^2 - 6/r^2) A = 0 y L2 P_2 = 6 P_2.
    No es tautologia: la referencia es la solucion exacta de la ecuacion, no el esquema.
    """
    filas = []
    for nivel in range(int(niveles)):
        m = Malla2D(malla_base.M, malla_base.rs_min, malla_base.rs_max, malla_base.nr,
                    malla_base.nt0, malla_base.cfl, nivel=nivel)
        nsteps = int(round(float(T) / m.dt))

        def ref(n, _m=m):
            return _manufacturada(_m.r, _m.th, n * _m.dt, omega)

        u0 = ref(0)
        v0 = (_manufacturada(m.r, m.th, m.dt, omega) - _manufacturada(m.r, m.th, 0.0, omega)) / m.dt

        def forzador(n, u, _m=m):
            e = _manufacturada(_m.r, _m.th, n * _m.dt, omega)
            u[0, :] = e[0, :]
            u[-1, :] = e[-1, :]

        cheqs = sorted(set([nsteps // 2, nsteps]))
        u, v, resid = corre(m, u0, v0, nsteps, forzador=forzador, ref=ref, cheqs=cheqs,
                            nulo_ang=nulo_ang)
        rmax = max(r["residuo_rel"] for r in resid) if resid else float("nan")
        filas.append({"nivel": nivel, "nr": m.nr, "nt": m.nt, "hr": m.hr, "hth": m.hth,
                      "dt": m.dt, "nsteps": nsteps, "residuo_rel_max": rmax,
                      "cheqs": resid, "malla": m.resumen()})
    ordenes = []
    for a, b in zip(filas[:-1], filas[1:]):
        ra, rb = a["residuo_rel_max"], b["residuo_rel_max"]
        if ra > 0.0 and rb > 0.0:
            ordenes.append({"par": [a["nivel"], b["nivel"]],
                            "orden": math.log(ra / rb) / math.log(2.0)})
    p_min = min([o["orden"] for o in ordenes], default=float("nan"))
    return {
        "dominio": "perfil angular l = 2 VIVO; no se reclama exactitud, solo orden",
        "omega": float(omega), "T": float(T),
        "referencia": "solucion manufacturada exacta r j_2(omega r) P_2(cos t) cos(omega t)",
        "nulo_ang": bool(nulo_ang),
        "filas": filas, "ordenes": ordenes,
        "orden_min": p_min, "orden_min_exigido": ORDEN_MIN_F1B,
        "veredicto": ("VERDE" if (p_min >= ORDEN_MIN_F1B) else "ROJO") if not nulo_ang
        else ("CONTROL-OK" if p_min < ORDEN_MIN_F1B else "CONTROL-ROJO"),
    }


# --------------------------------------------------------------------------------------------
# Crudo y salida
# --------------------------------------------------------------------------------------------

def imprime_par_dominio(universo, motor, unidad, ventana, res_f1a, res_f1b, res_ctrl, cert):
    print("UNIVERSO DECLARADO: %s" % universo)
    print("MOTOR: %s" % motor)
    print("UNIDAD: %s" % unidad)
    print("VENTANA: %s" % ventana)
    print("HUELLA: %s" % HUELLA)
    print("--- F1.c PAR DE DOMINIO (umbral sin su dominio = verde falso) ---")
    print("  exacto (rama l = 0, angular inerte) : % .6e   [umbral % .1e]" %
          (res_f1a["residuo_rel_max"], UMBRAL_F1A_EXACTO))
    print("  vivo   (perfil l = 2 en la malla 0)  : % .6e   [orden min % .4f]" %
          (res_f1b["filas"][0]["residuo_rel_max"], res_f1b["orden_min"]))
    print("  control negativo (angular APAGADO)   : % .6e" % (res_ctrl["filas"][0]["residuo_rel_max"],))
    print("--- certificacion del operador angular (R3) contra P_2 analitico ---")
    for k in ("residuo_rel_max", "error_polo_rel", "error_ecuador_rel", "nodo_peor_t"):
        print("  %-20s : % .6e" % (k, cert[k]) if isinstance(cert[k], float)
              else "  %-20s : %s" % (k, cert[k]))


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Banco 2D axisimetrico (r*, theta) en tortuga. "
                                             "Huella %s" % HUELLA)
    ap.add_argument("--gate", default="f1",
                    choices=["f1", "f8", "f9", "f10", "f11", "f12", "f13", "f14", "listar"])
    ap.add_argument("--M", type=float, default=0.0)
    ap.add_argument("--rs-min", type=float, default=2.0)
    ap.add_argument("--rs-max", type=float, default=14.0)
    ap.add_argument("--nr", type=int, default=97)
    ap.add_argument("--nt", type=int, default=17)
    ap.add_argument("--cfl", type=float, default=CFL_SELLADO)
    ap.add_argument("--T", type=float, default=20.0)
    ap.add_argument("--omega", type=float, default=1.0)
    ap.add_argument("--celdas-media-onda", type=float, default=6.0)
    ap.add_argument("--niveles-f1b", type=int, default=3)
    ap.add_argument("--potencial", default="ratificado", choices=["ratificado", "nulo"])
    ap.add_argument("--json", action="store_true", help="imprime el crudo JSON en la salida")
    ap.add_argument("--out-json", default=None, help="ruta del crudo (por defecto sim/data/)")
    ap.add_argument("--estricto", action="store_true", help="devuelve 1 si algun gate falla")
    args = ap.parse_args(argv)

    t0 = time.time()
    ventana = utc_now()
    universo = ("este archivo (1 pieza) + sim/PREREGISTRO_FRENTE_2D_CQG_20261013.md (1 pieza) + "
                "sim/ADENDA_1_RATIFICACION_SECCION_4_Y_ESQUEMA_2D_RATIFICADO_20261013.md (1 pieza)")
    motor = "numpy %s + scipy (spherical_jn); sin red, sin aleatoriedad" % (np.__version__,)
    unidad = "nodo / celda / paso temporal / linea / encabezado"

    if args.gate == "listar":
        print("UNIVERSO DECLARADO: %s" % universo)
        for k in sorted(GATES_DECLARADOS):
            desc, dom = GATES_DECLARADOS[k]
            print("  %-4s %s :: %s" % (k, desc, dom))
        return 0

    if args.gate != "f1":
        desc, dom = GATES_DECLARADOS[args.gate]
        print("UNIVERSO DECLARADO: %s" % universo)
        print("GATE %s NO IMPLEMENTADO en este esqueleto (aborta fail-closed)." % args.gate.upper())
        print("  objeto : %s" % desc)
        print("  umbral y dominio : %s" % dom)
        print("  motivo : el frente de reflexion y el extractor estan BLOQUEADOS por orden del dueno.")
        return 3

    malla = Malla2D(args.M, args.rs_min, args.rs_max, args.nr, args.nt, args.cfl)
    if args.potencial == "nulo":
        malla.w_pot = np.zeros_like(malla.w_pot)

    cert = certifica_L2(malla)
    res_f1a = f1a_modo_discreto(malla, args.T, args.celdas_media_onda)
    res_f1b = f1b_manufacturada(malla, args.T, args.omega, args.niveles_f1b, nulo_ang=False)
    res_ctrl = f1b_manufacturada(malla, args.T, args.omega, 1, nulo_ang=True)
    ctrl_bajo = res_ctrl["filas"][0]["residuo_rel_max"] >= CTRL_F1B_MIN

    veredicto = {
        "f1a_exactitud": res_f1a["veredicto"],
        "f1b_dispersion": res_f1b["veredicto"],
        "f1c_control_negativo_no_converge": bool(ctrl_bajo),
        "dominio_declarado": {"f1a": res_f1a["dominio"], "f1b": res_f1b["dominio"]},
    }
    todo_verde = (res_f1a["veredicto"] == "VERDE" and res_f1b["veredicto"] == "VERDE" and ctrl_bajo)

    crudo = {
        "huella": HUELLA,
        "utc": ventana,
        "argv": list(sys.argv[1:] if argv is None else argv),
        "universo_declarado": universo,
        "motor": motor,
        "unidad": unidad,
        "identidad_self": identidad_self(os.path.abspath(__file__)),
        "gate": {"nombre": "Gate 2D-F1 (nombre del dueno)", "etiqueta_sellada": "N-2D-0",
                 "M": args.M, "potencial": args.potencial, "cfl": args.cfl,
                 "nota": "primera corrida obligatoria ANTES de inyectar el potencial de Schwarzschild"},
        "malla": malla.resumen(),
        "certificacion_L2_theta": cert,
        "f1a": res_f1a,
        "f1b": res_f1b,
        "f1b_control_angular_apagado": res_ctrl,
        "veredicto": veredicto,
        "todo_verde": bool(todo_verde),
        "segundos_muro": round(time.time() - t0, 3),
    }

    imprime_par_dominio(universo, motor, unidad, ventana, res_f1a, res_f1b, res_ctrl, cert)
    print("--- F1.a detalle ---")
    print("  dominio : %s" % res_f1a["dominio"])
    print("  xi = %.12e  lam_r = %.12e  nsteps = %d" % (res_f1a["xi"], res_f1a["lam_r"],
                                                         res_f1a["nsteps"]))
    for r in res_f1a["cheqs"]:
        print("    n = %6d  t = %8.3f  residuo_rel = % .6e" % (r["n"], r["t"], r["residuo_rel"]))
    print("  VEREDICTO F1.a: %s" % res_f1a["veredicto"])
    print("--- F1.b detalle (orden) ---")
    for f in res_f1b["filas"]:
        print("    nivel %d  nr = %4d  nt = %4d  hr = %.6f  hth = %.6f  dt = %.6e  residuo = % .6e"
              % (f["nivel"], f["nr"], f["nt"], f["hr"], f["hth"], f["dt"], f["residuo_rel_max"]))
    for o in res_f1b["ordenes"]:
        print("    orden %s -> %s : %.6f" % (o["par"][0], o["par"][1], o["orden"]))
    print("  orden_min = %.6f  (exigido >= %.4f)" % (res_f1b["orden_min"], ORDEN_MIN_F1B))
    print("  VEREDICTO F1.b: %s" % res_f1b["veredicto"])
    print("--- control negativo (angular APAGADO: no debe converger) ---")
    print("    residuo = % .6e   (piso exigido >= % .1e)  -> %s"
          % (res_ctrl["filas"][0]["residuo_rel_max"], CTRL_F1B_MIN,
             "OK" if ctrl_bajo else "FALLA"))
    print("VEREDICTO GLOBAL Gate 2D-F1 : %s" % ("VERDE" if todo_verde else "ROJO"))
    print("  F1.a %s | F1.b %s | control %s" % (veredicto["f1a_exactitud"],
                                                veredicto["f1b_dispersion"],
                                                "OK" if ctrl_bajo else "FALLA"))

    ruta_json = args.out_json
    if ruta_json is None:
        d = os.path.join(here, "data")
        if os.path.isdir(d):
            ruta_json = os.path.join(d, "crudo_2d_f1_%s.json" % ventana.replace(":", ""))
    if ruta_json:
        try:
            with open(ruta_json, "w", encoding="utf-8") as fh:
                json.dump(crudo, fh, indent=1, sort_keys=True)
            print("CRUDO: %s" % ruta_json)
        except OSError as exc:
            print("AVISO: no se pudo escribir el crudo: %r" % (exc,))
    if args.json:
        print("CRUDO_JSON: %s" % json.dumps(crudo, sort_keys=True))

    if args.estricto and not todo_verde:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
