# PRE-REGISTRO SELLADO DEL FRENTE 2D (t, r*, theta) Y FONDOS CURVOS — 2026-10-13

HUELLA: HUELLA-PREREGISTRO-FRENTE-2D-CQG-TEUKOLSKY-20261013

T_UTC_VENTANA: 2026-10-13T18:52:00Z (reloj UTC del turno de sellado; se re-sella al primer numero).

UNIVERSO DECLARADO: este documento (1 pieza) + el arbol git /Users/marlene/gw-rw-zerilli (satelite independiente, SIN submodulos, SIN dependencia de sfqed-paper) + la triada verificada del 1D citada en la seccion 1. MOTOR = ninguno: documento de sellado; las cifras se fijan por contrato, no por corrida. UNIDAD = linea / encabezado / umbral adimensional. VENTANA = reloj UTC de la cabecera. `.git` NO entra en el universo.

## Seccion 0 · Contrato de destino (A2.1)

- UBICACION REPO: /Users/marlene/gw-rw-zerilli
- TARGET: /Users/marlene/gw-rw-zerilli/sim/PREREGISTRO_FRENTE_2D_CQG_20261013.md
- BLOB_PRE: AUSENTE
- LINEAS_PRE: 0
- HUELLA: la fila unica de la cabecera (HUELLA-PREREGISTRO-FRENTE-2D-CQG-TEUKOLSKY-20261013).
- GATE PRE: `bash tools/gate_pre_escritura.sh <TARGET> AUSENTE HUELLA-PREREGISTRO-FRENTE-2D-CQG-TEUKOLSKY-20261013 0` corriendo desde /Users/marlene/platino-labs (alli vive el arnes) → RC 10 (destino nuevo sin colision) → ESCRIBIR → gate POST → RC 11 (la huella ya habita el destino).
- Condicion de contencion: el gate esta acotado AL TARGET (`git status --porcelain -- TARGET`), no al arbol entero. Los cuatro objetos sin rastrear del sandbox (`?? sim/reflexion_frontera_1d.py`, `?? sim/reflexion_escala_D.py`, `?? sim/__pycache__/*`, `?? .DS_Store`) NO bloquean esta escritura, y esta escritura NO los adjudica.
- PROHIBIDO hasta sellar ESTE pre-registro: escribir cualquier driver 2D, correr cualquier malla 2D, extraer cualquier sobretono.

## Seccion 1 · Estado de partida verificado (con su comando)

Las tres cifras de la orden del dueno fueron medidas; las tres tienen comando que las respalda.

| # | cifra de la orden | valor medido | casa (archivo) | comando |
|---|---|---|---|---|
| V1 | frontera F4 pasando holgada a −47.49 dB | **−47.4885 dB** en energia (umbral sellado −40.0 dB; margen 7.49 dB) | `sim/ACTA_CIERRE_FRONTERA_V3_20261013.md` (commits `4f91b88`, `50a1b29`) | `python3 sim/driver_rw_zerilli_1d.py --frontera --json` |
| V2 | el extractor recupera modos a 1.42e-3 | **1.4185e-03** relativo (MPM, K=3, contra Leaver l=2, n=0) | `sim/ACTA_EXTRACTOR_ESPECTRAL_CALIBRACION_20261013.md` (sha16 `33c0768870dc7c42`; commit `6d73a15`) + apendice blob `6bf81d84` (commit `4206b50`) | `python3 sim/extractor_polos_matrixpencil.py --json` |
| V3 | la ley de potencias R_t proporcional a D a la −1.39 | **R_t = 9.8807e-02 · D^(−1.3936)** (p=3), residuo relativo maximo **3.021e-02** | `ACTA_REFLEXION_FRONTERA_SOMMERFELD_VS_PML_20261013.md` errata **E-h** + `ADENDA_1_..._20261013.md` **AD-3.1** | `python3 sim/reflexion_escala_D.py` + ajuste EXP vs POT sobre las 24 filas unicas |

- F1..F7 certificados en V3: F1 PASA (`cfl_certificante = 1.0`), F2 OK (`p = 2.0002`), F3 OK (`d1 = 1.9249e-03 / 2.0058e-03`), F4 VERDE (−47.4885 dB), F5 PASA (`desv_rel = 0.004276`), F6 medido (0 nodos compartidos en 3 pares), F7 PASA (`desv_rel Leaver = 0.033637`).
- El apendice del extractor (`APENDICE_CORRECCIONES_ACTA_EXTRACTOR_20261013.md`) declara que el literal `1.418505` da **cero ocurrencias** en el acta; la cifra del acta se lee como **DERIVADA** (K=3 → `1.4185e-03`), no como transcripcion verbatim.

