# ACTA DE CIERRE — CERTIFICACIÓN DE FRONTERA V3 (F4 VERDE) — 2026-10-13

ESTADO: **F4 VERDE**. Ambos lados caen por debajo del umbral sellado (-40 dB) con
`sponge_A = 25` intacto. La certificación de frontera queda cerrada.

UNIVERSO DECLARADO: 2 archivos crudo registrados en `sim/data/` (V3) + 1 driver
(708 líneas) + 1 pre-registro sellado (94 líneas).
MOTOR: `python3 -B sim/driver_rw_zerilli_1d.py`, leapfrog 1D en coordenada tortuga,
numpy 2.4.6 / scipy 1.17.1 / Python 3.14.7, macOS, `TZ=UTC`.
UNIDAD: dB (coeficiente de amplitud de reflexión 20*log10), líneas, nodos, segundos.
VENTANA: `--modo frontera --offset no-anidado`, k = 0 (malla gruesa no anidada),
dominio (-140.0, 280.0), `--sponge-L 96.0`, `--sponge-A 25.0`, `--cfl 0.5`,
`--sigma_f 2.0`; t_incidente 20.0 / 6.0, t_reflejado 340.0 / 234.0.

---

## §1 — ORDEN

Vía (a) del dueño: reparar la esponja en V3 y **correr `--modo frontera --offset
no-anidado` con `sponge_A = 25` sellado, verificando que AMBOS lados caigan por
debajo de -40 dB**. La vía (b) (esponja apagada) fue **prohibida**: esquivaría el
parámetro pre-registrado. Todo el ciclo corrió bajo el gate **A2.1**.

## §2 — RESULTADO (crudo `v3frontera`)

| lado | x_frontera | x_monitor | A_incidente | A_reflejado | coef_amplitud | dB | toca_F4 | estable |
|---|---|---|---|---|---|---|---|---|
| derecha | 280.0 | 120.0 | 1.00002250107925 | 0.004222655443310207 | 0.004222560431143307 | **-47.48848252620233** | False | True |
| izquierda | -140.0 | -26.0 | 1.000022761520867 | 0.004222668531047619 | 0.0042225724188773945 | **-47.48845786723316** | False | True |

- Umbral sellado: **-40.0 dB** (`UMBRAL_F4_DB`). Margen: **+7.4885 dB**.
- Los dos lados coinciden a **2.5e-5 dB** (control de simetría del montaje).
- `A_incidente` = 1.0000 en ambos lados: el monitor mide la incidente LIMPIA
  (defecto D-F corregido; el monitor izquierdo vivía en -30, dentro de la capa).

## §3 — CRUDOS REGISTRADOS (contención 2)

| archivo | bytes | sha256 | commit |
|---|---|---|---|
| `sim/data/crudo_rw_zerilli_v3frontera_20261013T183443Z.json` | 1764 | `cfd9acdbd9de0582d03b0c6400c7a928f205a8bb9b5010fe26bb7792317e85a4` | `4f91b88` |
| `sim/data/crudo_rw_zerilli_v3todo_20261013T183502Z.json` | — | `b7965db64a9480cf45381b0ecd3a24a521abe9893b62205925345ddb7980c7d5` | `4f91b88` |

Ligados al blob del driver **`d6b899c6d142254dd025d6c8ef4b0fbf13d715e7`**
(HEAD `20ad7fb`, 708 líneas, sha256
`45e63b3803a515958addcb247fb6757e63f13f2d22a7a8164c1f01cf29eccf98`).

## §4 — REPARACIONES QUE PRODUJERON EL VERDE

1. **D-F (monitor dentro de la capa).** El monitor izquierdo estaba en -30, dentro
   de la capa [-140,-44], midiendo una incidente ya atenuada (A_inc = 0.7317). Se
   movió a **-26**: A_inc = 1.0000.
2. **D-G (la absorción declarada se había partido a la mitad).** Con
   `sigmax = 2*sponge_A/sponge_L` fijo, el perfil cúbico p=3 daba
   `int_sigma = 12.50022` contra la ley de la referencia
   `int_0^L sigma dxi = sigmax*L/(p+1)`. **p=1 restaura `int_sigma = A = 25`
   EXACTO** sin tocar la línea de `sigmax`.
3. **D-H (gobierna L/sigma_f, no la curvatura).** El cruce de F4 ocurre en
   **L/sigma_f ~ 24**; confirmado a 4 dígitos con dos pares independientes:
   (L=48, sigma_f=2) = -40.8565 y (L=96, sigma_f=4) = -40.8541. Con A = 25
   preservado: L=12 -24.2912 | L=48 -40.8565 | L=96 -47.4885.
4. **Pasada 3b (guardas fail-closed).** Config degenerada (2L >= ancho del dominio)
   se volvía **MUDA** en vez de fallar. Guarda A en `solve()` y guarda B en
   `suite_frontera()`, ambas con `SystemExit` que carga los números. Validadas con
   control positivo (aborta) y negativo (corre normal).

## §5 — DIVERGENCIAS DECLARADAS (no reparadas)

