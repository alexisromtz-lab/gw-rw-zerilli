# PREREGISTRO SELLADO — EXTRACTOR ESPECTRAL DE POLOS COMPLEJOS (PRONY / MATRIX PENCIL)

HUELLA: HUELLA-EXTRACTOR-ESPECTRAL-PRONY-MATRIXPENCIL-20261013

- `T_UTC_VENTANA`: 2026-10-13T10:45:38Z
- `UNIVERSO DECLARADO`: `sim/PREREGISTRO_EXTRACTOR_ESPECTRAL_20261013.md` (1 pieza) + `sim/driver_rw_zerilli_1d.py` (1 pieza, sólo lectura)
- `MOTOR`: python 3.14.7 · numpy 2.4.6 · scipy 1.17.1
- `UNIDAD`: línea · polo · valor singular · muestra · decibelio
- `VENTANA`: reloj UTC impreso en la cabecera del crudo

## §0 · Contrato A2.1 (pre-vuelo bloqueante)

| fase | comando | RC esperado |
|---|---|---|
| PRE | `bash tools/gate_pre_escritura.sh <TARGET> AUSENTE <HUELLA> 0` | **10** (destino no existe) |
| WRITE | `create_file` | — |
| POST | `bash tools/gate_pre_escritura.sh <TARGET> <BLOB_POST> <HUELLA> <LINEAS_POST>` | **11** (huella presente) |

- TARGET = `sim/PREREGISTRO_EXTRACTOR_ESPECTRAL_20261013.md`.
- PRE medido: `T_UTC=2026-10-13T10:45:38Z` · **RC=10** · `git status --porcelain -uall` = 2 entradas (`?? sim/__pycache__/driver_rw_zerilli_1d.cpython-314.pyc`, `?? sim/driver_rw_zerilli_1d.py`).
- PROHIBIDO escribir `sim/extractor_polos_matrixpencil.py` antes de que este pre-registro tenga POST con RC 11.
- Nota de contrato: un `BLOB_PRE` vacío devuelve **RC 20** (contrato incompleto). Para un objeto nuevo el token es `AUSENTE`; el gate corta en la fase 1 con RC 10 antes de comparar blob.

## §1 · Objeto, alcance y frontera

OBJETO: instrumento determinista que extrae los polos complejos `s_n` de una serie temporal real muestreada uniformemente, dominada por oscilaciones amortiguadas:

```
Psi(t) = Suma_n Re[ A_n * exp( s_n * t ) ] ,  s_n = -w_I,n + i*w_R,n ,  A_n = |A_n| * exp(i*p_n)
```

con `w_I,n > 0` (decaimiento). Devuelve `(w_R,n, w_I,n)` y `(|A_n|, p_n)`.

ALCANCE:
1. Extractor algebraico **Matrix Pencil Method (MPM)** — matrices de Hankel + descomposición en valores singulares.
2. Contraste declarado: **Prony / predicción lineal (LP)** sobre la misma serie, con idéntico contrato de entrada y salida, como segunda ruta independiente del álgebra.
3. Test sintético de calibración (control cerrado): señal analítica generada **en memoria**, con polos conocidos y ruido gaussiano **controlado** (semilla declarada).
4. Criterio: precisión de máquina (`<= 1e-14` relativo) sin ruido; y **mapa de la cota de error** como función del SNR y de la ventana temporal de corte.

FRONTERA (declarado AJENO, no se toca):
- El solucionador de fondo (`gw-rw-zerilli`) es **escalar Klein-Gordon** (Regge-Wheeler / Zerilli, sin ligadura dinámica), **no** Maxwell. El caso de **cavidades Maxwell con pérdidas** es un **destino de reúso** de este instrumento, no una validación suya (ver §9).
- Leaver `M*w = 0.37367 - 0.08896 i` (l=2, n=0) entra como **referencia externa citada [REF]**, no autogenerada.

