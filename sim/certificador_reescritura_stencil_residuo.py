#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =========================================================================== #
# HUELLA-CERTIFICADOR-REESCRITURA-STENCIL-RESIDUO-20261013
# --------------------------------------------------------------------------- #
# Certificador SIMBOLICO del residuo de ecuacion modificada del stencil cubico
# (Lagrange, 4 nodos) de sim/driver_rw_zerilli_1d.py:218 -> cubic_stencil.
#
# SUSTRATO (unico): sim/PREREGISTRO_REESCRITURA_STENCIL_RESIDUO_20261013.md
#   Seccion 3  ecuacion modificada (via simbolica)
#   Seccion 4  contrato de aceptacion de orden (operador IDENTIDAD)
#   Seccion 5  control falsable obligatorio (must-fail)
#
# ADAPTACION DECLARADA (unica desviacion de la letra de la orden): la plantilla
# del dueno esta escrita para un operador DERIVADA (orden 0 = 0*u, orden 1 = 1*u').
# Este frente certifica el operador de EVALUACION / INTERPOLACION (la identidad I)
# => se lee con su propia convencion:
#   orden 0 -> 1*u     (exactamente 1: particion de la unidad)
#   orden 1 -> h*u'    (exactamente 0)
#   orden 2 -> h^2*u'' (exactamente 0)
#   orden 3 -> h^3*u''' (exactamente 0)
#   orden 4 -> PRIMER termino no nulo, coeficiente -prod(s-a)/24
#
# REGLA DE LA PUERTA: "exactamente 0" es CERO SIMBOLICO (simplify == 0), NO una
# tolerancia: una tolerancia aqui no mide nada (el objeto es algebraico).
#
# PREMISA DECLARADA: malla UNIFORME (h constante entre los 4 nodos). La
# normalizacion x0 = x_j + s*h exige h constante; con malla no uniforme el
# residuo NO es el de esta formula (no medido aqui).
#
# PROHIBICION (Seccion 6): prohibido extraer de este frente cualquier afirmacion
# sobre consistencia de Cauchy o estabilidad de arranque (t = 0): el residuo es
# del stencil ESPACIAL. Este frente NO mide eso.
#
# CERO CONTACTO: no importa, no ejecuta ni muta el arnes 2D, F11, Nodo 2 ni la
# malla hiperbolica. Solo importa sympy. NO escribe archivos.
#
# CODIGOS DE RETORNO (RC = ORDEN ESPURIO DETECTADO)
#   0  VERDE   primer termino no nulo en m = 4 (orden nominal p = 4)
#   1  RECHAZO termino espurio O(h^1)  (advectivo / error de fase)
#   2  RECHAZO termino espurio O(h^2)  (disipativo)
#   3  RECHAZO termino espurio O(h^3)  (dispersivo)
#   5  RECHAZO NORMA_ROTA (sum w != 1)
#   6  NO_CLASIFICABLE (primer termino no nulo en m > 4, o residuo nulo hasta MMAX)
#   8  NO_MEDIBLE (fallo interno del instrumento)
#   9  BANCO FALLIDO: el must-fail NO enrojecio como estaba pre-registrado
#      => el instrumento se declara INVALIDO (fail-closed)
#
# BANCO MUST-FAIL (eps = 1/1000, congelado antes de la primera cifra):
#   C0 (0, 0, 0, 0)   -> rc 0, primer_orden_no_nulo = ninguno < 5
#   E1 (1, -1, -1, 1) -> rc 2, primer_orden_no_nulo = 2
#   E2 (1, -3, 3, -1) -> rc 3, primer_orden_no_nulo = 3
#   E3 (1, 0, 0, -1)  -> rc 1, primer_orden_no_nulo = 1
# =========================================================================== #

from __future__ import annotations

import argparse
import json
import sys

import sympy as sp

HUELLA = "HUELLA-CERTIFICADOR-REESCRITURA-STENCIL-RESIDUO-20261013"
S = sp.Symbol("s")
NODOS = (0, 1, 2, 3)
P_NOMINAL = 4
MMAX = 8
S_MATERIALIZA = sp.Rational(1, 2)
EPS_MUST_FAIL = sp.Rational(1, 1000)