## Seccion 2 · Alcance y exclusiones de este frente

- Dentro: metrica estacionaria, axisimetrica (derivada parcial respecto de phi identicamente nula); coordenadas (t, r*, theta); campo escalar o de Teukolsky segun el fondo; fronteras absorbentes en r* (los dos extremos) y regularidad en los polos theta = 0, pi.
- Fuera (AJENO): la deteccion por LIGO/Virgo sobre el IMF no lineal 3+1; nada de eso se reclama aqui.
- Fuera (trabajo futuro declarado): el fondo de Kerr rotante exige armomicos esferoidales y acoplamiento de l; entra SOLO si el frente lo abre su propia seccion de umbrales.

## Seccion 3 · LA LEY DEL 1D NO SE TRANSFIERE AL 2D (defecto declarado, no adjudicado)

La orden pide dimensionar capas absorbentes bidimensionales con la ley V3. El acta que mide esa ley declara sus propios limites (§ «LO QUE NO SE MIDE», puntos 2, 3, 4 y 5):

1. **Una sola resolucion** (`h = 0.05`, CFL = 0.50): «la ley en celdas NO se transfiere a otra resolucion sin re-medir».
2. **Un solo perfil de familia** (sigma_max · xi^p, p = 1..4) y un solo CFL.
3. **Incidencia normal 1D escalar: nada de 2D/3D, esquinas, incidencia oblicua ni anisotropia.** Las pautas bidimensionales son PROYECCIONES de la ley 1D, no mediciones.
4. **Piso del medidor** `R_max_banda = 1.170e-10 = −198.64 dB`: ninguna cifra por debajo de eso es distinguible de cero con este dispositivo.

Consecuencia operativa (la que cambia el plan):

- `R_t proporcional a D^(−1.3936)` es un **interpolante local de potencia** sobre `D` en **unidades de x** (1 ud = 20 celdas a `h=0.05`), medidor `R_t`, borde `dirichlet`, `smax_frac = 0.55`, fondo 1D, incidencia normal. **NO es una ley de escalado geometrico.**
- El ajuste exponencial alternativo tenia residuo 20–25 por ciento y el acta ordena **no usar** sus 295 uds como prediccion (errata E-h); la potencia (residuo 1.3–3.6 por ciento) situa el objetivo hipotetico de 1e-8 en `D = 1.05e5 uds = 2.09e6 celdas = 436 × Lx` ⇒ **el objetivo no es alcanzable en este dominio**. Dentro de `D` en [12, 64] uds la ley **interpola**; fuera, no.
- La **prescripcion de dimensionado del propio acta NO es la potencia**: es `D = 1.1 λ_min` para −40 dB y `D = 5.7 λ_min` para −60 dB, con perfil p=3 y **sin tocar sigma_max**. Y para el sandbox el acta cierra con una via mas barata: **quitar la esponja y dejar Mur-1** (ganancia medida de ~100 dB en energia; F4 pasa holgado sin capa).
- ⇒ Cualquier capa 2D de este frente **re-mide** su ley (gate F11 abajo). Usar −1.3936 como *prior* para dimensionar 2D es exactamente la proyeccion que el acta prohibe: **no se hereda, se re-mide**.

## Seccion 4 · Esquema 2D y por que el 2D es necesario (declaracion de encuadre)

- Para **Schwarzschild** con axisimetria, los armonicos esfericos separan: cada par (l, m) obedece su propia ecuacion 1D. El 2D **no anade fisica**; sirve de **verificacion de instrumento** (el 2D debe reproducir el 1D). Es el gate F8.
- El 2D **si anade fisica** cuando hay **mezcla de l** (fondo de Kerr / ecuacion de Teukolsky) o cuando la fuente no es axisimetrica; y anade **geometria** en las fronteras (esquinas, incidencia oblicua) — justo el dominio que la ley 1D NO cubre (seccion 3.3).
- Descomposicion modal declarada: el campo se proyecta en la base esferica Y_lm(theta, phi); se registra la **energia por modo** en cada instante de extraccion. La pureza modal es un gate (F10), no un supuesto.
- Integrador: leapfrog escalonado heredado del 1D (mismo esquema, misma direccion de radiacion declarada: saliente en el infinito espacial, ENTRANTE en el horizonte). CFL sellado: Δt/Δr* = 0.50 en la malla gruesa, con la cota `Δt/Δr* < 1/sqrt(1 + V_max·Δr*^2/4 + L_theta)` donde `L_theta` es el termino angular de la malla en theta; la cota efectiva se **mide** (F9), no se supone.
- Tres mallas **no anidadas** tambien en 2D: Δk = Δ0 / 2^k con offset δk = k·Δk/3 en ambas direcciones, de modo que ningun nodo se comparte entre niveles.

