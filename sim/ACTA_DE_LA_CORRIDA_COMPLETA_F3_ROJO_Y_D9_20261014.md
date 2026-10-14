# ACTA — CORRIDA COMPLETA DEL ARNES F3: VEREDICTO ROJO Y DEFECTO D9
HUELLA: HUELLA-ACTA-DE-LA-CORRIDA-COMPLETA-F3-ROJO-Y-D9-20261014

- **FECHA:** 2026-10-14T00:56:24Z
- **MOTOR:** `python3.14 + numpy` (`python3 -B`, cwd = `sim/`). Cero `scipy`, cero red, cero aleatoriedad, cero estado oculto. La evolucion la hace `sim/arnes_zerilli_curvatura_2d_f3.py`; el acta no integra nada.
- **CASA:** `gw-rw-zerilli`. **PADRE:** `sim/PREREGISTRO_GATE_2D_F3_ZERILLI_CURVATURA_20261013.md` (365 l · 23787 B · sha256 `b19176d9747d6f4ec982b0e38834a1d7a8a95868029c5a439e08fb31bd28149e` · blob `b43403a8b881a05adf24389b3cd9432446677865`). **ERRATA 1:** sellada en el commit `36ab43801f3dc4755282c2746e2bb150449a92c1`.
- **LA ORDEN (verbatim del dueño):** «1. Correr pre-vuelo asegurando RC 10. 2. Escribir `sim/arnes_zerilli_curvatura_2d_f3.py`. 3. Correr post-vuelo asegurando RC 11. 4. Ejecutar el banco de controles estructurales (`--solo-controles C0,C1a,C1b,C9`) antes de lanzar la evolucion temporal completa de C2.»
- **TUPla A2.1 DEL ARNES (verbatim):** TARGET `sim/arnes_zerilli_curvatura_2d_f3.py` · BLOB_PRE `NO_EXISTE_PRE10` · HUELLA `HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261013` · LINEAS_PRE `0` · RC esperado 10.
- **TUPla A2.1 DE ESTA ACTA:** TARGET `sim/ACTA_DE_LA_CORRIDA_COMPLETA_F3_ROJO_Y_D9_20261014.md` · BLOB_PRE `NO_EXISTE_PRE10` · HUELLA `HUELLA-ACTA-DE-LA-CORRIDA-COMPLETA-F3-ROJO-Y-D9-20261014` · LINEAS_PRE `0` · **RC_GATE_PRE = 10** (colision «no existe») medido a `2026-10-14T00:45:41Z`; POST esperado **RC 11**.
- **ESTADO:** el arnes existe, esta certificado (POST RC 11) y **corrio dos veces**. El acto **no repara, no mueve umbrales y no escribe codigo**: el unico archivo que escribe es esta acta.

## UNIVERSO DECLARADO

Este acto mide **cuatro objetos** y los nombra para que no se confundan: (a) el **arnes** `sim/arnes_zerilli_curvatura_2d_f3.py` (el instrumento); (b) el **mapa de tortuga con 2M = 3.0 sobre la malla sellada F11** (el objeto fisico); (c) el **crudo** `sim/data/crudo_2d_f3_*` (que **no existe**, por D9); (d) la **malla sellada** (`r*` en [2.0, 98.0], `nr0 = 384`, `nt0 = 33`, `hr = 0.2506527415143603`) y el **dato de C2** (`sim/arnes_capa_absorbente_2d_f11.py` + `sim/arnes_richardson_2d_f2_v3.py`, ambos intactos). Toda cifra de este acta viaja con su hora; **la unidad de las cifras de conteo es archivo, y la de los residuos es norma L2 relativa**, salvo donde se declare otra.

## §1. Registro de los cuatro pasos ordenados

| paso | que se corrio | hora UTC | RC |
|---|---|---|---|
| 1 | gate PRE del arnes (A2.1) | `2026-10-14T00:18:55Z` | **10** (autoriza crear) |
| 2 | escritura del arnes (3 heredocs deterministas) | `2026-10-14T00:37:35Z` (mtime) | 0 |
| 3 | gate POST del arnes (A2.1) | `2026-10-14T00:38:44Z` | **11** (huella hallada en el destino) |
| 4a | banco `--solo-controles C0,C1a,C1b,C9` + C3 | `2026-10-14T00:38:52Z` | **0** (`RC_GLOBAL_SOLO_CONTROLES = 0`) |
| 4b | humo con `nr0 = 96` (no es medicion) | `2026-10-14T00:39:34Z` | 1 |
| 4c | **evolucion temporal completa de C2 (malla sellada)** | `2026-10-14T00:42:29Z` | **1 — VEREDICTO ROJO** |

