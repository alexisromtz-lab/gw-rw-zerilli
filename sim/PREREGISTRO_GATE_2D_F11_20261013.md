# PRE-REGISTRO · GATE 2D-F11 — LEY DE LA CAPA ABSORBENTE 2D (re-medida, no heredada)

    HUELLA      : HUELLA-PREREGISTRO-GATE-2D-F11-20261013
    FECHA       : 2026-10-13
    MOTOR       : python3.14 + numpy (sin scipy, sin red, sin aleatoriedad, sin estado oculto;
                  mismo argv => misma salida; corridas con `python3 -B`)
    CASA        : sim/driver_rw_zerilli_2d.py  (tabla de gates, l.91–92: "f11")
    ORDEN A2.1  : TARGET sim/PREREGISTRO_GATE_2D_F11_20261013.md ·
                  BLOB_PRE NO_EXISTE_PRE10 · HUELLA-PREREGISTRO-GATE-2D-F11-20261013 ·
                  LINEAS_PRE 0 · RC esperado 10 (AUTORIZACIÓN DE CREACIÓN)
    GATE PRE    : RC 10 obtenido el 2026-10-13T21:05:53Z
                  (`bash /Users/marlene/platino-labs/tools/gate_pre_escritura.sh <TARGET> NO_EXISTE_PRE10 HUELLA-PREREGISTRO-GATE-2D-F11-20261013 0`)
    ESTADO      : SELLO DE REGLAS. **Cero ejecución numérica.** No se ha corrido ninguna malla 2D,
                  ninguna capa, ningún extractor para este gate.

---

## Sección 0 · Objeto y lugar del sello

Este documento sella los invariantes del **Gate 2D-F11** ("ley de la capa absorbente 2D") **antes de
la primera cifra**. Nace de dos fuentes que ya viven en la casa y no se re-miden aquí:

1. La fila F11 sellada en `sim/PREREGISTRO_FRENTE_2D_CQG_20261013.md` §6:
   > F11 | ley de la capa absorbente 2D **re-medida** (no heredada del 1D) | si el exponente 2D difiere
   > del 1D (−1.3936) en mas del residuo del ajuste (3.0 por ciento) | DIVERGE: manda la ley 2D;
   > **prohibido dimensionar con la ley 1D**
2. El veto ya escrito en `sim/PREREGISTRO_RICHARDSON_2D_F2_20261013.md` §8:
   > **Absorcion perimetral VEDADA** (gate F11): no se hereda la ley 1D (`R_t = 9.8807e-02 · D^(-1.3936)`,
   > residuo maximo 3.021e-02) ni se dimensiona ninguna capa. La ley de la capa 2D se **re-mide** en F11
   > con su propia fuente; usar -1.3936 como prior esta prohibido por el §3 de la pieza sellada.

UNIVERSO DECLARADO de las cifras de este sello: los dos drivers 1D/2D del sandbox
(`sim/driver_rw_zerilli_1d.py`, `sim/driver_rw_zerilli_2d.py`) y las tres piezas selladas citadas.
No hay universo más ancho; no se extrapola fuera de él.

---

## Sección A · Universo declarado y física congelada

| invariante | valor sellado | procedencia |
|---|---|---|
| parámetro de espín | `M = 0.0` **estricto** (espacio plano bidimensional) | `sim/PREREGISTRO_RICHARDSON_2D_F2_20261013.md` §8; F2 ya cerró VERDE con esta frontera congelada |
| potencial | **Zerilli desactivado** (`V ≡ 0` fuera de la capa) | ídem |
| coordenadas | plano 2D $(r^*,\theta)$; operador angular en base de armónicos **o** modos acoplados, declarado en el crudo | `sim/PREREGISTRO_FRENTE_2D_CQG_20261013.md` §4 |
| CFL | $\mathrm{CFL} = 0.50$ | driver 2D: `--cfl CFL_SELLADO` (l.483); la cota efectiva con término angular se **mide** en F9, no se supone |
| arranque | **Cauchy exacto**, certificado en F2: $v^{-1/2} = -\tfrac{1}{2}\,\Delta t\,a^0$ | `sim/arnes_richardson_2d_f2_v3.py` (commit `f8b788c`); F2 es el criterio `\|p-2\| \le 0.05` |
| dominio radial | por defecto `--rs-min 2.0 --rs-max 14.0` (ancho 12.0) — **sujeto a la desigualdad obligatoria de la Sección B** | `sim/driver_rw_zerilli_2d.py` ll.479–480 |

La física de este gate es **una capa absorbente en espacio plano**: no entra curvatura, no entra
rotación, no entra el extractor. La no-contaminación interior se mide contra la solución exacta en
espacio infinito (Control C2, Sección E).