RC_VERDE = 0
RC_NORMA = 5
RC_NO_CLASIFICABLE = 6
RC_NO_MEDIBLE = 8
RC_BANCO_FALLIDO = 9

CAUSA_VERDE = "VERDE: ORDEN p = 4 CERTIFICADO (coef = -prod(s-a)/24)"
CAUSA_ESPURIA = {
    1: "RECHAZO: RESIDUO_DE_ORDEN_INFERIOR_DETECTADO (O(h^1) != 0)",
    2: "RECHAZO: RESIDUO_DISIPATIVO_DETECTADO (O(h^2) != 0)",
    3: "RECHAZO: RESIDUO_DISPERSIVO_DETECTADO (O(h^3) != 0)",
}

CONTROLES = (
    ("C0", "positivo (sin perturbacion)", (0, 0, 0, 0)),
    ("E1", "disipativo (par, u'')", (1, -1, -1, 1)),
    ("E2", "dispersivo (impar, u''')", (1, -3, 3, -1)),
    ("E3", "advectivo (impar, u')", (1, 0, 0, -1)),
)
ESPERADO_MUST_FAIL = {"C0": (0, None), "E1": (2, 2), "E2": (3, 3), "E3": (1, 1)}

LINEA_UNIVERSO = (
    "UNIVERSO DECLARADO: operador I = cubic_stencil (Lagrange, 4 nodos 0..3) sobre u suave; "
    "malla UNIFORME (h constante); s simbolica generica; eps_must_fail = 1/1000; "
    "controles = {C0, E1, E2, E3}; casa = sim/; motor = python3 -B + sympy."
)


def pesos_lagrange():
    """Pesos de Lagrange de 4 nodos en la variable normalizada (x0 = x_j + s*h)."""
    pesos = []
    for a in NODOS:
        num = sp.Integer(1)
        den = sp.Integer(1)
        for b in NODOS:
            if b != a:
                num *= (S - b)
                den *= (a - b)
        pesos.append(sp.simplify(num / den))
    return pesos


def momentos(pesos, mmax=MMAX):
    """mu_m(s) = sum_a w_a(s) * a^m  (Seccion 3)."""
    return [
        sp.simplify(sum(pesos[a] * NODOS[a] ** m for a in range(4)))
        for m in range(mmax + 1)
    ]


def veredicto(pesos):
    """Contrato de la Seccion 4. Devuelve (rc, causa, traza, m_lider).

    La identidad se mide SIMBOLICAMENTE en s (no en un s puntual): "exactamente 0"
    significa cero simbolico.
    """
    traza = {"huella": HUELLA, "nodos": list(NODOS), "p_nominal": P_NOMINAL,
             "eps_must_fail": str(EPS_MUST_FAIL)}

    suma = sp.simplify(sum(pesos))
    traza["sum_w"] = str(suma)
    if suma != 1:
        return RC_NORMA, "RECHAZO: NORMA_ROTA (sum w != 1)", traza, None

    mus = momentos(pesos)
    traza["w"] = [str(x) for x in pesos]
    traza["mu"] = [str(x) for x in mus[:5]]

    # Ordenes 0..3: CERO SIMBOLICO exigido.
    for m in range(0, P_NOMINAL):
        dif = sp.simplify(mus[m] - S ** m)
        traza["mu%d_menos_s%d" % (m, m)] = str(dif)
        if dif != 0:
            if m in CAUSA_ESPURIA:
                return m, CAUSA_ESPURIA[m], traza, m
            return (RC_NO_CLASIFICABLE,
                    "NO_CLASIFICABLE: termino espurio en m=%d" % m, traza, m)

    # Primer termino no nulo con m >= 4.
    m_lider = None
    dif_lider = None
    for m in range(P_NOMINAL, MMAX + 1):
        dif = sp.simplify(mus[m] - S ** m)
        traza["mu%d_menos_s%d" % (m, m)] = str(dif)
        if dif != 0:
            m_lider = m
            dif_lider = dif
            break

    if m_lider is None:
        return (RC_NO_CLASIFICABLE,
                "NO_CLASIFICABLE: residuo identicamente nulo hasta m=%d" % MMAX,
                traza, None)

    coef = sp.simplify(dif_lider / sp.factorial(m_lider))
    traza["orden"] = m_lider
    traza["coef_lider"] = str(coef)

    if m_lider != P_NOMINAL:
        return (RC_NO_CLASIFICABLE,
                "NO_CLASIFICABLE: primer termino no nulo en m=%d (> p=%d)" % (m_lider, P_NOMINAL),
                traza, m_lider)

    esperado = -sp.prod([S - a for a in NODOS]) / sp.factorial(P_NOMINAL)
    coincide = sp.simplify(coef - esperado) == 0
    traza["coef_esperado_forma_cerrada"] = str(esperado)
    traza["coincide_forma_cerrada"] = bool(coincide)
    if not coincide:
        return (RC_NO_CLASIFICABLE,
                "NO_CLASIFICABLE: coef lider != -prod(s-a)/24", traza, m_lider)

    # Cross-check del sustrato (Seccion 3): (mu_4 - s^4) + prod(s-a) == 0.
    traza["cross_check_sustrato"] = bool(
        sp.simplify((mus[4] - S ** 4) + sp.prod([S - a for a in NODOS])) == 0
    )
    return RC_VERDE, CAUSA_VERDE, traza, m_lider


