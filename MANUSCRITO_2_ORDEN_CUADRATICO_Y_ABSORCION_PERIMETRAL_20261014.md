# Preservación del orden de convergencia cuadrático O(h²) y absorción perimetral adiabática sub-40 dB en esquemas hiperbólicos bidimensionales kick-drift

**HUELLA:** `HUELLA-MANUSCRITO-ORDEN-CUADRATICO-Y-ABSORCION-PERIMETRAL-20261014`
**VERSION:** `manuscrito-2-v1-20261014`
**FECHA DE CIERRE:** 2026-10-14
**CASA:** `/Users/marlene/gw-rw-zerilli` (raíz del repo: `sim/`)
**AUTOR:** Roman Martinez, Jose Alexis — `alexisromtz-lab`
**LICENCIA:** MIT · **TIPO DE REGISTRO:** publicación (preprint) · **IDIOMA:** spa
**PRE-VUELO A2.1 (turno 1):** `bash tools/gate_pre_escritura.sh /Users/marlene/platino-labs/MANUSCRITO_2_ORDEN_CUADRATICO_Y_ABSORCION_PERIMETRAL_20261014.md NO_EXISTE_PRE10 'HUELLA-MANUSCRITO-ORDEN-CUADRATICO-Y-ABSORCION-PERIMETRAL-20261014' 0` → `COLISION: ... no existe.` → **PRE_RC = 10** (ausencia medida ⇒ escritura autorizada).

---

## UNIVERSO DECLARADO (global del manuscrito)

```
UNIVERSO DECLARADO: árbol /Users/marlene/gw-rw-zerilli, rama main, HEAD ec9cb42,
medido 2026-10-14 (hora UTC junto a cada cifra).
motor = python3 (arneses: -B) 
unidad de las cifras de frontera = dB de energía reflejada (|R_dB|, unidad "energia")
unidad de las cifras de convergencia = orden empírico p sobre refinamiento de malla
tolerancias: umbral_p = 0.05 · umbral de frontera sellado = -40.0 dB · UMBRAL_C5_DB = 0.5
```

**Regla de lectura:** toda cifra afirma con **portador declarado** (archivo · blob · líneas · bytes) y **comando que la respalda**. Una cifra cuya procedencia sea un **asunto de commit** y no un crudo **se declara como compromiso, no como resultado medida** (§4.4). La instrucción que gobierna este manuscrito es no inventar experimentos: se empaqueta lo ya medido y sellado.

---

## 1. Objeto y marco

Se consideran esquemas hiperbólicos **bidimensionales** de tipo *kick-drift* sobre coordenadas de malla, con dos propiedades a certificar:

1. **Orden de convergencia cuadrático** `O(h²)` preservado bajo refinamiento de malla, con extinción del piso de error en arranque de Cauchy simétrico.
2. **Absorción perimetral adiabática** por debajo del umbral sellado de `-40 dB`, sin reflexión parásita de pared y sin contaminación interior.

El frente 2D se organiza en **gates** (`F1`, `F2`, `F3`, `F4`, `F11`) y en una línea **simbólica** (certificación de stencils por reescritura de Taylor). Cada gate tiene su pre-registro sellado en Git **antes** de la primera cifra, su crudo, y su veredicto con causa.

**Estado del frente al cierre de este manuscrito:** `F1` VERDE · `F2` VERDE · `F4` VERDE · `F11` VERDE (nominal) · `F3` **ROJO declarado** con rectificación ratificada en prosa y aún no implementada · **Línea A** certificada (banco must-fail 4/4 discriminado).

---

## 2. Cadena de commits del frente (trazabilidad)