Lectura del paso 4a: **los cinco controles analiticos/de identidad y el fail-closed de C3 pasan en la malla sellada** (C0 · C1a · C1b · C9 · C3). Los tres rojos del paso 4c (§3) son de otra clase: dos de umbral de malla (C4, C6) y uno de geometria del dato (C2).

## §2. Salida VERBATIM de la corrida completa (unico registro; NO es un crudo)

El stdout de abajo es **todo** lo que el acto produjo: su ultima fase —la escritura del crudo— **fallo** con `AttributeError` (D9, §4) ⇒ **no hay crudo F3 en `sim/data`** y las cifras que C2 no pudo cerrar (`E_muerta`, `E_entrante`) **no quedaron persistidas en ninguna pieza**. El log vive en `/tmp/f3_run_full.log` (40 l · 3859 B · sha256 `3644ad31b3c4cffcf6d1c9b8a21767dbed3b3385c7a9f24bb89e0f3335d96a05`), que es efimero: por eso se embebe aqui. **No se retipea: se incrusta con `cat`** (la salida de terminal envuelve a ~78 columnas y copiarla a mano fabricaria lineas falsas).

```text
UNIVERSO DECLARADO: malla sellada F11 (r* en [2.0, 98.0], nr0=384, nt0=33, hr=0.2506527415143603) | mapa tortuga con 2M = 3.0 sobre esa malla | dato de C2 | cifras analiticas de V_Z y U
HUELLA = HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261013
hora_utc = 2026-10-14T00:42:29Z
geometria F11 (VERBATIM): L = 24.000000 | c_esponja = 26.000000 | p = 50.000000 | p_eff = 50.1253263707571790 | r*_sponge = 74.000000 | r*_max = 98.000000 | gamma_max = 4.1666666666666670 | integral_gamma = 25.0000000000000000 | solape = 48.000000
2M = 3.000000 | l = 2 | lambda = 2.000000 | U(r*_min) = -3.196335448630e-02 | U(74.0) = -5.927132326515e-05 | U(r*_max) = -2.443425558417e-05 | max |U| = 3.196335448630e-02 en r* = 2.000000
ventanas (c_dato = 10.0): t_1 = 40.125326 | t_a = 52.125326 | t_s = 52.000000 | t_ret = 75.874674 | t_3 = 87.874674 | T_obs = 99.874674
dt = 4.570649962478013500e-02 | nsteps = 2186 | capturas C4 en k = 262 (t = 11.975103) y k = 1137 (t = 51.968290)
D7 CRONOLOGIA DECLARADA (unidades de r* = unidades de t): mitad saliente: anillo 40.125, esponja 64.000, retorno al anillo 75.875 | mitad entrante: pared 8.000, anillo 56.125 (frente 44.125), esponja 80.000, retorno de SU eco al anillo 103.875 (frente 91.875)
[C0] rc=0 ok=True
    U(M=0) = 2.775558e-17 <= 1e-14 : PASA | diff vs F11 (a, l=0, sin esponja, 40 pasos) = 0.000000e+00 | diff vs F11 (b, l=2, con esponja, 1200 pasos) = 1.589813e-15 <= 1e-13 : PASA
[C1a] rc=0 ok=True
    |r*_A - ref| = 4.440892e-16 | |r*_B - ref| = 1.465494e-14 | |r*_A - r*_B| = 1.509903e-14 <= 1e-12 : PASA (ref sellada = 2.851374906561190; cambios de signo del barrido = 1; raices reales del polinomio = 9)
[C1b] rc=0 ok=True
    |r*_rejilla_max - r*_teorico| = 9.941668e-02 <= 0.5 hr = 1.253264e-01 : PASA
[C9] rc=0 ok=True
    max |r*(r(r*)) - r*| = 2.842171e-14 <= 1e-13 : PASA (n = 200001 puntos) | identidad analitica 2M(1+W+lnW) = r*: 1.421085e-14 | nodos de la malla: 1.421085e-14 | punto fijo desnudo en r* = 2.0 tras 60 pasos: r = nan (err nan) => NO contrae, Lambert W0 es obligatoria
[C3] rc=0 ok=True
    C3 FAIL-CLOSED: solape de capa: 2*L = 105.600000000000009 >= ancho = 96.000000000000000 (guarda anti-solape del pre-registro §B.3; no se rebaja el umbral, se corrige L_frac)
[C2] rc=1 ok=False
    R_dB NO MEDIBLE: E_sal = 7.386219e+01, E_vuelta = -9.579974e-02 (la razon no existe)
    residuo no-P2 (DATO inicial / SOLUCION final) = 2.953954e-16 / 9.999999e-01 (informativo: mide el piso del metro angular y, separado, el objeto)
[C4] rc=1 ok=False
    max |u_ON - u_OFF| en r* < r*_sponge = 1.334221e-13 <= 1e-13 : ROJO (pasos [262, 1137])
[C6] rc=1 ok=False aplicable=True
    dispersion theta de U = 0.0e+00 (esperado 0.0) | componente no-P_2 de -U u0 = 1.788218e-10 <= 1e-12 : ROJO | PISO del metro angular (no-P_2 de L2 P_2) = 2.239675e-04 (informativo)
[C7] rc=None ok=None aplicable=False
    D6 DECLARADO: la banda sellada [2.0, 13.8] CONTIENE el dato de C2 (centrado en 10.0, soporte +-6 sigma = [-2.0, 22.0]); el maximo de la banda es el propio dato. Medida contra la banda del dato sale [2.0, -2.0] = VACIA. Control que no puede diferir (familia D5): se reporta la cifra y NO se adjudica.
[C8] rc=None ok=True aplicable=True
    p_eff - r*_min = 48.125326 > 6 sigma = 12.0 : PASA
CONTROLES QUE DECIDEN: C0, C1a, C1b, C2, C3, C4, C6, C9
CONTROLES INFORMATIVOS (no deciden): C7, C8
VEREDICTO = ROJO | rojos = ['C2', 'C4', 'C6']
Traceback (most recent call last):
  File "/Users/marlene/gw-rw-zerilli/sim/arnes_zerilli_curvatura_2d_f3.py", line 1009, in <module>
    sys.exit(main())
             ~~~~^^
  File "/Users/marlene/gw-rw-zerilli/sim/arnes_zerilli_curvatura_2d_f3.py", line 964, in main
    "sigma": float(a.sigma), "nr0": int(m.nr0), "nt0": int(m.nt0),
                                        ^^^^^
AttributeError: 'Malla2D' object has no attribute 'nr0'. Did you mean: 'hr0'?
```