1. **El pre-registro sellado NO sella ningún número de esponja.** Sella el umbral
   -40 dB, CFL = 0.50 y "condiciones absorbentes a ambos extremos". `sponge_A = 25.0`
   y `sponge_L = 96.0` viven como **DEFAULTS del CLI**: la reparación viaja en
   defaults y la corrida nominal no necesita flags.
2. **Fórmula de offsets.** El §4 sellado escribe `delta_k = k*Delta_k/3`; el modo
   `no-anidado` (el que la orden usa) implementa `delta_k = k*Delta_0/3`. Las dos
   quedan medidas en el crudo F6 (`literal`: deltas [0, 0.008333, 0.008333]) y no se
   elige por el dueño.
3. **D-E refutado en su cura propuesta.** Más suavidad es **peor**. A int_sigma = 25
   con L = 96: p=0 (escalón) -53.2756 > p=0.5 -49.8374 > **p=1 (rampa) -47.4885** >
   p=2 -44.2430. El perfil más PLANO gana porque tiene el menor pico
   `sigmax = (p+1)*A/L`; ley medida ~6 dB por halving de sigmax. La referencia ya lo
   decía: `|R| ~ sigma/(4*omega)`.
4. **Config degenerada.** Con L=96, un dominio más angosto que 2L solapa las capas y
   no deja dominio físico; interfaces cruzadas en +56.0 / +54.0 en el dominio V2
   (-40,150). Remediado con guardas, **no** bajando el umbral sellado.
5. **F3 es un piso de MEDIBILIDAD, no una cota de `d1`.** El pre-registro §7 dice
   `d1 < 2.2e-14`; el driver lo implementa como `abs(d1) < UMBRAL_F3*escala` =>
   "ORDEN NO MEDIBLE". Con `nota_p = OK`, `d1 = 1.9249e-3` (rw) / `2.0058e-3`
   (zerilli): el orden SE MIDIÓ.

## §6 — CONTENCIONES CUMPLIDAS

1. **No se tocó ningún artefacto sellado vecino**: ni `PREREGISTRO_RW_ZERILLI_20261013.md`,
   ni el extractor, ni `reflexion_frontera_1d.py`, ni `reflexion_escala_D.py`.
2. **Crudo V3 registrado** en `sim/data/`, commit aislado ligado al blob V3 (tabla §3).
3. **El residuo no contamina la ventana de extracción**: la cola tardía NUNCA supera
   a la reflexión prompt (L=96: -49.1726 tardío vs -47.4885 prompt).
4. **Control de dominio**: p=1/L=48 da -40.8565 **bit-idéntico** en (-90,180),
   (-140,280) y (-200,400) => la reflexión es propiedad de la CAPA, no del borde.
5. **Control de validez A = 0**: der -90.6623 / izq -90.6620 (Mur-1 solo pasa F4 con
   ~50.66 dB); con `--rsmax 200` y A = 25 vuelve a -21.68/-19.10 => el reflector es
   la esponja, no el borde del dominio.

## §7 — PROTOCOLO A2.1 DE ESTA ACTA

- PRE: `bash tools/gate_pre_escritura.sh /Users/marlene/gw-rw-zerilli/sim/ACTA_CIERRE_FRONTERA_V3_20261013.md NO-EXISTE-BLOB "<huella>" 0`
  -> **RC 10** (`no existe`) a las **18:36:25Z** = ausencia medida, cero colisión.
  *Lectura declarada: para una CREACIÓN, RC 10 es la evidencia de ausencia.*
- Nota de casa: `/Users/marlene/platino-labs` **no es árbol git** => el gate devuelve
  **RC 14** (fail-closed) y esta acta no podía escribirse allí; por eso vive en el
  árbol git que contiene el objeto certificado.

## §8 — VEREDICTOS F1–F7 (crudo `v3todo`, 14.27 s, dominio ampliado)

| gate | veredicto | cifra | umbral sellado |
|---|---|---|---|
| F1 | PASA | 6 filas certificantes, `cfl_certificante = 1.0` | 1e-12 |
| F2 | OK | p = 2.0002312004820553 (rw) · 2.000226129020191 (zerilli) | abs(p-2) > 0.15 |
| F3 | OK | `nota_p = OK`; d1 = 1.9249e-3 / 2.0058e-3 | piso 2.2204e-14 |
| F4 | **VERDE** | -47.48848252620233 / -47.48845786723316 dB | -40.0 |
| F5 | PASA | isospectralidad desv_rel = 0.004276612396287675 | 1e-2 |
| F6 | medido | literal: 16800 compartidos resid 3.82e-10 (par 1,2); no-anidado: 0 en los tres pares | tol 1e-9 |
| F7 | PASA | leaver desv_rel = 0.03363680329482106 | 5e-2 |

Todas las filas de `fisica.*` con `estable = True`.

## §9 — CADENA DE COMMITS

`41b39ee` (crudo V2 F4 ROJO, -21.68/-19.10) -> `29f4885` (V3 pasada 2) ->
`3958f0f` (V3 pasada 3, numstat 73 29) -> **`20ad7fb`** (V3 pasada 3b: guardas,
numstat 43 0) -> **`4f91b88`** (crudos de la certificación, numstat 2 0).
