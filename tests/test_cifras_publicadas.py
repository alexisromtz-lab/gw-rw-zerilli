# HUELLA-GW-RW-ZERILLI-TEST-CIFRAS-20261020
"""El README de este repositorio promete que cada cifra tiene portador.

Este test hace exigible esa promesa en cada push. No mide fisica: mide
procedencia. Dos falsadores, uno por cada forma de mentir de una cifra:

  1. una cifra publicada cuyo valor no esta en ningun crudo commiteado;
  2. una celda roja que alguien borre del README para dejar solo lo verde.

No hay red, no hay tolerancias elegidas a mano: la tolerancia de cada cifra es
la de su propio redondeo (media unidad del ultimo digito publicado).
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CRUDOS = sorted((RAIZ / "sim" / "data").glob("*.json"))
README = RAIZ / "README.md"

# Una cifra "publicada" es la que se escribe con seis decimales o mas: las de
# menos digitos son redondeos de prosa y no reclaman portador propio.
PATRON_CIFRA = re.compile(r"-?\d+\.\d{6,}(?:[eE][-+]?\d+)?")


def _cargar_crudos() -> list[tuple[str, object]]:
    """Devuelve (nombre, objeto). Un crudo ilegible es un rojo, no un olvido."""
    cargados = []
    for ruta in CRUDOS:
        try:
            cargados.append((ruta.name, json.loads(ruta.read_text(encoding="utf-8"))))
        except json.JSONDecodeError as exc:  # fail-closed
            raise AssertionError(f"crudo ilegible: {ruta.name}: {exc}") from exc
    return cargados


def _hojas_numericas(objeto: object):
    if isinstance(objeto, dict):
        for valor in objeto.values():
            yield from _hojas_numericas(valor)
    elif isinstance(objeto, list):
        for valor in objeto:
            yield from _hojas_numericas(valor)
    elif isinstance(objeto, (int, float)) and not isinstance(objeto, bool):
        if math.isfinite(objeto):
            yield objeto


def _quantum(literal: str) -> float:
    """Media unidad del ultimo digito publicado (la tolerancia de su redondeo)."""
    m = re.fullmatch(r"(\d+)\.(\d+)(?:[eE]([-+]?\d+))?", literal.lstrip("-"))
    assert m, f"literal no reconocido: {literal}"
    decimales = len(m.group(2))
    exponente = int(m.group(3) or 0)
    return 0.5 * 10.0 ** (exponente - decimales)


def _cifras_publicadas() -> list[str]:
    return PATRON_CIFRA.findall(README.read_text(encoding="utf-8"))


def test_el_readme_publica_cifras():
    """Un README vaciado no puede pasar este test por vacuidad."""
    assert len(_cifras_publicadas()) >= 8, "el README perdio sus cifras: nada que auditar"


def test_toda_cifra_publicada_tiene_portador():
    crudos = _cargar_crudos()
    assert crudos, "no hay crudos: sin portadores no hay auditoria"
    hojas = [(nombre, valor) for nombre, objeto in crudos for valor in _hojas_numericas(objeto)]
    textos = [(nombre, (RAIZ / "sim" / "data" / nombre).read_text(encoding="utf-8")) for nombre, _ in crudos]

    huerfanas = []
    for literal in sorted(set(_cifras_publicadas())):
        publicado = float(literal)
        tolerancia = _quantum(literal)
        en_hoja = any(
            abs(valor - publicado) <= tolerancia for _, valor in hojas if math.isfinite(valor)
        )
        en_texto = any(literal in texto for _, texto in textos)
        if not (en_hoja or en_texto):
            huerfanas.append(literal)

    assert not huerfanas, f"cifras publicadas sin crudo que las respalde: {huerfanas}"


def test_c4_refusada_por_cfl_no_se_rebaja():
    """La celda REFUSED es un dato: el sello CFL no se rebaja para aprobar."""
    crudos = _cargar_crudos()
    refusadas = [
        c4 for _, objeto in crudos for c4 in [objeto.get("c4")] if isinstance(c4, str)
    ]
    assert refusadas, "desaparecio el registro de c4 REFUSADA"
    for texto in refusadas:
        assert texto.startswith("REFUSADA"), texto
        assert "0.7500000000" in texto and "0.5000000000" in texto, texto


def test_c3a_sigue_no_medible():
    """C3a no se reumbraliza: se publica como NO MEDIBLE por piso de redondeo."""
    causas = []
    for _, objeto in _cargar_crudos():
        for clave, celda in (objeto.get("celdas") or {}).items():
            if isinstance(celda, dict) and clave.startswith("C3a"):
                causas.append(celda.get("causa", ""))
    assert causas, "desaparecio la celda C3a"
    assert any("NO MEDIBLE" in causa for causa in causas), causas


def test_f1_publica_el_rojo_antes_de_la_reparacion():
    """El 1.0163 pre-reparacion tiene crudo. Si no, el verde no se puede auditar."""
    f1 = [objeto for _, objeto in _cargar_crudos() if objeto.get("gate", {}).get("nombre") == "Gate 2D-F1 (nombre del dueno)"]
    assert f1, "no hay crudos del Gate 2D-F1"
    rojos = [o for o in f1 if o.get("todo_verde") is False]
    verdes = [o for o in f1 if o.get("todo_verde") is True]
    assert rojos, "falta el crudo ROJO pre-reparacion (F1.b orden 1.0163)"
    assert verdes, "falta el crudo VERDE post-reparacion"
    orden_min_rojo = min(o["f1b"]["orden_min"] for o in rojos)
    assert abs(orden_min_rojo - 1.0163) <= 5e-5, f"el rojo publicado es 1.0163, medido {orden_min_rojo}"
    ordenes_verdes = sorted(v for o in verdes for v in (x["orden"] for x in o["f1b"]["ordenes"]))
    assert abs(ordenes_verdes[0] - 1.9246) <= 5e-5, ordenes_verdes
    assert abs(ordenes_verdes[-1] - 2.0251) <= 5e-5, ordenes_verdes


def test_el_readme_conserva_las_celdas_rojas():
    """Quitar lo rojo del escaparate es el unico cambio que este repo no admite."""
    texto = README.read_text(encoding="utf-8")
    for marca in ("REFUSADA", "NO MEDIBLE", "ROJA"):
        assert marca in texto, f"el README dejo de declarar {marca}"
