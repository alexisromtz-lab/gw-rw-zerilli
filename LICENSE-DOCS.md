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

- **Este repositorio todavía no tiene DOI.** No se designa un identificador que
  no existe: el blanco de atribución es hoy la URL del repositorio más el commit
  citado, y su forma exigible es
  `Roman Martinez, Jose Alexis. gw-rw-zerilli (Platino Labs), commit <sha>, 2026`.
- Cuando se acuñe el DOI del Manuscrito 2, el blanco de atribución pasa a ser el
  **DOI de concepto** (resuelve siempre a la última versión y no caduca por
  Release). Hasta entonces, esta línea es la que vale.

## El campo `license` del depósito

El campo `license` de los metadatos Zenodo es de **un solo valor**: no admite las
dos capas a la vez. Ahí se declara la capa que corresponde al objeto depositado —
un `publication` / `preprint`, es decir **documentación**. Por eso el metadato
lleva `cc-by-4.0` y el `LICENSE` del código sigue en MIT: no hay contradicción,
hay dos objetos.

Esta es la resolución de la discrepancia que el README declaraba sin adjudicar
(manifiesto en `MIT` vs. árbol de trabajo en `cc-by-4.0`). Determinación del
dueño, 2026-10-20: doble licencia, **MIT para el código, CC BY 4.0 para el texto**.