def firma_control(delta):
    """delta_mu_m ESCALADO por eps: eps * sum_a delta_a * a^m (Seccion 5)."""
    return [
        sp.simplify(EPS_MUST_FAIL * sum(delta[a] * NODOS[a] ** m for a in range(4)))
        for m in range(0, 5)
    ]


def primer_no_nulo(vec):
    for m, v in enumerate(vec):
        if v != 0:
            return m
    return None


def pesos_perturbados(base, delta):
    return [sp.simplify(base[a] + EPS_MUST_FAIL * delta[a]) for a in range(4)]


def correr_must_fail():
    base = pesos_lagrange()
    filas = []
    vector = []
    banco_ok = True
    for nombre, descripcion, delta in CONTROLES:
        rc, causa, traza, m_lider = veredicto(pesos_perturbados(base, delta))
        firma = firma_control(delta)
        pnn = primer_no_nulo(firma)
        esperado = ESPERADO_MUST_FAIL[nombre]
        coincide_pre_registro = (rc, pnn) == esperado
        if not coincide_pre_registro:
            banco_ok = False
        filas.append({
            "control": nombre,
            "delta": descripcion,
            "delta_vector": list(delta),
            "delta_mu": [str(x) for x in firma],
            "primer_orden_no_nulo": pnn,
            "rc": rc,
            "causa": causa,
            "orden_lider": m_lider,
            "esperado_pre_registro": {"rc": esperado[0], "primer_orden_no_nulo": esperado[1]},
            "coincide_pre_registro": bool(coincide_pre_registro),
        })
        vector.append(rc)
    return filas, vector, banco_ok


def informe_base(s_materializa=S_MATERIALIZA, como_json=False):
    pesos = pesos_lagrange()
    rc, causa, traza, m_lider = veredicto(pesos)
    par_simbolico = (traza.get("orden"), traza.get("coef_lider"))
    coef_expr = sp.sympify(traza["coef_lider"]) if "coef_lider" in traza else None
    coef_en_s = sp.simplify(coef_expr.subs(S, s_materializa)) if coef_expr is not None else None
    residuo_en_s = sp.simplify((coef_expr * S ** 4).subs(S, s_materializa)) if coef_expr is not None else None
    informe = {
        "huella": HUELLA,
        "modo": "base",
        "universo": LINEA_UNIVERSO,
        "premisa_malla": "UNIFORME (h constante entre los 4 nodos)",
        "adaptacion_declarada": "operador IDENTIDAD (1*u / 0*u' / 0*u'' / 0*u''')",
        "s_materializa": str(s_materializa),
        "par_simbolico": [par_simbolico[0], par_simbolico[1]],
        "coef_lider_en_s": str(coef_en_s),
        "rc": rc,
        "causa": causa,
        "traza": traza,
    }
    if como_json:
        print(json.dumps(informe, ensure_ascii=False, indent=2, sort_keys=True))
        return rc

    print(LINEA_UNIVERSO)
    print("huella = %s" % HUELLA)
    print("modo = base (identidad simbolica, s generica)")
    print("premisa = malla UNIFORME (h constante entre los 4 nodos)")
    print("sum_w = %s" % traza.get("sum_w"))
    for m in range(0, P_NOMINAL):
        print("mu_%d - s^%d = %s" % (m, m, traza.get("mu%d_menos_s%d" % (m, m))))
    print("orden_detectado = %s" % traza.get("orden"))
    print("PAR (orden | coef_lider) = (%s | %s)   [identidad simbolica en s]"
          % (traza.get("orden"), traza.get("coef_lider")))
    print("coef_esperado_forma_cerrada = %s" % traza.get("coef_esperado_forma_cerrada"))
    print("coincide_forma_cerrada = %s" % traza.get("coincide_forma_cerrada"))
    print("PAR en s = %s  = (%s | %s)"
          % (s_materializa, traza.get("orden"), coef_en_s))
    print("cross_check_sustrato = %s" % traza.get("cross_check_sustrato"))
    print("rc = %d" % rc)
    print("causa = %s" % causa)
    if residuo_en_s == 0:
        print("BORDE DECLARADO: coef_lider(s = %s) = 0 -> interpolacion exacta en nodo; "
              "NO se reclama orden 4 en s entero." % s_materializa)
    return rc