```
41b39ee  data(f4): crudo F4-frontera V2 = FALLA (der -21.68 dB / izq -19.10 dB vs umbral -40 dB)
29f4885  sim: V3 pasada 2 (perfil cubico) PRESERVADA como intermedia — F4 RED -14.19 dB
3958f0f  sim: V3 pasada 3 — perfil LINEAL (p = 1) + L = 96 + dominio (-140, 280). D-G REPARADO
20ad7fb  V3 PASADA 3b: guardas fail-closed de configuracion (no mueven cifras validas)
4f91b88  V3 CERTIFICACION DE FRONTERA (F4) — VERDE. Crudos registrados.
50a1b29  ACTA DE CIERRE — certificacion de frontera V3 (F4 VERDE) — 2026-10-13
4206b50  docs(extractor): apendice de correcciones metrologicas al acta de calibracion
2eebc3b  sello(frente2d): preregistro sellado del frente 2D (t,r*,theta) y fondos curvos
90759a8  ADENDA 1: ratificacion seccion 4 y esquema 2D ratificado
2ae75fd  docs(2d): adenda 1 al preregistro y crudo de dominio medido para gate 2d-f1
39868c6  frente 2D: esqueleto del banco axisimetrico (r*,theta) + F1 medido ROJO en F1.b
bad0358  frente 2D: Gate 2D-F1 VERDE (F1.a 6.000848e-14; F1.b orden 2.0251/1.9246; control 4.913749e+00)
6a186ed  sim/arnes_richardson_2d_f2_v3.py: copia byte-identica del v2 como foto previa del instrumento
f8b788c  feat(sim): certificar Gate 2D-F2 en VERDE (Richardson cuadratico p=2.0028 en nr0=256)
f974578  feat(sim): certificar Gate 2D-F11 en VERDE asintotico (R_dB = -44.94 dB, C5 RC 0 a 3072)
b010768  feat(symbolic): certificar Linea A (stencils por Taylor, banco must-fail 4/4 discriminado)
36ab438  docs(sim): sellar ERRATA 1 del pre-registro Gate 2D-F3 (resoluciones D1-D5)
d0e23da  feat(sim): sellar arnes_zerilli_curvatura_2d_f3.py PRE-R2 (blob fa536467…, 1009 l, POST RC 11)
861c3dd  docs(symbolic): acta de cierre formal Linea A (resolucion colision b010768, vector 4/4 OK)
ec9cb42  test(sim): registrar corrida completa F3 con triple rojo diagnosticado (D9 reparado)   <-- HEAD
```

---

## 3. Gate F1 — orden base y control de manufactura

Veredicto **VERDE** (commit `bad0358`). Denominador declarado: malla axisimétrica `(r*, theta)`, malla de la corrida F1.

| Magnitud | Medido | Rol |
|---|---|---|
| `F1.a` | `6.000848e-14` | residuo de la solución manufacturada |
| `F1.b` orden | `2.025059` (una dirección) · `1.924614` (la otra) | orden empírico medido |
| Control | `4.913749e+00` | valor del control de la corrida |

Reparación registrada en el mismo commit: la inicialización del bucle *kick-drift* usaba `v^{-1/2}` en lugar del medio paso correcto; se corrigió **una línea** y se nombró el invariante en el docstring del `core`. Antes de la reparación, `F1.b` medía orden `1.0163` (ROJO, commit `39868c6`). La diferencia entre `1.0163` y `2.025059` es el efecto de un medio paso mal puesto.

---

## 4. Gate F2 — convergencia cuadrática de Richardson

### 4.1 Portadores

| Propiedad | Valor medido | Comando |
|---|---|---|
| Arnés | `sim/arnes_richardson_2d_f2_v3.py` | — |
| Líneas / Bytes | `800` / `42 099` | `wc -l -c` |
| Blob (disco) | `72844790ba3ef2184d941ed1202c84b88771276b` | `git hash-object` |
| sha256_16 | `2efba187cbb6a038` | `shasum -a 256` |
| Estado en git | limpio | `git status --porcelain` |
| Crudo | `sim/data/crudo_2d_f2_richardson_post_arranque_v3_nr0_256_20261013T204500Z.json` | — |
| Líneas / Bytes del crudo | `310` / `7 132` | `wc -l -c` |
| Blob del crudo | `9935fa1ee1b484aa87c5f5a10f1469a7e7baefdc` | `git hash-object` |
| **Vecino NO adjudicado** | `sim/arnes_richardson_2d_f2.py` — **` M` sucio: no se toca** | `git status --porcelain` |

### 4.2 UNIVERSO DECLARADO y arranque

```
UNIVERSO DECLARADO (F2): N = refinamiento nr0 ∈ {64, 128, 256} · umbral_p = 0.05
arranque = "exacto: u^{-1} = u^0 + 0.5 dt^2 a(u^0), v = (u^0 - u^{-1})/dt"
comando = sim/arnes_richardson_2d_f2_v3.py --estricto --nr0 256 --json
```

### 4.3 Escalera medida (tres renglones, un solo objeto)

| `nr0` | Razón de diferencias | Orden `p` | `umbral_p` | Veredicto |
|---|---|---|---|---|
| `64` | `3.9744790879443896` | `1.990765787067249` | `0.05` | VERDE |
| `128` | `4.003063234816212` | `2.0011044055918528` | `0.05` | VERDE |
| `256` | `4.007945543016709` | `2.0028629063990215` | `0.05` | VERDE |

Celdas del crudo `nr0 = 256`:

- `F2 PRINCIPAL` VERDE: `p = 2.0028629063990215`, `razon = 4.007945543016709`, `d1 = 0.019985206667236667`, `d2 = 0.004986396759321774`, `piso = 1.4005653925511307e-14`.
- `C2 REDUCCION` VERDE: `p = 2.004403069239498`.
- `C3b ANGULAR ORDEN 1` **ROJO**: `p = 0.9857539455144246`.
- `C3a RADIAL ORDEN 1` **NO MEDIBLE**: causa `C1: senal por debajo del piso de redondeo (ORDEN NO MEDIBLE)`.
- `c4` **REFUSADA**: `R2 FAIL-CLOSED: CFL = 0.7500000000 > sellado 0.5000000000 (la cota no se rebaja)`.