## §3. Adjudicacion por control (causas verbatim en §2)

- **C0 (identidad U = 0 en M = 0) — rc 0, PASA.** `U(M=0) = 2.775558e-17 <= 1e-14`. **Es un cero de maquina del calculo, no un cero exacto**, y asi queda declarado: la resta `V_Z − (1 − 2M/r)·6/r²` con `2M = 0` cancela dos expresiones que valen lo mismo. Y **`V → 0` no se uso como criterio**: el reduce contra el F11 (a: `l=0`, sin esponja, 40 pasos; b: `l=2`, con esponja, 1200 pasos) da `0.000000e+00` y `1.589813e-15 <= 1e-13` ⇒ el operador F3 coincide con F11 cuando el potencial se apaga.
- **C1a (raiz analitica de `dV_Z/dr* = 0`) — rc 0, PASA.** `|r*_A − ref| = 4.440892e-16` · `|r*_B − ref| = 1.465494e-14` · `|r*_A − r*_B| = 1.509903e-14 <= 1e-12`. Ref sellada `2.851374906561190`; un solo cambio de signo en el barrido; nueve raices reales del polinomio.
- **C1b (consistencia de rejilla) — rc 0, PASA.** `|r*_rejilla_max − r*_teorico| = 9.941668e-02 <= 0.5 hr = 1.253264e-01`.
- **C9 (ida y vuelta `r* → r → r*`) — rc 0, PASA.** `max |r*(r(r*)) − r*| = 2.842171e-14 <= 1e-13` sobre `n = 200001` puntos; identidad `2M(1 + W + lnW) = r*`: `1.421085e-14`; nodos de la malla: `1.421085e-14`. **Y la negativa declarada:** el punto fijo desnudo en `r* = 2.0` tras 60 pasos da `r = nan` ⇒ **no contrae ⇒ Lambert W0 es obligatoria en todo el dominio** (§R2/§R3).
- **C3 (anti-solape, fail-closed) — rc 0, PASA.** `2*L = 105.600000000000009 >= ancho = 96.000000000000000`: la guarda del padre §B.3 **no se rebajo**; la prescripcion 1D no se reutilizo para dimensionar la capa.
- **C2 (no reflexion / eco) — rc 1, ROJO: `R_dB NO MEDIBLE`.** `E_sal = 7.386219e+01`, `E_vuelta = -9.579974e-02` ⇒ **la razon no existe** (el metro devuelve `None` cuando `E_vuelta <= 0`, y aqui es negativa). Dos cifras informativas acompanan: el residuo no-P2 del **dato inicial** = `2.953954e-16` (piso del metro angular: el dato ES P2) y el de la **solucion final** = `9.999999e-01` ⇒ a `t = T_obs` el campo **no conserva coherencia l = 2**. Se declara la coincidencia de direccion (ventana de retorno con campo residual, no un pulso que vuelve) y **NO se adjudica la causa**: el crudo que llevaba `E_muerta`/`E_entrante` y las capturas del campo nunca se escribio (D9).
- **C4 (pureza interior, ON vs OFF con el mismo dt) — rc 1, ROJO.** `max |u_ON − u_OFF| en r* < r*_sponge = 1.334221e-13 <= 1e-13` (33 % por encima del umbral heredado de F11), capturas `k = 262` (`t = 11.975103`) y `k = 1137` (`t = 51.968290`).
- **C6 (invariancia angular) — rc 1, ROJO.** `dispersion theta de U = 0.0e+00` (PASA, como se esperaba: el potencial no depende de θ) · **`componente no-P_2 de −U u0 = 1.788218e-10 <= 1e-12` ⇒ ROJO (178×)** · piso informativo del metro angular `= 2.239675e-04`.
- **C7 — `rc = None`, NO APLICABLE (D6 declarado por el arnes).** La banda sellada `[2.0, 13.8]` **contiene el dato de C2** (centrado en 10.0, soporte ±6σ = [−2.0, 22.0]): su maximo es el propio dato y la medida contra la banda sale **vacia**. Es un control que **no puede diferir** ⇒ se reporta la cifra, **no se adjudica**. (Nota de metro: las `filas_testigo` de C4 usan `g["c"] = 26.0` ⇒ `r* <= 14.0`, **48 filas**, no `p_eff`; la cronologia D7 usa `p_eff − 6σ = 38.125326`, **145 filas**. Dos conjuntos testigo distintos en la misma corrida: se declara.)
- **C8 — `rc = None`, informativo.** `p_eff − r*_min = 48.125326 > 6σ = 12.0` : PASA.
- **VEREDICTO: `ROJO | rojos = ['C2', 'C4', 'C6']`.** Deciden C0, C1a, C1b, C2, C3, C4, C6, C9; no deciden C7, C8.