---

## Sección B · Geometría y perfil de la esponja

### B.1 Capa y perfil (sellado)

- Capa **perimetral exterior** activada a partir de $r^*_{\text{sponge}} = r^*_{\text{max}} - L_{\text{sponge}}$.
- Perfil **monótono creciente**, $\mathcal{C}^1$ o superior:

$$\gamma(r^*) \;=\; \gamma_{\max}\left(\frac{r^* - r^*_{\text{sponge}}}{L_{\text{sponge}}}\right)^{n},
\qquad n \in \{2,3\}$$

- Esponja **interna y angular idénticamente nula**: $\gamma \equiv 0$ para $r^* < r^*_{\text{sponge}}$ y
  en el eje/polo. Se implementa como **cero estructural** (máscara exacta, no valor pequeño), de modo que
  el interior no recibe ni un término disipativo — condición necesaria para que C2 (Sección E) mida lo
  que dice medir.
- **Sin ajuste libre post-hoc:** $\gamma_{\max}$ y $L_{\text{sponge}}$ se fijan en la corrida **antes** de
  la primera cifra de reflexión y no se mueven después de verla.

### B.2 Pico declarado numéricamente (sellado, sin ajuste posterior)

La casa contiene **dos asignaciones incompatibles** para pasar de la deuda de la integral al pico. Se
imprime el par y **se elige una declarándolo** (robustez accidental no se reclama: si conviene, se
declara elegida):

UNIVERSO DECLARADO para las cuatro cifras de esta tabla: `A = 25.0` (default `--sponge-A`,
`sim/driver_rw_zerilli_1d.py` l.659) y `ω = 1.0` (l.485) ⇒ `λ = 2π/ω = 6.283185307179586`.

| asignación | regla | γ_max (n=2) | γ_max (n=3) | ∫γ dr* realizado |
|---|---|---|---|---|
| **M1 — ELEGIDA** | $\gamma_{\max} = (n+1)A/L$ ⇒ ∫γ = A **exacto** | `10.851473392629227` | `14.468631190172301` | `25.000000000000000` en los dos |
| M2 — NO ELEGIDA | $\gamma_{\max} = 2A/L$ (fórmula literal de `sponge_sigma`, l.299) | `7.234315595086151` | `7.234315595086151` | `16.666666666666668` (n=2) · `12.500000000000000` (n=3) |
| L de referencia | $L = 1.1\lambda = 6.911503837897546$ (prescripción del acta 1D: `D = 1.1 λ_min` para −40 dB) | | | |

**Por qué M1 y no M2 (declarado, no adjudicado):** M2 es la asignación cuyo defecto la casa **ya pagó y
declaró** (D-G: «el defecto era del MAPEO sigmax(A,p,L), no del perfil»; medido por trapecio
`p=1 -> 25.00000 · p=2 -> 16.66681 · p=3 -> 12.50022` ⇒ con `p=3` la integral valía `A/2`, no `A`).
Con la familia ordenada $n \in \{2,3\}$ el defecto **volvería por construcción** bajo M2. M1 lo cierra por
álgebra y, además, hace **comparables** n=2 y n=3 (misma deuda acumulada, distinta suavidad) — que es
exactamente la comparación que este gate necesita. Las cifras de M2 quedan impresas arriba para que la
elección sea auditable.

### B.3 Desigualdad obligatoria del dominio (guard de solape, primero en la lista)

La capa se mide **desde el extremo**: si $2L_{\text{sponge}} \ge$ ancho radial del dominio, las dos capas
se solapan, sus interfaces se cruzan y **no queda dominio físico**. La corrida *no falla: se vuelve muda*
(probe estructural documentado en la casa: dominio V2 $(-40,150)$ con $L=96$ ⇒ interfaces `+56.0` y
`+54.0` cruzadas, región física vacía). De ahí la regla fail-closed: *una salida que no puede diferir no
es evidencia* ⇒ `SystemExit` (es el Control C3 de la Sección E).

Con el $L$ de la prescripción del acta ($L = 6.911503837897546$, Sección B.2):

| configuración | L (uds-x) | 2L | ancho radial mínimo | r*\_max mínimo (desde 2.0) | D dentro de [12, 64] uds-x |
|---|---|---|---|---|---|
| V-a (prescripción 1D) | `6.911504` | `13.823008` | `> 13.823008` | `15.823008` | **NO** — 1.736236× **bajo** el piso |
| V-b | `12.000000` | `24.000000` | `> 24.000000` | `26.000000` | sí (borde inferior) |
| V-c | `48.000000` | `96.000000` | `> 96.000000` | `98.000000` | sí |
| V-d (L sellado del 1D) | `96.000000` | `192.000000` | `> 192.000000` | `194.000000` | **NO** — por encima del techo |