### 4.4 Extinción del piso de error (la cifra que sostiene el título)

```
UNIVERSO DECLARADO: corrida nr0 = 256 · arranque exacto · referencia de piso ref_piso_f2
d2        = 4.986396759321774e-03
ref_piso  = 1.081241e-02
factor    = d2 / ref_piso = 0.46117348115006496   (< 1  ⇒ piso extinguido)
```

El patrón anterior era `p = 2.328719` / `0.540266` / `0.862230` en los tres niveles: una escalera **incoherente**, con orden aparente que **bajaba** al refinar. El arranque exacto de Cauchy simétrico extingue ese piso y la escalera pasa a ser monótona hacia `2`. **Declaración de método:** el valor `ref_piso_f2` es una referencia tomada del propio instrumento, no un objeto externo; el factor mide una razón entre dos corridas del mismo arnés.

### 4.5 Modo de cierre y colisión A2.1

`sim/ACTA_CIERRE_2D_F2_VERDE_Y_COMMIT_ATOMICO_20261013.md` registra: ventana de medición `2026-10-13T21:04:05Z → 21:05:07Z` UTC, cwd `/Users/marlene/gw-rw-zerilli`.

- `HEAD` = `f8b788cff91d844794cf36e8cbc18c10a22ab980` a las `21:03:28Z`.
- Primer pre-vuelo A2.1 a las `21:04:05Z` ⇒ el commit se había escrito **37 segundos antes** de la medición.
- **Estado: COLISION A2.1 — la mutación ya estaba escrita. Cero escrituras.**
- Un cuarto crudo (`...T204500Z.json`) entró al commit: idéntico a `T203620Z` salvo `stamp`, `hora_utc`, `segundos` y `comando` ⇒ **determinismo sobre bytes congelados**, declarado como tal (no como medición independiente).

---

## 5. Gate F11 — absorción perimetral (nominal)

### 5.1 Portadores

| Propiedad | Valor medido | Comando |
|---|---|---|
| Arnés | `sim/arnes_capa_absorbente_2d_f11.py` | — |
| Líneas / Bytes | `703` / `32 310` | `wc -l -c` |
| Blob (disco) | `5977cce60c2616e3d196707e3cef29ce8bff710` | `git hash-object` |
| sha256_16 | `fb054652c315e438` | `shasum -a 256` |
| Crudo | `sim/data/crudo_capa_absorbente_2d_f11_20261013T221500Z.json` | — |
| Líneas / Bytes del crudo | `270` / `6 677` | `wc -l -c` |
| Blob del crudo | `c52de2abdba1feea49bedfae726c9fbcde3b53fe` | `git hash-object` |
| Identidad con HEAD | blob disco **==** blob en `HEAD` | `git hash-object HEAD:sim/data/...json` |
| Estado en git | limpio | `git status --porcelain` |
| HUELLA del arnés | `HUELLA-ARNES-CAPA-ABSORBENTE-2D-F11-20261013` | `grep -n HUELLA` |

**Nota de metro (trampa medida):** el crudo lleva embebido un bloque `identidad_self` que describe **al arnés**, no al crudo: `bytes: 32310` y `lineas: 703` son del `.py`; el JSON tiene `270` líneas y `6 677` bytes. Leer el bloque embebido como descripción del crudo es el error natural de este portador.

### 5.2 UNIVERSO DECLARADO de la corrida

```
UNIVERSO DECLARADO (F11 nominal):
malla   : nr0 = 384 · cfl = 0.5 · dt = 0.045706499624780135 · dt_cota = 0.045706499624780135 (dt == cota)
          hr = 0.2506527415143603 · hth = 0.04908738521234052 · nt0 = 33 · nivel = 0
pasos   : nsteps = 1836 · nsteps_off = 2886
geometria: A = 25.0 · L = 24.0 · L_frac = 0.25 · ancho = 96.0 · c = 26.0 · n = 3 · p = 50.0
          integral_gamma = 25.0 · gamma_max = 4.166666666666667
          rs_min = 2.0 · rs_sponge = 74.0 · rs_max = 98.0 · solape = 48.0
          regla_anticolape = "2*L < ancho => C3 INACTIVA POR CONSTRUCCION"
rung    : "E1"
hora    : 2026-10-13T22:39:44Z
```

### 5.3 Resultado nominal