## §4. Defectos declarados (ninguno reparado en este acto)

Numeracion nueva (D8–D12) puesta por esta acta: **nombres y numeros quedan sujetos a la ratificacion del dueño.** Los defectos **D6** (C7 no aplicable) y **D7** (cronologia declarada) **siguen en pie** tal como los declaro el arnes.

- **D9 (bloqueante) — el crudo nace muerto.** `main()` construye el crudo en la **l.964**: `"sigma": float(a.sigma), "nr0": int(m.nr0), "nt0": int(m.nt0),` ⇒ `AttributeError: 'Malla2D' object has no attribute 'nr0'. Did you mean: 'hr0'?` (traceback verbatim en §2). **Inventario medido de `Malla2D`** (`sim/arnes_richardson_2d_f2_v3.py`, `__init__` l.153–179): guarda `nivel` (l.160), `cfl` (161), `hr0` (162), **`nt0` (163)**, `hr` (164), `delta` (166/168), `nr` (169), `rs` (170), `nt` (171), `hth_0` (172), `hth` (173), `th` (174), `dt_cota` (179). **`nt0` existe; `nr0` no.** Reparacion candidata (**NO ejecutada**): `int(m.nr0)` -> `int(a.nr0)` (argparse guarda el `nr0` pedido, 384) y `int(m.nt0)` -> `int(a.nt0)` por fidelidad a la tupla. **Coste medido:** reparar el arnes **invalida la certificacion POST (RC 11)** y **la huella vigente ya habita el destino** (`HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261013`) ⇒ **cualquier tupla que la repita devuelve RC 11 por construccion**; hace falta huella NUEVA + BLOB_PRE + LINEAS_PRE con RC esperado 0.
- **D8 — la cifra que falta.** C2 quedo «NO MEDIBLE» y el crudo no se escribio ⇒ **`E_muerta` y `E_entrante`, que el metro si acumula, no quedaron persistidos**. La pregunta de F3 —**cuanto refleja la curvatura**— sigue sin responder, y esa es la salida del acto, no un accidente de forma. **Declarado, no rellenado**: no se reconstruye un objeto certificado desde cifras de pantalla.
- **D10 (medido en §5) — el operador no tiene pico interior.** En la malla sellada y con `2M = 3.0`, `U` es **estrictamente creciente** en los 383 intervalos (`383` subidas · `0` bajadas): el maximo del valor absoluto esta **en la pared interior** (`max |U| = 3.196335448630e-02` en `r* = 2.0`). El «pico» que el padre buscaba **no esta en el dominio medido**. No se cambia la masa para fabricarlo (§R3 fija `2M = 3.0`).
- **D11 (medido en §5) — C1a/C1b certifican el pico de `V_Z`, no el de `U`.** Ambos anclan en `r*_pico = 2.851374906561190`, que es el maximo de `V_Z`; el termino metrico-angular `(1 − 2M/r)·6/r²` **crece hacia adentro** y alli es ~1.5 veces mas grande que `V_Z` (§5.3) ⇒ **el objeto que se evoluciona no tiene el pico que `C1` certifica**. El control es correcto y su objeto es otro.
- **D12 (medido en §5.4) — filas testigo dentro del cuerpo del dato.** Las 48 filas `r* <= 14.0` (rs 2.000000 … 13.780679) estan **dentro del soporte inicial del dato** (±3σ = [4.0, 16.0]) y su expectativa no es cero por construccion. **C4 rojo por 33 % no se adjudica como fuga**: ver el dominio medido de sus umbrales, abajo.
- **Dominio de dos umbrales (declarado, no reparado; el umbral no se baja).** Sonda de escala **NO certificada** (dos rungs de `nr0`, no un barrido): C4 `2.813821e-09` (`hr = 1.0105263157894737`) -> `1.334221e-13` (`hr = 0.2506527415143603`) y C6 `2.014891e-07` -> `1.788218e-10`. Firma de cantidad de discretizacion, no de fuga fisica. Contraste medido: **F11 certifico con el MISMO metro** (`ON vs OFF`) `8.11e-72` y `2.377e-14` en `sim/data/crudo_capa_absorbente_2d_f11_20261013T221500Z.json` (C2, l.39–54), sobre la misma malla. **Colision de nombres medida:** el metro «no contaminacion interior (ON vs OFF, mismo dt)» se llama **C2** en F11 (`UMBRAL_C2 = 1e-13`) y **C4** en el padre F3 (`UMBRAL_C4 = 1e-13`, criterio «residuo interior <= umbral F11»): **mismo metro, mismo umbral, dos nombres**; el **C4 de F11** es **otro metro** (`ratio = E_entrante/E_sal <= 1e-3`). Y **`UMBRAL_C6 = 1e-12` lo puse yo**: el padre §D no da criterio numerico para C6, y el umbral quedo **~178× por debajo** de lo que el metro mide (1.788218e-10) y **~7 ordenes por debajo** de su piso informativo declarado (2.239675e-04). **Se declara el defecto de dominio; no se mueve el umbral despues de ver la cifra.**