## §2 · Contrato de entrada (medido, no supuesto)

MEDIDO (`T_UTC=2026-10-13T10:45:38Z`; `UNIVERSO DECLARADO`: `sim/driver_rw_zerilli_1d.py`, 565 líneas · 23523 B · sha16 `790aa7ae7ea02d19`):

- `solve()` **sí** devuelve la serie en su diccionario de retorno: línea 252, `"t": ts, "psi_obs": obs`.
- El **crudo JSON del driver NO exporta la serie**: `res` (líneas 539-548) lleva sólo `cabecera`, `F6_mallas`, `N_RW_0_nulo`, `F4_frontera` y `fisica`; las filas de `fisica` llevan `A`, `y8`, `pico_obs`, `fit`, `estable` — **no** la serie. `grep -cF '"serie"'` = **0**.

Consecuencia: el extractor acepta **tres** entradas, en este orden de precedencia.

1. `--desde-driver`: importa `driver_rw_zerilli_1d` **en modo lectura** (ese archivo jamás se modifica: es de otra mano y no está rastreado) y llama `solve()` para obtener `(t, psi_obs)` **en memoria**. Es la ruta de certificación.
2. `--serie FILE`: dos columnas `t` y `Psi` (separadas por blanco, `#` = comentario) o JSON con claves `t` y `psi` (o `psi_obs`).
3. `--modo sintetico`: señal generada en memoria (calibración cerrada, §5). No toca el driver.

`UNIVERSO DECLARADO` del instrumento al sellar: este pre-registro (1 pieza) + `sim/driver_rw_zerilli_1d.py` (1 pieza, sólo lectura) + el crudo que el instrumento escriba.
`MOTOR`: python 3.14.7 · numpy 2.4.6 · scipy 1.17.1. Sin red, sin estado oculto; la única aleatoriedad es el ruido sembrado y declarado.
`UNIDAD DECLARADA`: línea · polo · valor singular · muestra · decibelio.
`VENTANA DECLARADA`: reloj UTC impreso en la cabecera del crudo, en el mismo renglón que el `UNIVERSO` y el `MOTOR`.

## §3 · Álgebra sellada

Fijadas `N` muestras `y[0..N-1]` y el paso `dt`.

1. Normalización `y <- y / max|y|` (declarada; se reporta el factor).
2. **Matrices de Hankel** con `M` filas, `L` columnas, `M + L = N`:
   `Y0[m,k] = y[m+k]` y `Y1[m,k] = y[m+k+1]`, con `m` en `[0,M)` y `k` en `[0,L)`.
3. **SVD**: `Y0 = U * S * V^H`, con `S = diag(s_1 >= s_2 >= ...)`.
4. **Truncación de rango**: `r = 2K` **declarado a priori** (K = número de polos complejos = número de pares conjugados). La detección automática `s_i/s_1 < 1e-12` se permite **sólo como diagnóstico**, nunca como sustituto de `r`.
5. **Polos**: `Z = inv(S_r) * U_r^H * Y1 * V_r` (matriz r x r); autovalores `z_k = eig(Z)`.
6. **Paso al plano s**: `s_k = ln(z_k) / dt`. Se acepta `Im(s_k) < 0` y se refleja por conjugación **declarada** (la serie es real).
7. **Amplitudes**: mínimos cuadrados sobre la Vandermonde `V[m,k] = z_k^m`, `m` en `[0,N)`, usando las columnas `z_k` y `conj(z_k)`.

**Contraste Prony / LP**: `y_m = Suma_{k=1..p} a_k * y_{m-k}` resuelto por mínimos cuadrados sobre `p = 2K` retardos; las raíces de `z^p - Suma a_k z^(p-k)` son los polos; amplitudes con la misma Vandermonde. Se reporta **la discrepancia entre rutas**; no se elige una.