| Magnitud | Medido |
|---|---|
| `R_dB` | `-45.931354463740675` |
| `R_dB_unidad` | `"energia"` |
| `veredicto` | `VERDE` |
| `rung` | `"E1"` |
| `fallos` | `[]` (lista vacía) |
| `p_efectivo` | `50.12532637075718` |
| `max_inc` | `1.0` |

**`-45.931354463740675 dB`** (energía) es la **única** cifra de frontera F11 respaldada por un crudo commiteado hasta el cierre de este manuscrito, y corresponde al escalón nominal `E1` a `nr0 = 384`.

### 5.4 Banco de controles del crudo (todos `ok: true`, `rc: 0`)

| Control | Medición en el crudo |
|---|---|
| `C0` reducción | `diff = 0.0` (exacto) |
| `C1` pared Dirichlet reflectante | `rdb = -1.3461469019746655e-08` · umbral `1.0 dB` · `mur1: false` · `pared_dirichlet_en: 98.0` |
| `C2` no contaminación interior | `residuo_interior` en `[8.110793853111824e-72, 2.3773902065522737e-14]` · umbral `1e-13` |
| `C3` guarda de solape *fail-closed* | provocada con `L_frac 0.55` · `2L_sobre_ancho 1.1` |
| `C4` paquete saliente puro | `ratio 6.081972713140283e-06` · umbral `0.001` |
| `C6` simetría angular | `variacion_theta_max: 0.0` |
| `C7` eco prematuro | `eco_max 0.0030774451728989636` · umbral `0.01` |
| `C8` contención interior *fail-closed* | provocada |

**El crudo contiene los bloques `C0`, `C1`, `C2`, `C3`, `C4`, `C6`, `C7`, `C8`. NO contiene bloque `C5`.**

### 5.5 Escalera declarada y escalera medida

La escalera de parámetros está **declarada** en el crudo con cuatro escalones, y **sólo `E1` fue medido** en esta corrida:

```
E1: A = 25.0  · L_frac = 0.25 · n = 3     <-- medido (R_dB = -45.931354463740675)
E2: A = 100.0 · L_frac = 0.25 · n = 3     <-- declarado, no medido aquí
E3: A = 400.0 · L_frac = 0.25 · n = 3     <-- declarado, no medido aquí
E4: A = 400.0 · L_frac = 0.3  · n = 3     <-- declarado, no medido aquí
```

### 5.6 EL CONTROL `C5` — definido, invocado aparte, y **NO** contenido en el crudo

**Hecho medido.** El arnés **sí implementa** el control `C5`:

- `UMBRAL_C5_DB = 0.5` (línea 83 del arnés).
- Bloque de código del control en las líneas 495–530: `if ctrl == "C5":` construye una escalera radial (`niveles = [int(x) for x in a.ladder.split(",")]`), corre `corrida(...)` por cada `nr0`, calcula `deltas = abs(rdb_{i+1} - rdb_i)`, toma `finos = [d for d in deltas[-2:] if d is not None]` y exige `ok = bool(finos) and max(finos) <= UMBRAL_C5_DB`; devuelve `rc = 0` si `ok`, `rc = 1` si no.
- **Se invoca por separado**: `--solo-control C5 --ladder <lista>`.
- En la ruta no-`C5` el instrumento imprime: `"C5 no corrido: control independiente (--solo-control C5 --ladder %s)"`.

**Hecho negativo, medido dos veces.** El crudo commiteado `...T221500Z.json` (`270` líneas · `6 677` bytes · blob `c52de2ab…` = `HEAD`) **contiene sólo la corrida nominal `E1`**: no tiene celda `C5`, no contiene la cadena `3072`, no contiene `44.94`, no contiene `C5` como bloque. Un `grep` de `3072|"C5"|-44\.|rung|R_dB` sobre el crudo devuelve únicamente: l.2 `"R_dB": -45.931354463740675`, l.3 `"R_dB_unidad": "energia"`, l.29 `"esperado": "|R_dB| <= 1.0 (reflexion total); NO -90.66 dB de Mur-1"` y l.222 `"rung": "E1"`.

**Y la cifra titular del commit no tiene crudo.** El asunto del commit `f974578` enuncia `R_dB = -44.94 dB, C5 RC 0 a 3072`. Un `grep` de `44\.94` sobre todo `sim/` devuelve **exactamente un archivo**: `sim/PREREGISTRO_GATE_2D_F3_ZERILLI_CURVATURA_20261013.md`, línea 50, y esa línea es una **cita del asunto del commit**:

```
> F11 (fronteras absorbentes a -44.94 dB) formalmente certificados en Git (f974578), se
```