**Medido contra el dominio vigente:** con el default del driver 2D (ancho `12.0`) y $L = 6.911504$, la
diferencia `2L − ancho = 1.823007675795091` ⇒ **el guard C3 dispara con la configuración por defecto**.
El ancho radial del dominio es, por tanto, **la única decisión de dimensionado que este sello deja
ABIERTA** (misma forma que D3 en la pieza F2): se declara la desigualdad que debe satisfacer
(`ancho > 2L`), con sus cuatro números, y **no se elige por decreto**.

---

## Sección C · Veto y ruptura de la ley 1D (−1.3936)

### C.1 Justificación teórica del veto (sellada)

La ley 1D se midió en **incidencia estrictamente normal** ($k_\parallel = 0$), transporte hiperbólico
unidireccional, un solo perfil de familia, un solo `h`, un solo CFL (límites que el acta declara en su
§«LO QUE NO SE MIDE», puntos 1–3). En 2D plano la **dispersión angular** genera $k_\theta \ne 0$ ⇒
incidencia **oblicua**; forzar la impedancia 1D produce **reflexión espuria por desajuste de fase
tangencial**. El propio acta lo dice: las pautas bidimensionales son **PROYECCIONES** de la ley 1D, no
mediciones.

- **La ley 1D NO se hereda.** Usar `−1.3936` como *prior* de dimensionado está **prohibido**.
- `−1.3936` **no se re-deriva** aquí. Se cita verbatim y con su casa:
  `R_t = 9.8807e-02 · D^(−1.3936)` (p=3), residuo relativo máximo `3.021e-02`.
  Medido: la cadena `1.3936` vive en **1** archivo `sim/*.py` (la propia cita de la casa,
  `sim/driver_rw_zerilli_2d.py:91`) y en **6** rutas del repo fuera de `.git` (las tres piezas selladas,
  el `.pyc` y la cita). Cero ocurrencias en ningún crudo: `grep -l 'f11' sim/data/*.json` ⇒ **0**.

### C.2 Criterio de divergencia pre-registrado

Si la **impedancia óptima o tasa de absorción 2D** discrepa de la referencia 1D en más del **3.0 %** ⇒
**DIVERGE** y **prevalece la calibración 2D propia**.

- La tolerancia **no es un número libre**: es el **residuo del propio ajuste 1D**. Se declara el par, no
  se elige: **orden = 3.0 % · medido = 3.021 %** (el acta imprime `3.021e-02`). El sello usa **3.0 %**.

### C.3 Trampa de dominio que este sello declara (medida, no adjudicada)

`−1.3936` es un **interpolante local de potencia sobre `D` en unidades de x**, **no** una ley de
escalado geométrico, y **sólo interpola dentro de `D ∈ [12, 64]` uds-x**; fuera, no. Y en la
configuración del acta $D = L = 6.911503837897546$ uds-x, que queda **1.736236× por debajo del piso**.

> ⇒ En esa configuración **no existe referencia 1D comparable**: el veredicto legítimo es
> **NO COMPARABLE (sin referencia)**, que **no** es lo mismo que **DIVERGE**. Se imprimen los dos
> rótulos y no se funden: un `NO COMPARABLE` leído como `DIVERGE` sería el defecto del juicio, un piso
> arriba del defecto de la cifra.

Y la misma medición deja el precio del test: para tener referencia 1D hace falta
$D \ge 12$ ⇒ `ancho > 24` ⇒ `r*_max ≥ 26` **como mínimo** (columna V-b de la tabla B.3); y en el
extremo caro, $L = 48 \Rightarrow$ `ancho > 96`. La comparación de 3.0 % **no es gratis en dominio**.

### C.4 Segunda incoherencia interna de la casa (declarada, medida)

El acta prescribe **por espesor** (`D = 1.1 λ_min` para −40 dB, `D = 5.7 λ_min` para −60 dB, perfil p=3,
**sin tocar σ_max**); el driver mide que **el pico ES la reflexión** y que **ningún perfil rescata una
capa sub-longitud de onda**: a `L = 12` (≈ 1 longitud de onda) el mejor caso (p=0) da **`−31.01 dB`**.
⇒ Bajo la propia medición 1D de la casa, **−40 dB no es alcanzable por ningún perfil a `D ≈ 1.1 λ`**.
Se declara; no se adjudica. Lo resuelve F11 **midiendo**, no renegociando el umbral.

---