**Notación obligatoria del error** (el logaritmo es un mapa que amplifica): `ds = dz / (z * dt)`, de donde `ds/s = dz / (z * |s| * dt)`. Por lo tanto la precisión absoluta en `s` **no** se puede separar de `dt`: es propiedad del **par** `(dt, |s|)`, no del extractor. Se imprime `|s| * dt` junto a cada error.

## §4 · Parámetros sellados

| parámetro | valor sellado | por qué |
|---|---|---|
| `L` (columnas) | `floor(N/2)` | ventana de Sarkar `N/3 ... 2N/3`; se declara |
| `M` (filas) | `N - L` | se cumple `M + L = N` |
| `r` (rango) | `2K` declarado | la auto-detección es sólo diagnóstico |
| `rank_rel` (diagnóstico) | `1e-12` | umbral de valor singular relativo |
| semilla de ruido | `20261013` | declarada |
| ventana por defecto | `[t1, t2]` del crudo | sellada por `--t1` y `--t2` |
| `p` (Prony) | `2K` | mismo rango declarado |

## §5 · Caso sintético de calibración (control cerrado)

Generado **en memoria**, sin leer nada del disco. Con `K = 3` polos, `N` muestras y `dt` declarado:

| n | s_n | w_R,n | w_I,n | mod A_n | fase p_n | origen |
|---|---|---|---|---|---|---|
| 1 | -0.08896 + 0.37367 i | 0.37367 | 0.08896 | 1.00 | 0 | **Leaver l=2 n=0 [REF]** |
| 2 | -0.20000 + 0.60000 i | 0.60000 | 0.20000 | 0.50 | pi/3 | sintético declarado |
| 3 | -0.12000 + 0.15000 i | 0.15000 | 0.12000 | 0.25 | -pi/5 | sintético declarado |

`Psi(t_m) = Suma_n mod(A_n) * exp(-w_I,n * t_m) * cos(w_R,n * t_m + p_n)`, con `t_m = m * dt`.

Sub-casos declarados: `K=1` (sólo n=1) · `K=2` (n=1 y 2) · `K=3`. **Se reportan los tres**: si `K=1` no alcanza `1e-14`, el techo es del metro y no del caso.

Ruido: `n_m` normal estándar con semilla `20261013`, aplicado **después** de generar `Psi` limpia y escalado para el SNR objetivo.

## §6 · Definiciones operativas (lo que decide la respuesta si no se declara)

- **SNR (declarado)**: razón de energía sobre **la misma ventana de extracción**, `SNR_dB = 10 * log10( Suma_m y_m^2 / Suma_m n_m^2 )`. No es SNR de pico ni por muestra. Se imprime el par `(SNR_dB objetivo, SNR_dB medido)`.
- **Ventana de corte** `W`: muestras desde el inicio de la serie, con `W <= N`. Se expresa también en **periodos del modo más lento**: `W / T_3`, con `T_3 = 2*pi/w_R,3`.
- **Error**: **relativo complejo** `err_n = |s_n^rec - s_n^ref| / |s_n^ref|`. Se reporta además el error **absoluto** en `w_R` y en `w_I` por separado (un relativo complejo puede esconder que sólo uno de los dos se movió).
- **Emparejamiento rec <-> ref**: por vecino más cercano en el plano `s`, con **cota declarada** `|ds| < 0.25 * |s|`; un polo sin pareja se cuenta como **no recuperado** y no se descarta en silencio.
- **Piso de redondeo**: `eps = 2.220446049250313e-16`. Ningún error por debajo de `eps` cuenta como medición.

## §7 · Cortes de fallo — SELLADOS ANTES DE LA PRIMERA LÍNEA DE CÓDIGO

