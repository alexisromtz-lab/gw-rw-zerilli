<!-- HUELLA-GW-RW-ZERILLI-FUSION-20261020 -->

# gw-rw-zerilli — convergencia cuadrática `O(h²)` y absorción perimetral sub-40 dB en esquemas kick-drift 2D

> **EN —** Numerical-relativity-grade metrology on 2D kick-drift hyperbolic schemes, plus a 1D
> Regge–Wheeler / Zerilli leapfrog driver. **Second-order convergence** is measured on both
> potentials (`p = 2.0002312004820553` RW, `p = 2.000226129020191` Zerilli) and on the 2D Richardson
> ladder (`p = 1.990765787067249` / `2.0011044055918528` / `2.0028629063990215`, tolerance `0.05`).
> Perimetric absorption clears the sealed `−40 dB` at `R_dB = −45.931354463740675 dB`. Each gate was
> pre-registered in Git **before** its first number and closes with its own verdict: `F3` and three
> cells are **published RED**, one run is **REFUSED** fail-closed, and nothing is repaired after the
> fact.

**Manuscrito 2** — [`MANUSCRITO_2_ORDEN_CUADRATICO_Y_ABSORCION_PERIMETRAL_20261014.md`](MANUSCRITO_2_ORDEN_CUADRATICO_Y_ABSORCION_PERIMETRAL_20261014.md)
`HUELLA-MANUSCRITO-ORDEN-CUADRATICO-Y-ABSORCION-PERIMETRAL-20261014` · `manuscrito-2-v1-20261014`
· cierre `2026-10-14` · licencia declarada en el propio manuscrito: **MIT**.

## Las dos propiedades que se certifican

1. **Orden de convergencia cuadrático `O(h²)`** preservado bajo refinamiento de malla, con extinción
   del piso de error en arranque de Cauchy simétrico.
2. **Absorción perimetral adiabática** por debajo del umbral sellado de **−40 dB**, sin reflexión
   parásita de pared y sin contaminación interior.

Tolerancias selladas: `umbral_p = 0.05` · frontera `-40.0 dB` · `UMBRAL_C5_DB = 0.5`.

## Estado del frente, sin maquillaje

| gate | estado | cifra que lo porta |
|---|---|---|
| `F1` | **VERDE** | `F1.a = 6.000848e-14` · `F1.b` orden `2.0251` / `1.9246` · control `4.913749e+00` |
| `F2` | **VERDE** | 1D RW `p = 2.0002312004820553` · Zerilli `p = 2.000226129020191` (`nota_p = OK`); 2D Richardson `p = 1.990765787067249` / `2.0011044055918528` / `2.0028629063990215` |
| `F4` | **VERDE** | pasó de `FALLA` declarada en V2 (`−21.68 dB` / `−19.10 dB` frente a `−40 dB`) a VERDE en V3: `−47.48848252620233 dB` / `−47.48845786723316 dB`, margen `+7.4885 dB` |
| `F11` | **VERDE** (nominal) | `R_dB = −45.931354463740675` (unidad energía), corrida `E1`, `nr0 = 384`, `fallos = []` |
| `F3` | **ROJO declarado** | rectificación ratificada en prosa, **aún no implementada** |
| Línea A | certificada | banco *must-fail* `4/4` discriminado (`C0:0 E1:2 E2:3 E3:1`), `ORDEN p = 4 CERTIFICADO` |

### Las celdas que salen rojas y una corrida que se niega a correr

| celda | medición | declaración |
|---|---|---|
| `C3b ANGULAR ORDEN 1` | `p = 0.9857539455144246` | **ROJA** |
| `C3a RADIAL ORDEN 1` | sin medición válida | **NO MEDIBLE** |
| `c4` | `CFL = 0.7500000000 > sellado 0.5000000000` | **REFUSADA** *fail-closed* |

**Declaración obligatoria: `−44.94 dB a 3072 celdas` NO es un resultado medido.** Aparece únicamente
en el asunto del commit `f974578` y en una cita de ese asunto dentro de
`sim/PREREGISTRO_GATE_2D_F3_ZERILLI_CURVATURA_20261013.md`. No existe crudo commiteado que la
respalde: el crudo de `F11` no contiene `3072`, ni `44.94`, ni bloque `C5`; su única `R_dB` es
`−45.931354463740675` con `rung = E1`. Los escalones `E2`, `E3` y `E4` están declarados en la
escalera pero **no fueron medidos** en la corrida commiteada. Se cita como **compromiso del sujeto de
commit**, nunca como medición.

### El medio paso que costaba un orden de convergencia

Antes de la reparación, `F1.b` medía orden **`1.0163`** (ROJO, commit `39868c6`). La causa: la
inicialización del bucle *kick-drift* usaba `v^{-1/2}` en lugar del medio paso correcto. Se corrigió
**una línea** y se nombró el invariante en el docstring del `core`. La diferencia entre `1.0163` y
`2.025059` es el efecto de **un medio paso mal puesto** — y quedó registrada como tal.