## Sección D · Métrica y umbral sellado

### D.1 Métrica

$$R_{\mathrm{dB}} = 10\log_{10}\!\left(\frac{\mathcal{E}_{\text{reflejada}}}{\mathcal{E}_{\text{incidente}}}\right) \le -40.0\ \mathrm{dB}$$

- `−40.0 dB` es el umbral **ya sellado** de la casa (suite F4 del 1D, `sim/driver_rw_zerilli_1d.py:481`),
  y el mismo del frente 2D (CQG §6). No se estrena umbral en F11.
- $\mathcal{E}_{\text{reflejada}}$ se mide en la **ventana limpia interior**, tras el paso del paquete de
  salida, y se comprueba que **ningún eco de amplitud relativa $\ge 10^{-2}$ regrese al dominio físico
  antes del tiempo de tránsito de ida y vuelta**.

### D.2 Unidades declaradas (coherencia medida, y su trampa)

Las dos cifras del párrafo anterior **son el mismo umbral en dos unidades**:

| escrito | unidad | valor en dB |
|---|---|---|
| eco $\ge 10^{-2}$ | **amplitud** relativa | $10\log_{10}(10^{-2}) = -20.000000000$ dB |
| eco $\ge 10^{-2}$ | **energía** relativa | $10\log_{10}(10^{-2\cdot 2}) = -40.000000000$ dB ≡ umbral sellado |

$$10\log_{10}\!\big((10^{-2})^2\big) = 10\log_{10}(10^{-4}) = -40.0\ \text{dB}$$

**Trampa declarada:** si $R_{\mathrm{dB}}$ se calcula sobre **campos** y el eco se lee en **amplitud** (o
al revés), el umbral **viaja 20 dB** sin que ningún número cambie de forma. ⇒ Todo crudo de F11 debe
imprimir, junto a cada cifra, **la unidad** (energía o amplitud). `R_dB` de este sello es **en energía**.

---

## Sección E · Banco must-fail de metro (controles negativos)

Los tres controles se corren **como gates**, con el crudo de cada uno y **la causa impresa**, no sólo el
`RC` (un caso que devuelve el código esperado por otro motivo no discrimina).

### C1 · Esponja apagada ⇒ la energía vuelve íntegra

- Configuración: $\gamma_{\max} = 0$ **y** borde exterior del dominio **reflejante** (pared física).
- Esperado sellado: $|R_{\mathrm{dB}}| \le 1.0$ dB (la energía incidente retorna al dominio físico).
- **Condición que lo hace discriminante (medida, declarada):** en el 1D, con la esponja OFF
  (`sponge_L, sponge_A = 1.0, 0.0`, forzada en el nulo, l.425) la frontera **Mur-1** sola da
  **`−90.6623 / −90.6620 dB`**. ⇒ Si el control C1 se corriera con Mur-1 activo en el borde, mediría
  **Mur-1, no la esponja**, y su valor esperado dejaría de ser ≈ 0 dB. **Un control cuyo valor esperado
  proviene de otro mecanismo no discrimina.** Por eso C1 exige borde reflejante + $\gamma \equiv 0$.

### C2 · No-contaminación interior

- Esperado sellado: residuo en $t < t_{\text{interfaz}}$ con diferencia de **orden de redondeo**
  ($\le 10^{-13}$) respecto a la solución exacta en espacio infinito.
- Operativa declarada: ventana interior **antes** de que el frente saliente alcance
  $r^*_{\text{sponge}}$. Con $\gamma \equiv 0$ **estructural** en el interior, la diferencia esperada es
  **exactamente 0** dentro del pasado causal; un valor distinto de cero y $\le 10^{-13}$ señala
  redondeo de la aritmética de la capa.
- Respaldo del motor temporal (ya medido, no se re-mide aquí): en F2, `[e_interp] = 6.256075e-07`
  $\ll$ cota `2.139541e-05` ⇒ **el motor temporal no es el que rompe el interior**.
- **Trampa declarada:** si el interior difiere por *cualquier otra* razón (malla, offset, interpolación),
  el $10^{-13}$ mide esa otra razón. Se compara contra la misma corrida **con la capa apagada**, no contra
  una expectativa.

### C3 · Guarda de solape

- Regla: si $L_{\text{sponge}} \ge \frac{1}{2}(r^*_{\max} - r^*_{\min})$, el arnés **aborta con
  `SystemExit`** por sobredimensionamiento de la frontera.
- **Identidad verificada:** es la **misma desigualdad** que la guarda viva del 1D
  (`if 2.0 * sponge_L >= ancho_dominio: raise SystemExit(...)`, l.291) — `L ≥ ½ ancho ⟺ 2L ≥ ancho`.
