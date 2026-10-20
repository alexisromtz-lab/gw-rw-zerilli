<!-- HUELLA-GW-RW-ZERILLI-README-20261020 -->

# gw-rw-zerilli

**Regge–Wheeler y Zerilli en 1D y 2D, con lo verde y lo rojo publicados tal como salieron.**

> **EN —** Regge–Wheeler / Zerilli wave propagation on a Schwarzschild background: a 1D leapfrog driver and a 2D kick-drift scheme, pre-registered falsifiers and sealed raw files. Second-order convergence is measured on both potentials — `p = 2.0002312004820553` for Regge–Wheeler, `p = 2.000226129020191` for Zerilli. The absorbing perimeter clears its sealed threshold at `-47.48848252620233 dB` against `-40.0 dB`. Three cells are published RED or NOT MEASURABLE and one run is REFUSED *fail-closed*: nothing here is repaired after the fact.

Estado del frente al cierre del manifiesto (2026-10-14): `F1` VERDE · `F2` VERDE · `F4` VERDE · `F11` VERDE (nominal) · `F3` **ROJO declarado** · Línea A certificada.

---

## 1. Lo que sí salió

| Frente | Objeto medido | Veredicto y cifra |
|---|---|---|
| `F2` — 1D | Orden de convergencia por extrapolación de Richardson, sobre los dos potenciales | VERDE — RW `p = 2.0002312004820553` · Zerilli `p = 2.000226129020191`, ambos `nota_p = OK` |
| `F2` — 2D | Escalera de refinamiento `nr0 = 64 / 128 / 256`, umbral declarado `0.05` | VERDE — `p = 1.990765787067249` · `2.0011044055918528` · `2.0028629063990215` |
| Piso de error | Arranque de Cauchy simétrico en `nr0 = 256` | `d2 = 4.986396759321774e-03` contra `ref_piso_f2 = 1.081241e-02`, factor `0.46117348115006496` |
| `F4` | Frontera absorbente contra umbral sellado `-40.0 dB` | VERDE — `-47.48848252620233 dB` (derecha) · `-47.48845786723316 dB` (izquierda), margen `+7.4885 dB` |
| `F11` | Absorción perimetral, corrida nominal `E1`, `nr0 = 384` | VERDE — `R_dB = -45.931354463740675` (unidad: energía), `fallos = []` |
| Línea A | Certificación simbólica del residuo de ecuación modificada (reescritura de Taylor) | banco *must-fail* discriminado con vector `C0:0 E1:2 E2:3 E3:1`; `ORDEN p = 4 CERTIFICADO`, `escritura_a_disco: 0` |

## 2. Lo que salió rojo, y se queda rojo

| Celda | Medición | Declaración |
|---|---|---|
| `C3b ANGULAR ORDEN 1` | `p = 0.9857539455144246` | **ROJA** |
| `C3a RADIAL ORDEN 1` | sin medición válida | **NO MEDIBLE** |
| `c4` | `CFL = 0.7500000000 > sellado 0.5000000000` | **REFUSADA** *fail-closed* |
| `F3` — curvatura de Zerilli 2D | triple `['C2','C4','C6']`, `rc = 1` | **ROJO declarado**, con diagnóstico y rectificación ratificada en prosa, aún no implementada |

Estos cuatro hechos se publican como están: no se reumbralizan, no se reparan y no se omiten. Un repositorio que sólo muestra lo verde no certifica nada.

## 3. Regla de lectura de las cifras

Toda cifra de este repositorio afirma con **portador declarado** (archivo · blob `git hash-object` · líneas · bytes) y con el **comando que la respalda**. Los crudos viven en `sim/data/` y son la fuente; el manuscrito y los metadatos de depósito los citan, no los sustituyen.

**Declaración obligatoria: la cifra `-44.94 dB a 3072 celdas` NO es un resultado medido.** Aparece únicamente en el asunto de un commit (`f974578`) y en una cita de ese asunto dentro de `sim/PREREGISTRO_GATE_2D_F3_ZERILLI_CURVATURA_20261013.md`. No existe crudo commiteado que la respalde: el crudo de `F11` no contiene `3072`, ni `44.94`, ni bloque `C5`; su única `R_dB` es `-45.931354463740675` con `rung = E1`. Los escalones `E2`, `E3` y `E4` están declarados en la escalera pero **no fueron medidos** en la corrida commiteada. Se cita aquí como compromiso del sujeto de commit, nunca como medición.