El pre-registro del gate F11 (`sim/PREREGISTRO_GATE_2D_F11_20261013.md`, `291` líneas, sha256 `f4b50bb764f82492f4f0a6fbab7bb7d622dc213e627aaf987cdea12eac3abaab`) **tampoco** contiene `C5`, ni `3072`, ni `44.9`, ni el escalón medido. El manifiesto del commit `f974578` son **exactamente 3 archivos**: `sim/PREREGISTRO_GATE_2D_F11_20261013.md` (`291 +`), `sim/arnes_capa_absorbente_2d_f11.py` (`703 +`), `sim/data/crudo_capa_absorbente_2d_f11_20261013T221500Z.json` (`270 +`) — **1 264 inserciones**, y ninguna de ellas contiene el `C5` a `3072`.

**DECLARACIÓN EXPLÍCITA (obligatoria).** La cifra `-44.94 dB` a `3072` celdas con `C5 RC 0` es un **compromiso enunciado en un asunto de commit**, **no** un resultado respaldado por crudo commiteado. El resultado medido y registrado es:

```
R_dB = -45.931354463740675 dB (energia)  ·  nr0 = 384  ·  rung = "E1"  ·  VERDE  ·  fallos = []
portador: sim/data/crudo_capa_absorbente_2d_f11_20261013T221500Z.json
          270 l · 6 677 B · blob c52de2abdba1feea49bedfae726c9fbcde3b53fe (= HEAD)
```

Este manuscrito **no** presenta `-44.94 dB` como resultado medido. Lo presenta como lo que es: la promesa que el instrumento puede cumplir (`C5` existe, está acotado y es invocable), pendiente de corrida con su propio crudo.

---

## 6. Gate F4 — certificación de frontera V3

Veredicto **VERDE** (`sim/ACTA_CIERRE_FRONTERA_V3_20261013.md`).

```
UNIVERSO DECLARADO (F4): umbral sellado = -40.0 dB · amplitud incidente A_incidente = 1.0000
unidad = dB de energía reflejada
```

| Magnitud | Medido |
|---|---|
| Reflexión lado derecho | `-47.48848252620233 dB` |
| Reflexión lado izquierdo | `-47.48845786723316 dB` |
| Umbral sellado | `-40.0 dB` |
| Margen | `+7.4885 dB` |
| Acuerdo entre lados | `2.5e-5 dB` |
| `A_incidente` | `1.0000` |

Crudos: `crudo_rw_zerilli_v3frontera_20261013T183443Z.json` y `crudo_rw_zerilli_v3todo_20261013T183502Z.json`, atados al blob del driver `d6b899c6d142254dd025d6c8ef4b0fbf13d715e7`.

### 6.1 Reparaciones D-F / D-G / D-H y la ley del perfil `p`

El defecto estructural era que la frontera absorbía **de menos** en unos perfiles y **contaminaba** en otros. La serie de reparaciones condujo a un hecho simple: **`p = 1` restaura `int_sigma = A = 25` de forma EXACTA**. La ley medida del perfil:

```
UNIVERSO DECLARADO: perfil p ∈ {0, 0.5, 1, 2} · mismo dominio · misma malla
p = 0    -> -53.2756 dB
p = 0.5  -> -49.8374 dB
p = 1    -> -47.4885 dB      <-- perfil elegido (int_sigma = A exacto)
p = 2    -> -44.2430 dB
```

La serie es monótona: **absorber más fuerte por perfil cúbico cuesta exactitud de la integral**; `p = 1` es el punto en que la identidad de la integral se recupera exactamente y la absorción sigue `7.4885 dB` por debajo del umbral sellado.

### 6.2 Divergencias declaradas

El acta declara **cinco divergencias** y la tabla `F1–F7` del acta registra: `F1` `6` renglones certificados · `F2` `p = 2.0002312004820553 (rw)` y `2.000226129020191 (zerilli)` · `F3` `nota_p = OK` con `d1 = 1.9249e-3 / 2.0058e-3` · `F4` VERDE · `F5` `desv_rel = 0.004276612396287675` · `F6` residuo de `16800` compartido `3.82e-10` con `no-anidado = 0` · `F7` `desv_rel = 0.03363680329482106`.

Cadena de commits de la frontera: `41b39ee → 29f4885 → 3958f0f → 20ad7fb → 4f91b88`.

---

## 7. Línea A — certificación simbólica de stencils por Taylor

### 7.1 Portadores