## §5. Mediciones de este acto (segundo metro, de solo lectura)

Todas las cifras de §5 salen de las **funciones selladas del propio arnes** (`r_de_rs` · `vz_de_r` · `u_de_r` · `campos_de_malla` · `lambert_w0`) mas `f11.geometria` y `f2.Malla2D` — **no de una segunda implementacion**, que seria un metro distinto midiendo el mismo objeto. **Cero escrituras sobre el arnes y cero umbrales.** Comando: `python3 -B -` con `sys.path` a `sim/`, desde el repo. Log completo verbatim (23 l · 2800 B · sha256 `00242272a24d3904bfe10e971f48e8754c05d7a3353da65caf0a724406cc3783`):

```text
UNIVERSO DECLARADO: malla sellada F11 (r* en [2.0, 98.0], nr0 = 384, nt0 = 33, hr = 0.2506527415143603) sobre 2M = 3.0 . l = 2 . lambda = 2; medidas ANALITICAS de V_Z, f*6/r^2 y U(r*), y geometria del metro, con el mismo metro del arnes (import de los tres sellados)
MOTOR: python3 + numpy, sin scipy, sin red, sin aleatoriedad; CERO pasos de integracion temporal
HORA_UTC = 2026-10-14T00:48:05Z
geometria: g[c] (esponja) = 26.0 | g[p] = 50.0 | g[rs_min] = 2.0 | g[rs_max] = 98.0
malla: nr = 384 | nt = 33 | hr = 0.2506527415143603 | nivel = 0
anillo del medidor: ip = 192 | rs[ip] = 50.1253263707571790 | p_eff = 50.1253263707571790
filas_testigo del medidor (rs <= g[c] - 6 sigma = 14.000000): n = 48 | rs de 2.000000 a 13.780679
filas que usaria la cronologia D7 (rs <= p_eff - 6 sigma = 38.125326): n = 145
U en la malla (2M = 3.0): U[0] = -3.196335448630e-02 | U[-1] = -2.443425558417e-05 | max|U| = 3.196335448630e-02 en rs = 2.000000
dU/drs sobre los 383 intervalos: subidas = 383 | bajadas = 0 | iguales = 0 | min = 7.878341e-07 | max = 2.946051e-03
U en el nodo del flujo (anillo): rs = 50.125326370757 | U = -2.004103703582e-04
r* = 2.000    r = 4.364178849508 | f = 0.312585459155 | V_Z = 6.650914047302e-02 | f*6/r^2 = 9.847249495931e-02 | U = -3.196335448630e-02
r* = 4.000    r = 5.087678629994 | f = 0.410340114190 | V_Z = 6.605059787374e-02 | f*6/r^2 = 9.511650498130e-02 | U = -2.906590710756e-02
r* = 6.000    r = 6.000000000000 | f = 0.500000000000 | V_Z = 5.974517906336e-02 | f*6/r^2 = 8.333333333333e-02 | U = -2.358815426997e-02
r* = 8.000    r = 7.078585877183 | f = 0.576186536117 | V_Z = 5.110445861087e-02 | f*6/r^2 = 6.899559204377e-02 | U = -1.789113343290e-02
r* = 10.000   r = 8.295349767075 | f = 0.638351596468 | V_Z = 4.251200481855e-02 | f*6/r^2 = 5.565981959459e-02 | U = -1.314781477603e-02
r* = 12.000   r = 9.623820094708 | f = 0.688273474517 | V_Z = 3.500670808420e-02 | f*6/r^2 = 4.458792801237e-02 | U = -9.581219928168e-03
r* = 14.000   r = 11.041856844137 | f = 0.728306566337 | V_Z = 2.882519950147e-02 | f*6/r^2 = 3.584109349734e-02 | U = -7.015893995870e-03
r* = 20.000   r = 15.676570519911 | f = 0.808631613899 | V_Z = 1.675944498249e-02 | f*6/r^2 = 1.974239540540e-02 | U = -2.982950422908e-03
r* = 38.125   r = 31.383421221305 | f = 0.904408127500 | V_Z = 5.043152943698e-03 | f*6/r^2 = 5.509537395702e-03 | U = -4.663844520045e-04
r* = 50.125   r = 42.399572005670 | f = 0.929244568799 | V_Z = 2.900989520374e-03 | f*6/r^2 = 3.101403955105e-03 | U = -2.004144347311e-04
r* = 74.000   r = 64.918385405650 | f = 0.953788129799 | V_Z = 1.298786246499e-03 | f*6/r^2 = 1.357899860810e-03 | U = -5.911361431139e-05
r* = 98.000   r = 87.968978184002 | f = 0.965897068922 | V_Z = 7.244643186580e-04 | f*6/r^2 = 7.488985742422e-04 | U = -2.443425558417e-05
```

