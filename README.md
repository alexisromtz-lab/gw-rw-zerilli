# gw-rw-zerilli — convergencia cuadrática `O(h²)` y absorción perimetral sub-40 dB en esquemas kick-drift 2D

> **EN —** Numerical-relativity-grade metrology on 2D kick-drift hyperbolic schemes. Two properties
> are certified: **second-order convergence** preserved under mesh refinement (Richardson `p = 2.0028`,
> tolerance `0.05`) and **perimetric absorption below the sealed −40 dB** (`R_dB = −44.94 dB`). Each
> gate was pre-registered in Git **before** its first number and closes with its own verdict —
> including `F3`, which is **declared ROJO**.

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
| `F2` | **VERDE** | Richardson cuadrático `p = 2.0028` en `nr0 = 256` |
| `F4` | **VERDE** | pasó de `FALLA` declarada en V2 (`−21.68 dB` / `−19.10 dB` frente a `−40 dB`) a VERDE en V3 |
| `F11` | **VERDE** (nominal) | `R_dB = −44.94 dB`, `C5` con `RC 0` a 3072 |
| `F3` | **ROJO declarado** | rectificación ratificada en prosa, **aún no implementada** |
| Línea A | certificada | banco *must-fail* `4/4` discriminado |

### El medio paso que costaba un orden de convergencia

Antes de la reparación, `F1.b` medía orden **`1.0163`** (ROJO, commit `39868c6`). La causa: la
inicialización del bucle *kick-drift* usaba `v^{-1/2}` en lugar del medio paso correcto. Se corrigió
**una línea** y se nombró el invariante en el docstring del `core`. La diferencia entre `1.0163` y
`2.025059` es el efecto de **un medio paso mal puesto** — y quedó registrada como tal.

## Aparato

```
sim/arnes_richardson_2d_f2_v3.py              arnés de convergencia (Richardson F2)  blob 72844790ba3ef2184d941ed1202c84b88771276b
sim/arnes_zerilli_curvatura_2d_f3.py           arnés del frente de curvatura (F3)
sim/arnes_capa_absorbente_2d_f11.py            capa absorbente perimetral (F11)
sim/certificador_reescritura_stencil_residuo.py certificación simbólica de stencils (Taylor)
sim/data/crudo_2d_f2_richardson_post_arranque_v3_nr0_{64,128,256}_*.json   crudos del refinamiento
sim/PREREGISTRO_*                              sellos por gate, ANTES de la primera cifra
sim/ACTA_* · sim/ERRATA_* · sim/DECLARACION_*  actas de cierre, erratas y colisiones declaradas
```

## Reproducir

```sh
python3 -B sim/arnes_richardson_2d_f2_v3.py --help
# flags medidos en el arnes: --estricto --stamp --json --cfl --T --nr0   (refinamiento nr0 ∈ {64, 128, 256})
```

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
- `F2` tiene un **vecino no adjudicado** (`sim/arnes_richardson_2d_f2.py`, sucio ` M`): no se toca y
  no cuenta como resultado.
- `F11` es VERDE **nominal**; el adjetivo es parte del veredicto.

## Licencia y citación

**MIT** — declarada en el manuscrito y en [`LICENSE`](LICENSE).
Metadatos de depósito: [`ZENODO_MANUSCRITO_2_ORDEN_CUADRATICO_Y_ABSORCION_20261014.json`](ZENODO_MANUSCRITO_2_ORDEN_CUADRATICO_Y_ABSORCION_20261014.json).

**Parte del archivo de instrumentos de [alexisromtz-lab](https://github.com/alexisromtz-lab).**