| Propiedad | Valor medido | Comando |
|---|---|---|
| Instrumento | `sim/certificador_reescritura_stencil_residuo.py` | — |
| Líneas / Bytes | `341` / `13 623` | `wc -l -c` |
| sha256 | `d6eacf02a071e24f8ed523367b7294f75955dd9b774f635ce333d433c6f670e0` | `shasum -a 256` |
| Blob (disco) | `b647d613f1d6c5550e99cabda16206160be2749a` | `git hash-object` |
| Blob (HEAD) | `b647d613f1d6c5550e99cabda16206160be2749a` (**disco == HEAD**, sin deriva) | `git rev-parse HEAD:sim/...` |
| `mtime` (UTC) | `2026-10-13T23:05:19Z` | `stat -f '%Sm' -t '%Y-%m-%dT%H:%M:%SZ'` con `TZ=UTC` |
| Importaciones | `5` (`argparse`, `json`, `sys`, `sympy`, `__future__`) | `grep -n '^import\|^from'` |
| Escritura a disco | `0` (sólo `print`) | `grep -n 'open(\|write('` |
| Acta de cierre | `sim/ACTA_CIERRE_REESCRITURA_STENCIL_RESIDUO_20261014.md` | — |
| Líneas / Bytes del acta | `235` / `12 155` | `wc -l -c` |
| Blob del acta | `d343a6a6545cf98e40cf6edc204372a5b0f91046` | `git hash-object` |
| HUELLA del acta | `HUELLA-ACTA-CIERRE-REESCRITURA-STENCIL-20261014` | `grep -n HUELLA` |
| Pre-registro vecino | `sim/PREREGISTRO_REESCRITURA_STENCIL_RESIDUO_20261013.md` (`303` l · `15 911` B · blob `116d679a6ca5eb2fe67ae34fd0913b9d07ac26f5` == HEAD) | — |

**Trampa de metro declarada en el propio acta:** el patrón `json\.dump` devuelve `2`, y **ambos** son `json.dumps` (serializador a *stdout*). El conteo de «escritura a disco» no viaja por ese patrón: el cero puede ser del metro. Y el contacto del certificador con el arnés son `2` líneas, **ambas comentario** (l.7 y l.35): es un instrumento independiente, no un satélite del arnés.

### 7.2 Método

Reescritura simbólica del stencil por desarrollo de Taylor y comparación **término a término** del residuo con su orden asintótico declarado. El par simbólico base del acto:

```
par_simbolico = [4, "s*(-s**3 + 6*s**2 - 11*s + 6)/24"]
adaptacion_declarada = operador IDENTIDAD (1*u / 0*u' / 0*u'' / 0*u''')
```

El coeficiente del término de orden 4 es `coef = -prod(s-a)/24`: la fórmula cerrada de la familia de diferencias finitas, **generada por el instrumento**, no escrita a mano.

### 7.3 Vector de falsación (banco must-fail discriminado 4/4)

```
UNIVERSO DECLARADO: eps = 1/1000 congelado ANTES de la primera cifra · modo --must-fail
VECTOR RC = C0:0 E1:2 E2:3 E3:1
VECTOR esperado = C0:0 E1:2 E2:3 E3:1        ->  BANCO OK · banco_ok = True
```

Causas tipadas (`rc ≠ 0` con su causa impresa, no sólo el código):

| Caso | `rc` | Causa |
|---|---|---|
| `C0` | `0` | `VERDE: ORDEN p = 4 CERTIFICADO (coef = -prod(s-a)/24)` |
| `E1` | `2` | `RESIDUO_DISIPATIVO_DETECTADO (O(h^2) != 0)` |
| `E2` | `3` | `RESIDUO_DISPERSIVO_DETECTADO (O(h^3) != 0)` |
| `E3` | `1` | `RESIDUO_DE_ORDEN_INFERIOR_DETECTADO (O(h^1) != 0)` |

Un caso que devuelve el código esperado **por otro motivo no discrimina**: por eso el banco exige el par (código, causa). La base del vector está en JSON con `rc = 0`.

### 7.4 Modo de cierre — COLISIÓN A2.1, cero escrituras

El acta de cierre se titula **«CERRADO POR COLISION (cumplimiento pasivo A2.1, cero escrituras duplicadas)»**. La secuencia medida:

1. **Sonda de ausencia** `2026-10-13T22:59:41Z`: el acta **no existía**; `huella_en_repo = 0`.
2. **Gate A2.1 PRE** `2026-10-13T23:59:24Z` → **RC 11** (no `10`): la huella **ya habitaba** el árbol.
3. Entre la sonda y el gate **cupo otra mano** ⇒ la sonda de ausencia **caduca**; el `RC 11` del gate **cerró el frente en vez de duplicarlo**.

Lección de instrumento, aplicable a todo el frente: la sonda de ausencia es una medición **con hora**, y su hora es parte de la sonda.

### 7.5 Identidad del commit base

| Propiedad | Valor |
|---|---|
| commit | `b01076890c07040e53184cb2f380b7adcc52fafc` |
| padre | `f9745784ec88c4b5f94ec4e4b36ed65d9dd1b67a` |
| asunto | `feat(symbolic): certificar Linea A (stencils por Taylor, banco must-fail 4/4 discriminado)` |
| manifiesto | `2 files changed, 644 insertions(+)` → `PREREGISTRO…` (`303 +`) + `certificador…` (`341 +`) |
| cierre formal | commit `861c3dd` (acta de cierre, resolución colisión `b010768`, vector 4/4 OK) |