**§5.1 (D11).** En la pared interior el termino metrico-angular **domina** a `V_Z`: `r* = 2.0` -> `V_Z = 6.650914047302e-02` vs `f·6/r² = 9.847249495931e-02` (razon 1.48); `r* = 98.0` -> `7.244643186580e-04` vs `7.488985742422e-04` (razon 1.03). `U = V_Z − f·6/r²` es **negativo en todo el rango** (`-3.196335448630e-02` … `-2.443425558417e-05`, monotona estricta, 383 subidas) ⇒ **§R2 no es un matiz: cambia la clase del operador** (pozo atractivo puro, sin barrera en [2, 98]).

**§5.2 (por que no es un cero de maquina).** El cero de `C0` (`2.775558e-17`) es el de la resta en `M = 0`; con `2M = 3.0` el termino metrico-angular **vale mas** que el potencial (`r* = 2.0`: `0.098472` vs `0.066509`) ⇒ la magnitud `|U| = 3.196335448630e-02` esta **14 ordenes** por encima de ese cero. La cancelacion **no es catastrofica**: `V_Z − f·6/r²` con `|U| ~ 0.032` a partir de terminos de `O(0.1)` ⇒ factor ~3.

**§5.3 (D10, ley de escala).** `|U|` decrece monotona de `3.196335448630e-02` (`r* = 2.0`) a `2.443425558417e-05` (`r* = 98.0`); `dU/dr*` positiva en los **383** intervalos (`min = 7.878341e-07`, `max = 2.946051e-03`, `bajadas = 0`, `iguales = 0`) ⇒ **no hay maximo local interior**. El maximo de `V_Z` en la rejilla vive en `r* = 2.851` (`r = 4.648186`), donde `f·6/r² = 0.0577 > V_Z = 0.0597`; ahi `U = -4.23e-03`, **dentro del valle**. El punto fijo desnudo no contrae en el borde (`r = nan` tras 60 pasos, §3-C9) y `Lambert W0` es la identidad obligatoria en **todo** el dominio.