def informe_must_fail(como_json=False):
    filas, vector, banco_ok = correr_must_fail()
    if como_json:
        print(json.dumps({"huella": HUELLA, "modo": "must-fail", "universo": LINEA_UNIVERSO,
                          "eps_must_fail": str(EPS_MUST_FAIL), "filas": filas,
                          "vector_rc": vector, "banco_ok": bool(banco_ok)},
                         ensure_ascii=False, indent=2, sort_keys=True))
        return RC_VERDE if banco_ok else RC_BANCO_FALLIDO

    print(LINEA_UNIVERSO)
    print("huella = %s" % HUELLA)
    print("modo = must-fail (eps = %s, congelado antes de la primera cifra)" % EPS_MUST_FAIL)
    print("control  delta                         rc  primer_orden_no_nulo  causa")
    for fila in filas:
        print("%-8s %-29s %-3d %-21s %s"
              % (fila["control"], str(fila["delta_vector"]), fila["rc"],
                 ("ninguno<5" if fila["primer_orden_no_nulo"] is None
                  else str(fila["primer_orden_no_nulo"])), fila["causa"]))
    print("firmas (eps * sum_a delta_a a^m):")
    for fila in filas:
        print("  %s d0=%s d1=%s d2=%s d3=%s"
              % (fila["coincide_pre_registro"] and fila["control"] or fila["control"],
                 fila["delta_mu"][0], fila["delta_mu"][1],
                 fila["delta_mu"][2], fila["delta_mu"][3]))
    print("VECTOR RC = C0:%d E1:%d E2:%d E3:%d" % tuple(vector))
    print("vector esperado = C0:0 E1:2 E2:3 E3:1 (pre-registrado)")
    if banco_ok:
        print("BANCO OK: el metro distingue orden 4 de orden < 4, con causa tipada en los 4 casos.")
        return RC_VERDE
    print("BANCO FALLIDO: el control sembrado NO enrojecio como estaba pre-registrado; "
          "el instrumento se declara INVALIDO (fail-closed).")
    return RC_BANCO_FALLIDO


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Certificador simbolico del residuo de ecuacion modificada de cubic_stencil.")
    ap.add_argument("--must-fail", action="store_true",
                    help="corre el banco C0/E1/E2/E3 y reporta vector de RC y causas tipadas")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    ap.add_argument("--s", default=str(S_MATERIALIZA),
                    help="s a la que se materializa el PAR (racional, por ejemplo 1/2)")
    args = ap.parse_args(argv)

    try:
        s_materializa = sp.Rational(args.s)
    except Exception:
        print("NO_MEDIBLE: s no racional '%s'" % args.s, file=sys.stderr)
        return RC_NO_MEDIBLE

    if args.must_fail:
        return informe_must_fail(como_json=args.json)
    return informe_base(s_materializa=s_materializa, como_json=args.json)


if __name__ == "__main__":
    sys.exit(main())