---

## 8. Gate F3 — curvatura de Zerilli: ROJO declarado

**Este gate no se presenta como verde.** Veredicto **ROJO** con tres controles en rojo y uno no medible.

| Propiedad | Valor medido |
|---|---|
| Crudo | `sim/data/crudo_2d_f3_zerilli_20261014T010849Z.json` |
| Líneas / Bytes | `342` / `11 569` |
| Blob | `a6bc155abbc034386b3b71257eacadd8cda285bd` |
| Controles en rojo | `['C2','C4','C6']` |
| `rc` | `1` |
| Commit de registro | `ec9cb42` (**HEAD**) |
| Arnés sellado | blob `fa536467da94830360445ebaf54292166b70d95a` (`1009` l, commit `d0e23da`) |
| Arnés previo | blob `c3348c5598869c82f6fac0ea7a12cc96486b8430` (`1011` l) |

**Nota de identidad:** el arnés de F3 tiene dos blobs en la historia (`c3348c…` de `1011` líneas y el sellado `fa5364…` de `1009` líneas). **Antes de citar cualquiera de los dos hay que re-medir** cuál está en disco: son objetos distintos con el mismo nombre de ruta.

### 8.1 Rectificación ratificada (en prosa, **no implementada**)

La rectificación está ratificada y **aún no escrita en código**:

- `C2` exige **paquete saliente puro** (`v⁰ = -∂_{r*} u⁰`) en `r* = 26.0`, **o** una ventana de retorno después de la extinción de la cola.
- `C6` pasa a **pureza armónica**: `||Ψ - ψ_{ℓ=2}(r*,t) P₂(cos θ)||_{L2} <= tol(h_θ²)`.
- `C4` queda acotado al **orden de truncamiento acoplado** (`~5.0e-13` a `nr0 = 384`).

Implementar la rectificación exige una **tupla A2.1 nueva** con **huella nueva**: reutilizar la huella `…-R2` devuelve `RC 11` por diseño (la huella ya habita el árbol), lo cual **no** es señal de éxito sino de colisión.

---

## 9. Piezas vecinas y estado sucio declarado

| Pieza | Estado | Acción |
|---|---|---|
| `sim/arnes_richardson_2d_f2.py` | **` M` sucio, no adjudicado** | **NO tocar** |
| `sim/driver_rw_zerilli_1d.py` | `599` l · `25 638` B · sha256_16 `72df3878e2245bd0` · blob `62931cf059d72f797d66b4e6ed9d1b8e0958c95e` | sólo lectura (el acta V3 cita un blob posterior `d6b899c6…` a `708` l) |
| `sim/ACTA_CIERRE_FRONTERA_V3_20261013.md` | F4 VERDE | — |
| `sim/ACTA_CIERRE_2D_F2_VERDE_Y_COMMIT_ATOMICO_20261013.md` | F2 VERDE, colisión A2.1 | — |
| `sim/ACTA_CIERRE_REESCRITURA_STENCIL_RESIDUO_20261014.md` | Línea A, cierre por colisión | — |
| `sim/ACTA_DE_LA_CORRIDA_COMPLETA_F3_ROJO_Y_D9_20261014.md` | F3 ROJO diagnosticado | — |
| `sim/arnes_zerilli_curvatura_2d_f3.py` | dos blobs en historia | **re-medir antes de citar** |

---

## 10. Reproducibilidad

```
cd /Users/marlene/gw-rw-zerilli

# F2 — convergencia cuadrática
git hash-object sim/arnes_richardson_2d_f2_v3.py     # 72844790ba3ef2184d941ed1202c84b88771276b
python3 -B sim/arnes_richardson_2d_f2_v3.py --estricto --nr0 256 --json
git hash-object sim/data/crudo_2d_f2_richardson_post_arranque_v3_nr0_256_20261013T204500Z.json

# F11 — absorción perimetral (nominal)
git hash-object sim/arnes_capa_absorbente_2d_f11.py  # 5977cce60c2616e3d196707e3cef29ce8bff710
python3 -B sim/arnes_capa_absorbente_2d_f11.py --json
git hash-object sim/data/crudo_capa_absorbente_2d_f11_20261013T221500Z.json   # c52de2ab…

# F11 — el control C5, invocado aparte (NO está en el crudo nominal)
python3 -B sim/arnes_capa_absorbente_2d_f11.py --solo-control C5 --ladder <lista>

# Línea A — certificación simbólica de stencils
python3 -B sim/certificador_reescritura_stencil_residuo.py --must-fail   # vector C0:0 E1:2 E2:3 E3:1
```

---

## 11. Límites y declaraciones