**§5.4 (D12).** Del conjunto declarado por D7 (145 filas `r* <= 38.125326`), `p_eff` cae **dentro** y deja **118 filas** (`r* ∈ (38.125326, 74.0]`) entre el dato y la esponja; el medidor solo lee las **48** filas `r* <= 14.0`. Ambas elecciones se declaran: **no se re-ancla el conjunto testigo en este acto.**

**§5.5 (identidad de malla).** `nr = 384` · `nt = 33` · `hr = 0.2506527415143603` · `dt = 4.570649962478013500e-02` · `nsteps = 2186` · `ip = 192` · `p_eff = 50.1253263707571790` ⇒ el `dt` de este acto **es** el de la corrida ROJA (el paso temporal no esta en disputa).

## §6. Identidades (hora UTC · tamano · sha256 · blob git)

| pieza | lineas | bytes | sha256 | blob git | git |
|---|---|---|---|---|---|
| `sim/arnes_zerilli_curvatura_2d_f3.py` (mtime `2026-10-14T00:37:35Z`) | 1009 | 45883 | `b40c673a86ebc796841569d43a5b5773a9fd17648b834a48b30437d3b0e7987e` | `fa536467da94830360445ebaf54292166b70d95a` | `??` sin versionar |
| log de la corrida `/tmp/f3_run_full.log` | 40 | 3859 | `3644ad31b3c4cffcf6d1c9b8a21767dbed3b3385c7a9f24bb89e0f3335d96a05` | — | `/tmp` (efimero; embebido en §2) |
| log de la medicion `/tmp/f3_medida_u_20261014.txt` | 23 | 2800 | `00242272a24d3904bfe10e971f48e8754c05d7a3353da65caf0a724406cc3783` | — | `/tmp` (efimero; embebido en §5) |
| `sim/ERRATA_1_PREREGISTRO_GATE_2D_F3_20261013.md` | 94 | 8644 | `b23a17128c99ef78fcc0219d61fa6858f9f464f8e1fe2c02beee3560aebd1d95` | `84c6f582cbc2027d8b7a9aad4c63f27f09799ca` | sellada en `36ab438` |
| `sim/PREREGISTRO_GATE_2D_F3_ZERILLI_CURVATURA_20261013.md` | 365 | 23787 | `b19176d9747d6f4ec982b0e38834a1d7a8a95868029c5a439e08fb31bd28149e` | `b43403a8b881a05adf24389b3cd9432446677865` | `??` (append-only, intacto) |
| `sim/arnes_richardson_2d_f2_v3.py` (intacto) | 800 | — | `2efba187cbb6a03842c76ffa52190df127324bb736571eb5993647c6ffc65529` | `72844790ba3ef2184d941ed1202c84b88771276b` | sin cambios |
| `sim/arnes_capa_absorbente_2d_f11.py` (intacto) | 703 | 32310 | — | `5977cce60c2616e3d196707e3ccef29ce8bff710` | sellado en `f974578` |
| `sim/arnes_richardson_2d_f2.py` (**congelado por orden del dueño**) | 576 | — | — | disco `48b5859e337984e2…` vs HEAD `73c6cceb0209ddb2…` | ` M` (no se toca) |