## Aparato

```
sim/driver_rw_zerilli_1d.py                    driver leapfrog 1D (`--potencial rw|zerilli|nulo`)
sim/driver_rw_zerilli_2d.py                    driver 2D
sim/extractor_polos_matrixpencil.py            polos complejos por Prony / Matrix Pencil
sim/sonda_2d_f1_dominio.py                     sonda de dominio F1
sim/arnes_richardson_2d_f2_v3.py              arnés de convergencia (Richardson F2)  blob 72844790ba3ef2184d941ed1202c84b88771276b
sim/arnes_richardson_2d_f2.py                  vecino NO adjudicado: no produjo el crudo sellado
sim/arnes_zerilli_curvatura_2d_f3.py           arnés del frente de curvatura (F3)
sim/arnes_capa_absorbente_2d_f11.py            capa absorbente perimetral (F11)
sim/certificador_reescritura_stencil_residuo.py certificación simbólica de stencils (Taylor)
sim/data/crudo_2d_f2_richardson_post_arranque_v3_nr0_{64,128,256}_*.json   crudos del refinamiento
sim/data/crudo_rw_zerilli_v3_{todo,frontera}_*.json   crudos 1D de los dos potenciales
sim/PREREGISTRO_*                              sellos por gate, ANTES de la primera cifra
sim/ACTA_* · sim/ERRATA_* · sim/DECLARACION_*  actas de cierre, erratas y colisiones declaradas
```

## Reproducir

```sh
python3 -B sim/arnes_richardson_2d_f2_v3.py --help
# flags medidos en el arnes: --estricto --stamp --json --cfl --T --nr0   (refinamiento nr0 ∈ {64, 128, 256})

# los dos potenciales, mismo driver 1D (argv registrado en el crudo v3todo)
python3 -B sim/driver_rw_zerilli_1d.py --modo todo --potencial rw
python3 -B sim/driver_rw_zerilli_1d.py --modo todo --potencial zerilli

# capa absorbente perimetral (argv registrado en el crudo F11)
python3 -B sim/arnes_capa_absorbente_2d_f11.py --estricto --json <ruta-del-crudo>.json

# banco must-fail del certificador simbolico: debe discriminar C0:0 E1:2 E2:3 E3:1
python3 -B sim/certificador_reescritura_stencil_residuo.py --must-fail --json
```

Requiere `python3` con `numpy` (y `scipy` para el extractor de polos). Los arneses se corren con `-B`
para no escribir `__pycache__` dentro del árbol medido.

Cada cifra del manuscrito afirma con **portador declarado** (archivo · blob · líneas · bytes) y
**comando que la respalda**. Una cifra cuya procedencia sea un *asunto de commit* y no un crudo se
declara **compromiso**, no resultado medido (§4.4).

## Erratas y colisiones declaradas (esto es el valor)

El repositorio conserva, con nombre y fecha, lo que la mayoría esconde: la **errata** de identidad
`F2` v2/v3, la **colisión** de la sonda CFL con malla fija, la **declaración** de arranque exacto con
su criterio de piso, y la **errata del pre-registro** del gate 2D `F3`. Ninguna se reescribe hacia
atrás: se declaran y se conservan las dos filas.

## Límites declarados

- `F3` es **ROJO** y sigue ROJO: la rectificación está ratificada **en prosa** y todavía **no
  implementada**.
- `C3b` es **ROJA** (`p = 0.9857539455144246`), `C3a` es **NO MEDIBLE** y `c4` fue **REFUSADA** por
  `CFL 0.7500000000 > sellado 0.5000000000`. Las tres se publican sin reparar y sin reumbralizar.
- `F2` tiene un **vecino no adjudicado** (`sim/arnes_richardson_2d_f2.py`, sucio ` M`): no se toca y
  no cuenta como resultado.
- `F11` es VERDE **nominal**; el adjetivo es parte del veredicto, y su única cifra con crudo es
  `−45.931354463740675 dB` (corrida `E1`). La cifra `−44.94 dB` no tiene crudo: es compromiso.
- Este repositorio **todavía no tiene DOI**. Los metadatos de depósito del Manuscrito 2 están
  sellados en el árbol, pero no se cita identificador propio.
- El árbol de trabajo tiene `"license"` cambiado a `cc-by-4.0` sobre el manifiesto sin commitear:
  lo que publica el repositorio es **MIT**. Esta discrepancia se declara, no se adjudica aquí.

## Licencia y citación

**MIT** — declarada en el manuscrito y en [`LICENSE`](LICENSE).
Metadatos de depósito: [`ZENODO_MANUSCRITO_2_ORDEN_CUADRATICO_Y_ABSORCION_20261014.json`](ZENODO_MANUSCRITO_2_ORDEN_CUADRATICO_Y_ABSORCION_20261014.json).

**Parte del archivo de instrumentos de [alexisromtz-lab](https://github.com/alexisromtz-lab).**