- En 2D la guarda se evalúa sobre la **extensión radial** (la capa es un anillo); el eje/polo no lleva
  capa. El probe documentado del 1D (dominio $(-40,150)$, $L=96$ ⇒ interfaces `+56.0`/`+54.0`, región
  física vacía) es la ilustración de la violación, no un dominio válido.
- Con la configuración del acta, **este control dispara hoy** (Sección B.3, `2L − ancho = 1.823008`).

---

## Sección F · Tabla de cifras selladas y su comando

UNIVERSO DECLARADO: los dos drivers del sandbox y las tres piezas selladas citadas. Ninguna cifra de esta
tabla se ha producido corriendo una capa.

| # | cifra | valor | comando que la respalda |
|---|---|---|---|
| 1 | λ (ω = 1.0) | `6.283185307179586` | `python3 -B -c "import math;print(2*math.pi/1.0)"` |
| 2 | L = 1.1λ | `6.911503837897546` | ídem, `1.1*2*math.pi` |
| 3 | 2L | `13.823007675795091` | ídem |
| 4 | γ_max n=2 (M1) | `10.851473392629227` | `(n+1)*25/L` con L de (2) |
| 5 | γ_max n=3 (M1) | `14.468631190172301` | ídem |
| 6 | ∫γ realizado (M1) | `25.000000000000000` | `γ_max*L/(n+1)`, los dos n |
| 7 | γ_max (M2, no elegida) | `7.234315595086151` | `2*25/L` (l.299) |
| 8 | ∫γ realizado (M2) | `16.666666666666668` / `12.500000000000000` | `2A/(n+1)`; coincide con el trapecio medido `16.66681` / `12.50022` (D-G) |
| 9 | umbral de reflexión | `−40.0 dB` | `sim/driver_rw_zerilli_1d.py:481` (suite F4) · CQG §6 |
| 10 | frontera 1D sellada | `−47.4885 dB` | `python3 sim/driver_rw_zerilli_1d.py --frontera --json` (acta F4, L=96) |
| 11 | esponja OFF + Mur-1 (1D) | `−90.6623 / −90.6620 dB` | `sim/driver_rw_zerilli_1d.py` (l.71–72 del crudo del diseño) |
| 12 | L=12, mejor perfil (1D) | `−31.01 dB` | `sim/driver_rw_zerilli_1d.py` (D-H, banco 4) |
| 13 | residuo del ajuste 1D | `3.021e-02` | V3 en `sim/PREREGISTRO_FRENTE_2D_CQG_20261013.md` §1 |
| 14 | igualdad amplitud/energía | `−40.000000000 dB` | `10*log10(1e-2**2)` |
| 15 | `1.3936` en `sim/*.py` | `1` archivo (la cita, l.91) | `grep -rl '1\.3936' sim/*.py \| wc -l` |
| 16 | crudos con `f11` | `0` | `grep -l 'f11' sim/data/*.json \| wc -l` |

---

## Sección G · Lo que este sello NO hace

- **No produce resultados.** No hay una sola cifra de reflexión 2D en este documento.
- **No hereda** `−1.3936` ni dimensiona ninguna capa con ella.
- **No elige** el ancho del dominio radial: declara la desigualdad (`ancho > 2L`) con sus cuatro números.
- **No re-mide** F2 (VERDE, commit `f8b788c`), ni F4/F1 del 1D, ni `1.3936`.
- **No toca** `sim/arnes_richardson_2d_f2.py` (v1, otra mano, congelado, ` M` sin commitear).
- **No adjudica** las dos incoherencias internas medidas (B.2/M2 y C.4): se imprimen y se declaran.
- **No eleva** ninguna afirmación: sella reglas.

---

## Sección H · Estado y siguiente paso

- **GATE PRE** = `RC 10` (AUTORIZACIÓN DE CREACIÓN), obtenido `2026-10-13T21:05:53Z` con el TARGET
  **ausente** y `huella_en_target = 0`. Escritura única autorizada: este archivo.
- **PROHIBIDO hasta el cierre del sello:** escribir la capa 2D, correr cualquier malla con
  $\gamma \ne 0$, declarar cualquier `R_dB` de este gate.
- **Siguiente paso autorizable (uno solo):** verificar por conteo que este pre-registro está sellado
  (huella presente, encabezados contados, cero signos de dinero) y obtener del dueño la decisión de
  dimensionado que la Sección B.3 deja abierta (`ancho radial > 2·L_sponge`), **antes** de la primera
  corrida de la capa.

    HUELLA-PREREGISTRO-GATE-2D-F11-20261013