## 4. Mapa del repositorio

```
sim/driver_rw_zerilli_1d.py              driver leapfrog 1D (--potencial rw|zerilli|nulo)
sim/driver_rw_zerilli_2d.py              driver 2D
sim/arnes_richardson_2d_f2_v3.py         arnés de Richardson 2D (versión sellada)
sim/arnes_richardson_2d_f2.py            versión previa; NO es la que produjo el crudo sellado
sim/arnes_zerilli_curvatura_2d_f3.py     puerta de curvatura de Zerilli (ROJA)
sim/arnes_capa_absorbente_2d_f11.py      capa absorbente perimetral
sim/sonda_2d_f1_dominio.py               sonda de dominio F1
sim/certificador_reescritura_stencil_residuo.py   certificador simbólico (Línea A)
sim/extractor_polos_matrixpencil.py      polos complejos por Prony / Matrix Pencil
sim/data/*.json                          crudos sellados — de aquí salen todas las cifras
sim/PREREGISTRO_*.md                     pre-registros, commiteados antes de la primera cifra
sim/ACTA_*.md · sim/ERRATA_*.md          cierres, erratas y declaraciones de colisión
MANUSCRITO_2_ORDEN_CUADRATICO_Y_ABSORCION_PERIMETRAL_20261014.md
ZENODO_MANUSCRITO_2_ORDEN_CUADRATICO_Y_ABSORCION_20261014.json
```

## 5. Cómo reproducir

Requiere `python3` con `numpy` (y `scipy` para el extractor de polos). Los arneses se corren con `-B` para no escribir `__pycache__` dentro del árbol medido.

```bash
# 1D: mismo driver, los dos potenciales
python3 -B sim/driver_rw_zerilli_1d.py --modo todo --potencial rw
python3 -B sim/driver_rw_zerilli_1d.py --modo todo --potencial zerilli

# 2D: un escalón de la escalera de Richardson (repetir con --nr0 128 y --nr0 256)
python3 -B sim/arnes_richardson_2d_f2_v3.py --estricto --nr0 64 --json auto

# 2D: capa absorbente perimetral (escribe su propio crudo)
python3 -B sim/arnes_capa_absorbente_2d_f11.py --estricto --json sim/data/crudo_capa_absorbente_2d_f11_<sello>.json

# 2D: puerta de curvatura de Zerilli (la que sale ROJA)
python3 -B sim/arnes_zerilli_curvatura_2d_f3.py

# Línea A: banco must-fail del certificador simbólico (debe discriminar C0:0 E1:2 E2:3 E3:1)
python3 -B sim/certificador_reescritura_stencil_residuo.py --must-fail --json

# Polos complejos por Matrix Pencil
python3 -B sim/extractor_polos_matrixpencil.py --modo sintetico
```

Cada corrida escribe su crudo con hora UTC, `argv`, `huella` e `identidad_self`: dos ejecuciones no producen dos verdades distintas, producen dos crudos fechados.

## 6. Protocolo de medición

Toda escritura se autoriza sólo después de medir que la fila no exista, con una compuerta determinista previa y bloqueante, corrida con rutas **absolutas**. Códigos: `0` apto · `10` el objetivo no existe (creación autorizada) · `11` la huella ya está presente (colisión: cero escrituras) · `12` blob mutado · `13` objetivo sucio · `14` objetivo sin árbol git · `15` líneas distintas al contrato · `20` tupla incompleta. El cierre de cada paso viaja con la huella del objeto destino (blob, bytes, líneas, hora).

## 7. Estado de publicación

- **DOI: pendiente de depósito.** Los metadatos Zenodo del Manuscrito 2 están sellados en el árbol, pero este repositorio todavía no tiene identificador propio. No se cita uno.
- **Licencia:** MIT, declarada en `ZENODO_MANUSCRITO_2_...json` (`"license": "MIT"`). El árbol **no contiene archivo `LICENSE`**.
- **Autor:** Roman Martinez, Jose Alexis — Platino Labs.

Cifras medidas y selladas; no se inventan experimentos. Toda cifra de conteo caduca al escribirse: su hora es parte de la cifra.
