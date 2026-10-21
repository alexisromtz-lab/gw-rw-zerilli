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
· cierre `2026-10-14` · doble licencia: **documentación CC BY 4.0**, **código MIT**.

**DOI (concepto):** [10.5281/zenodo.23525359](https://doi.org/10.5281/zenodo.23525359) · `v1.0.1` → [10.5281/zenodo.23525446](https://doi.org/10.5281/zenodo.23525446)

**Construido sobre [1,2].** — *Building on the Regge–Wheeler–Zerilli formulation [1,2], we implement the
leapfrog ringdown driver and add a convergence test (`p = 2.0028629063990215`, within the sealed
tolerance `0.05`) that, to our knowledge, was not present in the original papers.*

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

<!-- HUELLA-GW-REPRODUCIBLE-20261020 -->

Primero la auditoria, en un clon limpio y **sin instalar el repositorio** (no hay `pyproject.toml`,
y no hace falta): los tests son biblioteca estandar, sin `numpy`.

```sh
git clone https://github.com/alexisromtz-lab/gw-rw-zerilli.git && cd gw-rw-zerilli
python3 -m pip install --quiet pytest && python3 -m pytest -q     # 8 tests, ~0,6 s
```

Despues el aparato numerico (aqui si hace falta `numpy`, y `scipy` para los polos):

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

El aparato numerico requiere `python3` con `numpy` (y `scipy` para el extractor de polos); la
auditoria de cifras de arriba no, corre con la biblioteca estandar. Los arneses se corren con `-B`
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
- El límite «**sin identificador propio**» **se cerró el `2026-10-20`**: `v1.0.0` acuñó los dos
  DOIs (ver *Licencia y citación*). Los metadatos de depósito del Manuscrito 2 siguen sellados en
  el árbol, y el Manuscrito 2 **no** tiene depósito propio: no se cita un identificador separado
  que todavía no existe.
- El árbol de trabajo tenía `"license"` cambiado a `cc-by-4.0` sobre el manifiesto:
  la discrepancia **queda adjudicada** por doble licencia (ver *Licencia y citación*).
  El campo del depósito lleva `cc-by-4.0` porque el objeto depositado es un
  `preprint`, es decir documentación; el código sigue en **MIT**.

## Licencia y citación

<!-- HUELLA-GW-RW-ZERILLI-LICENSE-DOCS-CC-BY-4.0-20261020 -->

**Doble licencia, por naturaleza del objeto:**

- **Código** (`*.py`, `*.sh`) — **MIT**, en [`LICENSE`](LICENSE).
- **Documentación** (manuscrito, README, metadatos, crudos de `sim/data/`) — **CC BY 4.0**,
  en [`LICENSE-DOCS.md`](LICENSE-DOCS.md).

Metadatos de depósito: [`ZENODO_MANUSCRITO_2_ORDEN_CUADRATICO_Y_ABSORCION_20261014.json`](ZENODO_MANUSCRITO_2_ORDEN_CUADRATICO_Y_ABSORCION_20261014.json)
— su campo `license` es de un solo valor y declara `cc-by-4.0` porque el objeto depositado es un `preprint`.

### Identificadores: qué cita cada archivo

<!-- HUELLA-GW-DOI-V101-20261020 -->

| para qué | DOI | archivo que lo lleva |
|---|---|---|
| **reproducir** una versión exacta (`v1.0.1`) | [`10.5281/zenodo.23525446`](https://doi.org/10.5281/zenodo.23525446) | `CITATION.cff`, campo `doi` |
| **atribución** — «esto salió de aquí» | [`10.5281/zenodo.23525359`](https://doi.org/10.5281/zenodo.23525359) | esta sección y `LICENSE-DOCS.md` |

El DOI de **concepto** resuelve siempre a la última versión: es el que no se rompe en cada release
y por eso es el de la vitrina. El DOI de **versión** no se mueve nunca: es el que hay que citar para
reproducir los bytes exactos. Copiar el de versión en la vitrina —o el de concepto en
`CITATION.cff`— es el error que esta tabla existe para impedir.

Depósito `v1.0.1`: registro <https://zenodo.org/record/23525446>, construido con `git archive`
desde la etiqueta `v1.0.1`. El archivo depositado **se verifica a sí mismo**: extraído en un venv
limpio sin `numpy`, `python3 -m pytest -q` da `8 passed`. Instancia anterior, inmutable:
`v1.0.0` = <https://zenodo.org/record/23525360>, archivo `gw-rw-zerilli-v1.0.0.zip`,
`1021013 B`, `sha256 29de5f067defae3fe94707b5f305fc4b50fa1d7fbfd0d0ae25c17adc3ff7b917`.

<!-- HUELLA-GW-DOI-V100-DEFECTO-20261020 -->

**Defecto declarado de `v1.0.0`.** Su archivo se construyó de la etiqueta `v1.0.0` (commit
`108c817`) **antes** de que existiera `CITATION.cff`, así que su `README` interno todavía dice
«sin DOI» — falso dentro de un artefacto que sí lo tiene. Los bytes publicados son inmutables y no
se reescriben: la instancia queda como testimonio del orden en que se hicieron las cosas, y `v1.0.1`
la corrige. La declaración viaja también en el campo `notes` del registro `v1.0.1`; en el de `v1.0.0`
no se pudo escribir sin republicar, y se prefiere el artefacto intacto a la nota.

**El `sha256` de un archivo no puede vivir dentro de ese archivo.** Por eso aquí se declara el de la
versión anterior, y el de cada versión vive en el campo `notes` de su propio registro Zenodo, que se
escribe con el hash ya calculado y antes de publicar. La fila `v1.0.0` no se borra al publicar
`v1.0.1`: se conservan las dos.

El registro declara `related_identifiers` hacia los dos papers (`cites` → `10.1103/PhysRev.108.1063`,
`10.1103/PhysRevLett.24.737`), que es la vía por la que quien busque esos DOIs encuentra este
repositorio.

**Parte del archivo de instrumentos de [alexisromtz-lab](https://github.com/alexisromtz-lab).**

## References

<!-- HUELLA-GW-REFERENCIAS-20261020 -->

[1] T. Regge and J. A. Wheeler, "Stability of a Schwarzschild Singularity," *Phys. Rev.* **108**, 1063 (1957). DOI: [10.1103/PhysRev.108.1063](https://doi.org/10.1103/PhysRev.108.1063)

[2] F. J. Zerilli, "Effective Potential for Even-Parity Regge-Wheeler Gravitational Perturbation Equations," *Phys. Rev. Lett.* **24**, 737 (1970). DOI: [10.1103/PhysRevLett.24.737](https://doi.org/10.1103/PhysRevLett.24.737)

**[1,2] son la base teórica, y nada más se cita.** Este repositorio no consume datos observacionales:
los `sim/PREREGISTRO_*` declaran LIGO/Virgo como **ajeno, no reclamado**, y aquí no hay ninguna serie
de interferómetro. Las dos referencias son las ecuaciones que se implementan, no una fuente de
mediciones. Citar una colaboración de la que no se tomó un dato sería atribución falsa.