1. **`-44.94 dB` a `3072` no es un resultado de este manuscrito** (§5.6). Es un asunto de commit sin crudo commiteado. El resultado medido es `-45.931354463740675 dB` (energía) a `nr0 = 384`, escalón nominal `E1`.
2. **El control `C5` existe y no se corrió en el crudo citado.** Su código está presente (`UMBRAL_C5_DB = 0.5`, líneas 495–530), su invocación es separada (`--solo-control C5 --ladder`), y el crudo commiteado es la corrida nominal. Un control definido y no corrido **no certifica nada** hasta que exista su crudo.
3. **Escalera declarada ≠ escalera medida** (§5.5): `E2`, `E3` y `E4` están declarados y **no** medidos.
4. **Denominadores y unidades**: las cifras de frontera son dB de **energía** reflejada (`R_dB_unidad: "energia"`); las de convergencia son **órdenes empíricos** `p` con `umbral_p = 0.05`; las de la Línea A son **códigos de causa** discriminados, no magnitudes. Sumar cifras de distinta clase en una sola fila es el defecto que este manuscrito evita.
5. **`F3` es ROJO y se declara ROJO**, con su rectificación ratificada en prosa y sin implementar (§8). Un ROJO declarado con causa es un resultado; un ROJO sin causa sería un pendiente.
6. **Hora como parte de la cifra**: las identidades se midieron el 2026-10-14 sobre `HEAD` `ec9cb42`; el árbol puede ser movido por otra mano. Antes de sellar cualquier cita, **re-medir `HEAD` y el blob**.
7. **`F2` §4.4**: el factor `0.46117348115006496` es una razón entre dos corridas del **mismo** arnés (`ref_piso_f2` es referencia del propio instrumento), no una comparación contra un objeto externo.

---

## 12. Índice de portadores citados

| Portador | Líneas | Bytes | Blob (disco) | Estado |
|---|---|---|---|---|
| `sim/arnes_richardson_2d_f2_v3.py` | 800 | 42 099 | `72844790ba3ef2184d941ed1202c84b88771276b` | limpio |
| `sim/data/crudo_2d_f2_richardson_post_arranque_v3_nr0_256_20261013T204500Z.json` | 310 | 7 132 | `9935fa1ee1b484aa87c5f5a10f1469a7e7baefdc` | limpio |
| `sim/arnes_capa_absorbente_2d_f11.py` | 703 | 32 310 | `5977cce60c2616e3d196707e3cef29ce8bff710` | limpio |
| `sim/data/crudo_capa_absorbente_2d_f11_20261013T221500Z.json` | 270 | 6 677 | `c52de2abdba1feea49bedfae726c9fbcde3b53fe` | limpio = HEAD |
| `sim/certificador_reescritura_stencil_residuo.py` | 341 | 13 623 | `b647d613f1d6c5550e99cabda16206160be2749a` | limpio = HEAD |
| `sim/ACTA_CIERRE_REESCRITURA_STENCIL_RESIDUO_20261014.md` | 235 | 12 155 | `d343a6a6545cf98e40cf6edc204372a5b0f91046` | limpio |
| `sim/PREREGISTRO_REESCRITURA_STENCIL_RESIDUO_20261013.md` | 303 | 15 911 | `116d679a6ca5eb2fe67ae34fd0913b9d07ac26f5` | limpio = HEAD |
| `sim/data/crudo_2d_f3_zerilli_20261014T010849Z.json` | 342 | 11 569 | `a6bc155abbc034386b3b71257eacadd8cda285bd` | limpio (ROJO) |
| `sim/arnes_zerilli_curvatura_2d_f3.py` | 1009 | — | `fa536467da94830360445ebaf54292166b70d95a` (sellado `d0e23da`) | **re-medir** |
| `sim/arnes_richardson_2d_f2.py` | — | — | **` M` por otra mano — no se toca** | sucio |

---

**CIERRE.** Las dos cifras que sostienen la parte verde de este manuscrito son:

1. `p = 2.0028629063990215` a `nr0 = 256` (tolerancia declarada `0.05`), con una escalera monótona `1.990765787067249 → 2.0011044055918528 → 2.0028629063990215` y extinción de piso por factor `0.46117348115006496`;
2. `-45.931354463740675 dB` (energía) a `nr0 = 384`, escalón nominal `E1`, con margen `+7.4885 dB` respecto del umbral sellado `-40.0 dB` en el gate F4 (`-47.48848252620233 / -47.48845786723316 dB`).

Y la declaración que sostiene la honestidad del resto: la cifra `-44.94 dB` a `3072` celdas con `C5 RC 0` **no tiene crudo commiteado**; vive en el asunto del commit `f974578` y en una cita de línea 50 de un pre-registro. **Se declara, no se adjudica.**