| id | condición | consecuencia |
|---|---|---|
| **C1** | sin ruido, error relativo de polo `<= 1e-14` | **éxito** (lo pedido) |
| **F1** | sin ruido, error relativo `> 1e-13` | el extractor **no alcanza precisión de máquina**: se declara y se mide el piso real; **no se pinta verde** |
| **F2** | sin ruido, rango detectado distinto de `2K` | fallo de instrumento: el `r` declarado no está en el objeto |
| **F3** | brecha singular `s_{2K}/s_{2K+1} < 1e6` | separación **sucia**: se declara; el error reportado no es atribuible al álgebra |
| **F4** | `cond(Z) > 1e10` | se declara mal condicionado; no se adjudica |
| **F5** | residuo de apareamiento conjugado `> 1e-10` | la serie no se leyó como real: fallo de instrumento |
| **F6** | el error debe **bajar** al subir el SNR | se **declara la tendencia**; **no se adjudica** con una sola tirada |
| **F7** | `W < 20` periodos del modo más lento | **frontera**: se declara el umbral de ventana; no se reporta como fallo del extractor |
| **F8** | contraste contra Leaver `> 5e-2` | **DIVERGENCIA DECLARADA** (mismo umbral que F7 del pre-registro del driver) |

Regla de lectura de F3, F4 y F7: son **defectos de dominio del metro**, no del objeto. Un rojo ahí **declara**; no repara ni baja umbrales.

## §8 · Barridos (mapa de la cota de error)

1. **dt** en `{0.0125, 0.025, 0.05, 0.1, 0.2, 0.5}` — para exponer `ds/s = dz/(z*|s|*dt)`. Se incluye `0.0125`, que es el `dt` del driver en `k=2` (`cfl*h` con `cfl=0.50` y `delta0=0.05`), para **medir el piso del driver**; los valores mayores muestran el techo propio del álgebra.
2. **SNR** en `{140, 120, 100, 80, 60, 40, 20}` dB — cota de error contra ruido.
3. **Ventana** como fracción de `N` en `{20, 40, 80, 160, 320}` periodos del modo lento, recortando por la izquierda desde el fin de la serie (declarado).

Cada celda imprime `(dt, SNR objetivo, SNR medido, W, err_R, err_I, err_complejo_rel, s_{2K}/s_{2K+1}, cond(Z), rango detectado)`. Una celda no medida se imprime como `null`, **no** como `0`.

## §9 · Controles

- **INTERNO (cierre algebraico)**: MPM contra Prony/LP sobre la **misma** serie — dos rutas independientes con el mismo contrato. La discrepancia se declara.
- **CERRADO (calibración)**: polos conocidos en memoria: el error **es medible**, no estimado (§5 y §6).
- **EXTERNO (destino de reúso)**: cavidades **Maxwell con pérdidas** — declarado como **uso futuro**; `sim/maxwell2d.py` (sha16 `1db75ea7b0b8cba4`) y `sim/maxwell2d_nl.py` (sha16 `79cf04d291aaeb3c`) quedan **citados, no abiertos** en este ciclo.
- **FÍSICO (certificación)**: la serie `psi_obs` del driver `gw-rw-zerilli` en `k=2` y `robs=40.0`, contrastada contra Leaver `0.37367 - 0.08896 i`.

## §10 · Procedencia y no elevación

- La referencia Leaver entra como **[REF]**: citada del pre-registro sellado del driver (`sim/PREREGISTRO_RW_ZERILLI_20261013.md`, sha16 `dbc61ca2d0addae7`), no autogenerada.
- Regla de la casa: **no se eleva** ninguna afirmación con menos de dos casos.
- Una cifra sin hora no es cifra: todo conteo viaja con `UNIVERSO DECLARADO`, `T_UTC`, unidad y motor.
- Este pre-registro **no se edita** una vez sellado: sólo recibe apéndices.

## §11 · Estado y paso siguiente

ESTADO: pre-registro sellado. `sim/extractor_polos_matrixpencil.py` **no existe todavía** y **no se escribe** hasta que el POST de este archivo devuelva RC 11.

PASO SIGUIENTE: `create_file sim/extractor_polos_matrixpencil.py` (gate PRE con RC 10, escritura, gate POST con RC 11).
