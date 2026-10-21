<!-- HUELLA-GW-RW-ZERILLI-LICENSE-DOCS-CC-BY-4.0-20261020 -->

# Licencia de la documentación — CC BY 4.0

La **documentación** de este repositorio se publica bajo **Creative Commons
Attribution 4.0 International (CC BY 4.0)**. El **código** se publica bajo **MIT**.
Son dos capas y no se mezclan.

- Deed (resumen legible): https://creativecommons.org/licenses/by/4.0/
- Texto legal (legalcode): https://creativecommons.org/licenses/by/4.0/legalcode

## Cobertura

| Capa | Extensiones | Licencia |
|---|---|---|
| Documentación | `*.md`, `*.json`, `*.cff` | CC BY 4.0 (este archivo) |
| Código | `*.py`, `*.sh` | MIT (`LICENSE`) |

Los crudos sellados de `sim/data/*.json` son **datos**: caen en la capa de
documentación (CC BY 4.0) porque su valor está en poder citarse y reanalizarse,
no en ejecutarse. El texto de `LICENSE` es el MIT canónico, **sin modificaciones**.

## Atribución

<!-- HUELLA-GW-LICENSE-DOCS-DOI-CONCEPTO-20261020 -->

El blanco de atribución es el **DOI de concepto** —resuelve siempre a la última
versión y no caduca por Release—:

| para qué | DOI |
|---|---|
| atribución («esto salió de aquí») | [`10.5281/zenodo.23525359`](https://doi.org/10.5281/zenodo.23525359) |

Forma exigible:
`Roman Martinez, Jose Alexis. gw-rw-zerilli (Platino Labs), 2026. DOI: 10.5281/zenodo.23525359`.

El **DOI de versión** (`v1.0.1` → `10.5281/zenodo.23525446`, `v1.0.0` →
`10.5281/zenodo.23525360`) **no** se cita aquí: sirve para reproducir los bytes
exactos y vive en `CITATION.cff`. Copiar el de versión en este archivo —o el de
concepto en el `CITATION.cff`— es el error que la tabla del README existe para
impedir.

### Límite histórico, cerrado

- **2026-10-20 · cerrado.** Este archivo decía: «Este repositorio todavía no
  tiene DOI. No se designa un identificador que no existe: el blanco de
  atribución es hoy la URL del repositorio más el commit citado». Era verdad
  hasta la acuñación del concepto `10.5281/zenodo.23525359`; desde entonces el
  blanco es el DOI. La frase no se reescribe: se cierra con fecha.

## El campo `license` del depósito

El campo `license` de los metadatos Zenodo es de **un solo valor**: no admite las
dos capas a la vez. Ahí se declara la capa que corresponde al objeto depositado —
un `publication` / `preprint`, es decir **documentación**. Por eso el metadato
lleva `cc-by-4.0` y el `LICENSE` del código sigue en MIT: no hay contradicción,
hay dos objetos.

Esta es la resolución de la discrepancia que el README declaraba sin adjudicar
(manifiesto en `MIT` vs. árbol de trabajo en `cc-by-4.0`). Determinación del
dueño, 2026-10-20: doble licencia, **MIT para el código, CC BY 4.0 para el texto**.