- **`sim/data` NO tiene crudo F3.** Medido dos veces por vias distintas (listado del directorio y `git status --porcelain -uall -- sim/data`); el mas reciente sigue siendo `crudo_capa_absorbente_2d_f11_20261013T221500Z.json` (270 l · 6677 B · sha256 `6300fe4e831b072b439df4c289de910e945859f36a65785a16c8a8a80b444438` · blob `c52de2abdba1feea49bedfae726c9fbcde3b53fe` · `veredicto VERDE` · `R_dB -45.931354463740675`).
- **HEAD `36ab43801f3dc4755282c2746e2bb150449a92c1`** (padre `b01076890c07040e53184cb2f380b7adcc52fafc`). **`huella_dueno_en_crudo = 0`** (nada del dueño viaja en la corrida; se declara, no se adjudica).
- ~23 entradas `??` de **otras manos** siguen intactas en el arbol.

## §7. Peticion al dueño (lo que NO adjudico yo)

1. **Tupla A2.1 de reparacion de D9** (propuesta, pendiente de su autorizacion; **huella nueva**, porque la vigente ya habita el destino y daria RC 11 por construccion): TARGET `sim/arnes_zerilli_curvatura_2d_f3.py` · BLOB_PRE `fa536467da94830360445ebaf54292166b70d95a` · HUELLA `HUELLA-ARNES-ZERILLI-CURVATURA-2D-F3-20261013-R2` · LINEAS_PRE `1009` · **RC esperado 0**.
2. Tras la reparacion, **volver a correr la evolucion completa** (no solo el banco) para que el crudo nazca, y **re-certificar con la huella nueva** (POST).
3. **¿Se rediseña C2?** Con el dato de §R5 (gaussiana pura en `r* = 10.0`, `v0 = 0`), la mitad que viaja al anillo tiene su **retorno declarado a `103.875 > T_obs = 99.874674`** (§D7) ⇒ la ventana `[52.125326, 75.874674]` **no contiene retorno declarado** y el ratio no existe. El defecto es de la **geometria del dato**, no del integrador.
4. **D10/D11:** el «pico» que el padre buscaba **no esta en el dominio medido** y **C1 certifica el de `V_Z`, no el de `U`**. ¿Se re-ancla C1 al operador que se evoluciona, o se acepta que el pico no es el objeto?
5. **D12 y el dominio de `UMBRAL_C4`/`UMBRAL_C6`:** ¿se re-ancla el conjunto testigo del medidor y se fija el dominio de los dos umbrales (hoy uno heredado de F11, el otro inventado por mi)?
6. **D6 y D7 siguen en pie**; no los toco.

## §8. Alcance

Cero reparaciones · cero escrituras sobre el arnes · cero umbrales movidos · cero commits · cero `git add`. El **unico** archivo que este acto escribe es **este acta** (gate PRE RC 10 a `2026-10-14T00:45:41Z`; POST esperado RC 11). `sim/data` sin crudo F3 · `sim/PREREGISTRO_GATE_2D_F3_…md` y `sim/ERRATA_1_…md` intactos · `sim/arnes_richardson_2d_f2.py` sigue ` M` · los `??` de otras manos intactos. Toda cifra citada viaja con su hora; **el acta es registro, no medida: si una cifra de aqui se cita fuera, se cita con la hora y el comando que la respalda** (§2, §5). Fuera de alcance y **no medido** en este acto: `platino-labs` sin arbol git (RC 14, segun memoria de repositorio) y los pendientes de `core/`. `python3 -B` en toda invocacion; cero `scipy`; cero red; cero aleatoriedad.