## Seccion 5 · Nulos y controles (desacoplados)

- N-2D-0 (INSTRUMENTO, reduccion al 1D): con V identicamente 0 y sin dependencia en theta, el solver 2D debe coincidir con el 1D en el dominio interior. Es el mismo nulo de d'Alembert del banco 1D trasladado de dimension.
- N-2D-1 (ORDEN): Richardson sobre tres mallas no anidadas, con la MISMA malla fisica de extraccion (interpolacion declarada). Piso de redondeo: si la primera diferencia cae por debajo de 100·eps·max|A|, el orden NO ES MEDIBLE y se declara; no se pinta verde.
- CONTROL INTERNO: la pureza modal (F10) certifica que el sesgo angular es de la discretizacion y no de la fisica.
- CONTROL EXTERNO (referencia citada, no autogenerada): modos cuasinormales de Leaver, `M·omega = 0.37367 − 0.08896 i` para l = 2, n = 0; y el primer sobretono n = 1. Su acuerdo se usa como **discrepancia declarada**, no como prueba de la fisica.

## Seccion 6 · Criterios de corte de fallo (sellados ANTES de la primera linea de codigo 2D)

| # | medida | umbral sellado | accion |
|---|---|---|---|
| F8 | error relativo L2 del nulo de reduccion 2D→1D (N-2D-0) | mayor que 1e-12 | FALLO de instrumento (abortar) |
| F9 | orden observado 2D sobre 3 mallas no anidadas (N-2D-1) | valor absoluto de (p − 2) mayor que 0.15 | FALLO: segundo orden refutado |
| F10 | fuga modal con inyeccion de un solo modo (l=2, m=0) a l' distinto de l | mayor que −60 dB relativo | FALLO: la malla en theta no es espectral; el 2D no se atribuye a la fisica |
| F11 | ley de la capa absorbente 2D **re-medida** (no heredada del 1D) | si el exponente 2D difiere del 1D (−1.3936) en mas del residuo del ajuste (3.0 por ciento) | DIVERGE: manda la ley 2D; **prohibido dimensionar con la ley 1D** |
| F12 | sobretono n = 1 extraido por MPM en 2D contra Leaver | desviacion relativa mayor que 5e-2 | DIVERGENCIA declarada (control externo) |
| F13 | sesgo parametrico a bajo SNR sobre M = 200 realizaciones con ruido declarado | valor absoluto del sesgo mayor que 2 veces el error estandar del estimador | FALLO: sesgo parametrico; el titular del paper no se sostiene |
| F14 | regularidad en los polos theta = 0, pi | crecimiento no acotado de la energia cerca del polo | FALLO de frontera (contamina la extraccion) |

## Seccion 7 · Entregable declarado

- **Titular del paper:** extraccion de modos cuasinormales en regimenes de bajo SNR **sin sesgo parametrico**.
- **Revista objetivo (declarada, no negociable en la medicion):** Classical and Quantum Gravity (CQG) o Physical Review D (PRD).
- **Condicion de redaccion:** el paper NO se empieza hasta que F8..F14 tengan crudo registrado. La cifra −1.3936 **no aparece** en el paper como ley 2D: aparece, si acaso, como ley 1D con su dominio declarado (seccion 3).

## Seccion 8 · Procedencia y no-elevacion

- Las tres cifras V1..V3 son MEDIDAS en el sandbox 1D; se citan con su casa y su comando. No se re-miden aqui.
- La isospectralidad de Darboux es un hecho analitico conocido; se usa como control, no como hallazgo.
- Los modos de Leaver son valores de referencia de la literatura; no se autogeneran.
- Las decisiones de encuadre de la seccion 4 (descomposicion modal, CFL con termino angular, rango de simetria) son **propias de este sello y NO estan ratificadas por el dueno**. Se declaran, no se adjudican: quedan **PENDIENTES DE RATIFICACION** antes de escribir el driver.
- Ninguna afirmacion se eleva con menos de dos casos. Este pre-registro sella reglas; no produce resultados.

## Seccion 9 · Estado y siguiente paso

- Orden de fases A2.1: gate PRE = RC 10 (este acto), ESCRIBIR (este acto), gate POST = RC 11 (la huella ya habita el destino) + conteo de encabezados y verificacion de signo de dinero = 0.
- PROHIBIDO hasta sellar: escribir el driver 2D, correr cualquier malla 2D, extraer cualquier sobretono.
- Siguiente paso autorizable (uno solo): tras verificar por conteo que ESTE pre-registro esta sellado, y tras la ratificacion del dueno sobre la seccion 4, crear el driver 2D **con la ley de la capa de su propia fuente** (gate F11), nunca con −1.3936 heredado.
