# ACTA — EXTRACTOR ESPECTRAL (PRONY / MATRIX PENCIL): CALIBRACIÓN, BARRIDOS Y MARGEN DEL SISTEMA

`HUELLA-ACTA-EXTRACTOR-ESPECTRAL-CALIBRACION-20261013`

- **Contrato A2.1.** El destino de esta acta **no existía** al abrirla: el gate de pre-vuelo se corrió
  como primera acción y devolvió **RC 10** (`COLISION: … no existe`, medido `2026-10-13T11:09:52Z`) ⇒ el
  acto ordenado es **crearla**, no mutarla. El instrumento intervenido (`sim/extractor_polos_matrixpencil.py`)
  sí viajó con tupla completa y **RC 0** a `11:01:42Z` (ver §1).
- **UNIVERSOS DECLARADOS.** (a) El instrumento `sim/extractor_polos_matrixpencil.py` (**1 pieza**) · (b) el
  driver `sim/driver_rw_zerilli_1d.py` (**1 pieza, SOLO LECTURA, jamás modificado**) · (c) los crudos que
  este ciclo escribió en `sim/data/` (**5 archivos**, §11). Unidad declarada: **línea · polo · valor singular ·
  muestra · decibelio**. Ventana declarada: reloj UTC.
- **MOTOR.** Python 3.14.7 · numpy 2.4.6 · scipy 1.17.1 · macOS/zsh.
- **Regla de lectura.** Ninguna cifra de esta acta se publica sin su **hora, su comando y su unidad**; toda
  celda no medida viaja como `null`, **nunca** como `0`.

---

## §1. IDENTIDAD DEL INSTRUMENTO (sellada) Y LAS SEIS REPARACIONES

Identidad medida a `2026-10-13T11:03:46Z` (`shasum -a 256` + `git hash-object` + `wc -l -c` + `grep -c`):

| campo | valor |
|---|---|
| archivo | `sim/extractor_polos_matrixpencil.py` |
| líneas · bytes | **935** · **39 590** |
| sha256_16 | `bd02127657d69bb0` |
| git blob | `4fb04ab780acf4f7eedcf0ea8c5c5757fe696d47` |
| commit de custodia | `75e5e27` (limpio contra HEAD) |
| huella (3 ocurrencias) | `HUELLA-EXTRACTOR-ESPECTRAL-PRONY-MATRIXPENCIL-20261013` |
| signos monetarios | **0** |

Encabezados: `^#+ ` = **26** · `^# ` = **26** · `^##` = **0** · `^### ` = **0** ⇒ los 26 son **bandas de
código**, no encabezados markdown (el contador se imprime **con su nivel declarado**, D22/D17).

**Las seis reparaciones** aplicadas en un solo acto (`multi_replace_string_in_file`) y validadas con
`get_errors` limpio + re-corrida:

1. **`mpm()` — emparejamiento por exclusión de índice.** `dist = np.abs(z - np.conj(zi))` · `dist[i] = inf` ·
   `j = argmin(dist)` · `if not np.isfinite(dist[j]): continue` ⇒ claves `residuo_conjugado_evaluado`,
   `residuo_conjugado_pares`.
2. **`mpm()` — docstring**: sobre `Z` real los pares conjugados nacen **bit-exactos** ⇒ F5 es **inerte por
   construcción** (declarado, §9).
3. **`extraer()`** — amplitudes vía `amplitudes(y, reps)` con **base real** `[Re(z^m), Im(z^m)]`; diagnóstico
   `residuo_reconstruccion_abs/_rel` (diagnóstico, **no** corte).
4. **`cortes()`** — `conj_eval`/`conj_val` + clave nueva **`F5_evaluado`**; **F2 = `sin_ruido and rank_rel !=
   rango_declarado`** (conformación al sello: el sello dice «sin ruido»).
5. **`correr_caso()`** — bloque de discrepancia MPM↔Prony con listas explícitas + clave `orientacion`.
6. **`cabecera()`** — `defectos_del_metro_declarados`.

**Pre-registro** `sim/PREREGISTRO_EXTRACTOR_ESPECTRAL_20261013.md`: **157 l · 12 113 B · sha16
`3a707f6cade6d6bc` · blob `ecd55fef00a79ca3d5e239e232c680791f8f6edb`** · `^#+`=13 · `^##`=12 · `^#`=1 ·
huella 1× (l.3) · **append-only desde el sellado, jamás editado** (commit `0feb32a`).

---

## §2. CRITERIO DE ÉXITO (3): PRECISIÓN DE MÁQUINA SIN RUIDO

Corrida `pase2`, crudo `sim/data/crudo_extractor_pase2_20261013T110322Z.json` (N=121, dt=0.5, T=60.0). El
corte sellado **C1** = «limpio ≤ 1e-14 = éxito»; **F1** = «limpio > 1e-13».

| caso | MPM `err_s_rel_max` | Prony/LP | C1 | F1 | `gap_sv` | `cond_Z` | `res_recon_rel` MPM | `res_recon_rel` Prony |
|---|---|---|---|---|---|---|---|---|
| `sin_ruido_K1` | **9.032349316464501e-16** | 5.9674784485486205e-15 | **1** | 0 | 3.7869042782210825e15 | 1.0939859848455114 | 1.5530611110070798e-15 | 1.0615470146041753e-14 |
| `sin_ruido_K2` | **1.3773311131392578e-15** | 5.206063106536604e-13 | **1** | 0 | 5.40655506890537e14 | 1.3369194044929071 | 1.0112621634232694e-15 | 3.336901416111741e-13 |
| `sin_ruido_K3` | **4.75261048138531e-15** | 4.663070950568567e-10 | **1** | 0 | 2.2298514906235344e14 | 1.513305396832809 | 1.9991099543545665e-15 | 7.832690228826263e-11 |
| `ruido_K3_snr100` | 2.6292191037661718e-05 | 0.031171371251228985 | 0 | 0 | 4.803630655742079e3 | 1.5133145299701203 | 9.77036640953822e-06 | 9.617494824610502e-02 |

- **C1 = 1 en los tres casos limpios** ⇒ criterion (3) cumplido **sin ruido**. El peor limpio (K=3) está
  **2.1× por debajo** del umbral 1e-14 y **21× por debajo** de F1.
- **Contraste Prony/LP**: sistemáticamente peor y **degradándose con el orden** (5.97e-15 → 5.21e-13 →
  4.66e-10) ⇒ el método de contraste **no** sustituye al MPM; se declara la discrepancia, no se elige en
  silencio.
- En ruido: `rank_rel = 60 ≠ 6 = rango_declarado` y **F2 queda en 0** porque F2 sólo aplica **sin ruido**
  (conformación al sello).
- `residuo_conjugado = 0.0` con `F5_evaluado = 1` y `n_pares = 1/2/3` ⇒ el guard funcionó: hay **objeto**
  medido detrás del cero (§9).

**Trampa de rótulo corregida.** El resumidor ad-hoc usaba `rojos = [k for k,v in cortes.items() if v == 1]`,
que **etiqueta como rojos** `C1` (criterio de **éxito**) y `F5_evaluado` (guard «F5 se evaluó»). **Sólo
F1..F8 son cortes**; `F8` vive en la suite del driver, no en `cortes`.

---

## §3. BARRIDO SNR — LA COTA DE ERROR (±) COMO FUNCIÓN DEL SNR

Crudo `sim/data/crudo_extractor_pase2_snr_20261013T110453Z.json`, `RC=0`.

| `snr_objetivo` | `snr_medido` | `err_s_rel_max` | `n_recuperados` | `gap_sv` | `cond_Z` | `abs_s_dt_min` |
|---|---|---|---|---|---|---|
| 140 | 139.8947 | 2.6288e-07 | 3 | 4.8040e+05 | 1.5133 | 0.096047 |
| 120 | 119.8947 | 2.6288e-06 | 3 | 4.8039e+04 | 1.5133 | 0.096047 |
| 100 | 99.8947 | 2.6292e-05 | 3 | 4.8036e+03 | 1.5133 | 0.096048 |
| 80 | 79.8947 | 2.6331e-04 | 3 | 4.8006e+02 | 1.5134 | 0.096061 |
| 60 | 59.8947 | 2.6728e-03 | 3 | 4.7706e+01 | 1.5142 | 0.096188 |
| 40 | 39.8947 | 3.1315e-02 | 3 | 4.4771e+00 | 1.5230 | 0.097899 |
| 20 | 19.8947 | 7.2208e-02 | **1** | 1.0785e+00 | 1.5527 | 0.192560 |

- De 140 a 40 dB el error **cae ≈ 1/SNR** (2.63e-07 → 3.13e-02 en 100 dB de recorrido: razón 1.19e+05 para
  1e+05 de SNR ⇒ pendiente ≈ 1.0). **A 20 dB se pierde la mitad del objeto**: `n_recuperados = 1` (dos polos
  sin pareja ⇒ **NO RECUPERADO**) y el error salta a 7.22e-02.
- `F6` (el error debe **bajar** con el SNR) se imprime como **DECLARADA, NO ADJUDICADA**, verbatim del
  instrumento: `{lectura: "BAJA", err_al_snr_max: 2.628789013405541e-07, err_al_snr_min:
  0.07220835138967006, estado: "DECLARADA, NO ADJUDICADA (una sola tirada por celda)"}` ⇒ una sola tirada
  por celda **no adjudica** una tendencia.
- `F3` (`gap < 1e6`) y `F7` (`W < 20` periodos del modo lento) se encienden en **todas** las filas: en el
  barrido SNR la ventana es corta por construcción (§9).

---

## §4. BARRIDO DE VENTANA — Y EL **DEFECTO DE DOMINIO DEL UMBRAL SELLADO** (declarado, no reparado)

Crudo `sim/data/crudo_extractor_pase2_ventana_20261013T110453Z.json`, `RC=0`. El sello §8 pide ventanas en
periodos del modo lento {20, 40, 80, 160, 320}. El instrumento mide y declara el dominio **antes** de
disparar (`dominio_del_sello`, verbatim):

> `T_modo_mas_lento = 41.8879` · `W(20 periodos) = 837.8` unidades · decaimiento del polo 1 en esa ventana =
> **4.299e-33** (contra `eps = 2.220e-16`) · lista de decaimientos `['4.299e-33','1.848e-65','3.415e-130',
> '1.166e-259','0.000e+00']`.

⇒ A 20 periodos del modo lento la señal del polo 1 está **17 órdenes por debajo del piso de redondeo**, y a
320 periodos vale **exactamente 0.000e+00**. **No hay objeto que extraer: hay que declararlo.** El sello se
respeta leyendo el barrido en la zona donde sí hay objeto (el defecto **no se repara bajando el umbral**).

| `etiqueta` | `W_muestras` | `T` | `W/T_lento` | `err_s_rel_max` | `n_rec` | `gap_sv` | F1 |
|---|---|---|---|---|---|---|---|
| 0.125 | 15 | 7.00 | 0.1671 | 2.9325e-06 | 3 | 1.8175e+07 | **1** |
| 0.25 | 30 | 14.50 | 0.3462 | 2.0219e-10 | 3 | 9.1583e+09 | **1** |
| 0.5 | 60 | 29.50 | 0.7043 | 7.7391e-14 | 3 | 2.7713e+13 | 0 |
| 0.75 | 91 | 45.00 | 1.0743 | 1.0201e-14 | 3 | 2.1094e+14 | 0 |
| 1.0 | 121 | 60.00 | 1.4324 | **4.7526e-15** | 3 | 2.2299e+14 | 0 |

Lectura: mejora **monótona** con la ventana; **sólo la ventana completa (60 unidades ≈ 1.43 periodos del
modo lento) alcanza la precisión de máquina** (C1). Con menos de 0.7 periodos el error se estanca en
1e-10…1e-14 ⇒ **la ventana, no la aritmética, es la que fija el suelo** (coincide con §5).

---

## §5. BARRIDO `dt` — Y EL PISO `eps` COMO **COTA INFERIOR**, NO COMO RESTRICCIÓN ACTIVA

Crudo `sim/data/crudo_extractor_pase2_dt_20261013T110454Z.json`, `RC=0`. Declaración del instrumento
(verbatim): `{T_fijo: 20.0, por_que: "ds/s = dz/(z*|s|*dt): con T fijo, mover dt mueve |s|*dt.",
N_resultante: {0.0125:1601, 0.025:801, 0.05:401, 0.1:201, 0.2:101, 0.5:41},
dt_del_driver_k2: "cfl*h con cfl=0.50, delta0=0.05, k=2 => dt = 0.0125"}`.

| `dt` | `N` | `err_s_rel_max` | `n_rec` | `abs_s_dt_min` | `piso_predicho` = `eps/(abs_s_dt)` | `gap_sv` |
|---|---|---|---|---|---|---|
| 0.0125 | 1601 | 1.3593e-10 | 3 | 0.002401 | 9.247e-14 | 3.3409e+10 |
| 0.025 | 801 | 8.2150e-11 | 3 | 0.004802 | 4.624e-14 | 2.9347e+10 |
| 0.05 | 401 | 4.2274e-11 | 3 | 0.009605 | 2.312e-14 | 3.3669e+10 |
| 0.1 | 201 | **2.5818e-12** | 3 | 0.019209 | 1.156e-14 | 1.4471e+11 |
| 0.2 | 101 | 1.2450e-11 | 3 | 0.038419 | 5.780e-15 | 3.3154e+11 |
| 0.5 | 41 | 9.9826e-13 | 3 | 0.096047 | 2.312e-15 | 2.1235e+11 |

- **No es monótono en `dt`** (el mejor es 2.58e-12 a `dt=0.1`, y 9.98e-13 a `dt=0.5`) porque con T fijo
  mover `dt` mueve **dos** cosas a la vez: la ventana en periodos **y** `|s|*dt` (§3 del sello).
- **Todo error medido está POR ENCIMA del piso predicho** (a `dt=0.0125`: 1.36e-10 medido contra 9.25e-14
  predicho, **≈1472×**) ⇒ el piso `eps/(|s|dt)` es una **cota inferior**, no la restricción activa. A T=20
  la restricción activa **es la ventana** (§4). Se declara; no se inventa umbral nuevo.

---

## §6. CERTIFICACIÓN DEL SISTEMA (`gw-rw-zerilli`) — CRITERIO (4)

Corrida `sim/extractor_polos_matrixpencil.py --modo driver` (`RC=0`, iniciada `2026-10-13T11:05:40Z`,
≈96 s) ⇒ crudo `sim/data/crudo_extractor_pase2_driver_20261013T110716Z.json`,
`d["fisico"]` + `d["serie"]` (**el modo driver anida en `fisico`, no en `driver`**).

**Serie física** (`--potencial rw --l 2 --M 1.0 --cfl 0.50 --delta0 0.05 --rsmin -40 --rsmax 150 --tmax 100
--xc 0 --sigma 3 --robs 40 --t1 48 --t2 92 --k-fisico 2`, `--offset no-anidado`):
`{k:2, h:0.0125, delta:0.03333333333333333, dt:0.00625, nodos:15198, nsteps:16000, estable:1,
driver_sha256_16:"72df3878e2245bd0", driver_blob:"62931cf059d72f797d66b4e6ed9d1b8e0958c95e"}`.
Ventana: `{t1:48.0, t2:92.0, n:7041, T:44.0, escala:0.2913310315471783}`.

**Polos (ordenados por `ds_contra_leaver_abs`; `s = −ω_I ± i ω_R`):**

| K | `wR` | `wI` | `modA` | `ds_abs` | `ds_rel` | `F8_polo` |
|---|---|---|---|---|---|---|
| 1 | 0.3847007752 | 0.0809303531 | 1.126909 | 1.3644e-02 | 3.5520e-02 | 0 |
| 2 | **0.3733455436** | **0.0884342455** | 1.288999 | **6.1781e-04** | **1.6084e-03** | 0 |
| 2 (2º) | 0.3785651645 | 0.2883454171 | 0.548380 | 1.9945e-01 | 5.1924e-01 | **1** |
| 3 | **0.3739164686** | **0.0884740647** | 1.283989 | **5.4487e-04** | **1.4185e-03** | 0 |
| 3 (2º) | 0.3737192386 | 0.3079782138 | 0.552087 | 2.1902e-01 | 5.7019e-01 | **1** |

- **`F8_caso = 0` en K1, K2 y K3 ⇒ NO hay divergencia declarada contra Leaver** (umbral sellado 5e-2). El
  veredicto de caso lee **el polo más cercano**; los polos espurios (ω_I ≈ 0.288/0.308) cargan `F8_polo = 1`
  y son el precio que el modelo paga por la cola de la serie.
- **Lectura model-free:** `wR = 0.3733455436` vs Leaver `0.37367` (Δ = 3.2446e-04, **0.087 %**) y
  `wI = 0.0884342455` vs `0.08896` (Δ = 5.2575e-04, **0.59 %**) a K=2; **estable en orden** a
  `|Δs|/|s| ≈ 1.49e-03` (1.6084e-03 → 1.4185e-03 entre K=2 y K=3).
- **Cautelas declaradas.** `rank_rel_1e-12 = 18 ≠ 2K` y `gap_sv = 2.923048e+01 / 2.615462e+01 / 1.079391e+00`
  ⇒ **el hueco de valores singulares NO discrimina en la serie física** (no es una suma finita de
  exponenciales): el orden K es una **elección**, no un rango medido. `W_periodos_lento = 2.6167 < 20` ⇒
  **F7 es FRONTERA**, también aquí. La amplitud **no converge en K** (|A| ≈ 1.127 / 1.289 / 1.284) ⇒ la
  amplitud no certifica nada.

---

## §7. HALLAZGO: **LA LECTURA DE UN MODO ÚNICO ES UN ARTEFACTO CONVERGENTE**

Medido sobre la **misma** serie, la **misma** malla, la **misma** ventana [48,92] y el **mismo** `robs`, con
**dos metros independientes**. La suite física del propio driver (comando
`python3 sim/driver_rw_zerilli_1d.py --modo fisica --tag pase2fisica`, `RC=0`, `5.359 s`, iniciado
`2026-10-13T11:09:12Z`) escribe
`sim/data/crudo_rw_zerilli_pase2fisica_20261013T110918Z.json` y lee, con su `fit_qnm` (mínimos cuadrados
Levenberg–Marquardt, **modelo asumido** `exp(−g t)(a cos(ω_R t) + b sin(ω_R t)) + c`, 5 parámetros):

`M_w_medido = [0.3841330991117816, −0.08140180862934848]` · `M_w_leaver = [0.37367, −0.08896]` ·
**`desv_rel = 3.360326610020356e-02`**.

**Contra mi MPM con K=1**, que es el **mismo objeto** (un solo modo, sin modelo asumido):
`wR = 0.3847007752`, `wI = 0.0809303531` ⇒ Δw_R = 5.6768e-04, Δw_I = 4.7146e-04,
**|Δs|/|s| = 1.876e-03**.

⇒ **Dos instrumentos de naturaleza distinta (LM paramétrico del driver y MPM algebraico sin modelo con K=1)
coinciden en 1.9e-3 sobre una lectura que está a 3.4 % de Leaver.** La lectura de un modo es **estable,
reproducible y falsa**: no es ruido. Y el MPM con **K ≥ 2**, al modelar el segundo componente, **corrige** el
polo dominante a **1.4e-3** de Leaver.

**Consecuencia de método.** El número de polos **no es ornamento**: es la diferencia entre un artefacto
convergente y la frecuencia del objeto. Y como el error del extractor (1.4e-3) es del **mismo orden** que su
propio residuo de reconstrucción (3.04e-3, `residuo_reconstruccion_rel` a K=3), la precisión del polo la fija
**cuánto se parece la serie a una suma finita de exponenciales**, no la aritmética del extractor.

---

## §8. CONTRASTE DE METROS (mismo objeto, ventanas idénticas)

| metro | modelo | parámetros | residual relativo en la ventana | desviación vs Leaver |
|---|---|---|---|---|
| driver `fit_qnm` | **asumido** (1 QNM + offset) | 5 | 1.2402e-02 (rms 3.613e-03 sobre `escala` 0.2913310315471783) | **3.3603e-02** |
| extractor MPM | **ninguno** | 2K = 6 | **3.0425e-03** | **1.4185e-03** |
| extractor Prony/LP | ninguno | p = 6 | 1.2406e-02 | ~1.9e-02 (polo más cercano) |

- El MPM describe la ventana **4.1× mejor** (3.04e-03 vs 1.24e-02) **sin** que le den el modelo, y su polo
  está **24× más cerca** de Leaver que el del driver.
- **El `3.36e-2` del driver NO es error de discretización.** La misma corrida da `p_richardson =
  2.099608060738076` (RW) y `2.1087235074440547` (Zerilli), con `nota_p = "OK"`, y la amplitud funcional
  `A` varía sólo en la 6ª cifra entre mallas (25.37450124 → 25.37261387 → 25.37217350) ⇒ la solución del
  problema de valores iniciales **está convergida a orden 2** con estabilidad ~1e-5, y el `M_w_R` del propio
  estimador se mueve apenas 1.24e-05 entre mallas (0.3841455389 → 0.3841330991). ⇒ **La desviación del
  3.36 % es propiedad del ESTIMADOR (un modo + offset sobre 44 unidades de ventana), no del objeto.**
- **Isospectralidad** RW vs Zerilli (malla k=2, `desv_rel = 4.2726912441951904e-03`): 0.43 %.
- **Frontera de namespaces (no mezclar).** El certificado `F1` del driver (`err 1.2e-14 … 3.4e-13`, commit
  `5b064f7`) pertenece a la suite **nula d'Alembert a CFL 1.00** — **otro objeto**. Y el `F3` del driver
  (`richardson`) es **otro namespace** que el `F3` del extractor (hueco de valores singulares).

---

## §9. DEFECTOS DECLARADOS (no adjudicados, no reparados)

1. **F5 es INERTE por construcción.** Sobre `Z` real los autovalores nacen en pares conjugados bit-exactos ⇒
   el residuo conjugado vale **exactamente 0.0** siempre. «Una salida que no puede diferir no es evidencia.»
   Declarado en el docstring de `mpm()` y en `cabecera()["defectos_del_metro_declarados"]`. **Guard nuevo:**
   `F5_evaluado` — un 0.0 **sin** `residuo_conjugado_pares` no es un verde.
2. **`driver_modificado` es un literal `False` hard-codeado: no mide nada.** Lo que **sí** protege es el par
   vivo `driver_sha256_16` + `driver_blob` (calculados del archivo en el momento) **más** un chequeo
   independiente: `git status --porcelain -uall -- sim/driver_rw_zerilli_1d.py` ⇒ **vacío** (medido
   `11:07:51Z`), limpio contra `5b064f7`.
3. **El hueco de valores singulares no discrimina en la serie física** (§6): `rank_rel = 18`, `gap` = 29.2 /
   26.2 / **1.08** ⇒ el orden K es elección declarada.
4. **F7 es frontera en casi todo el ciclo** (`W < 20` periodos del modo lento): en la serie física vale
   **2.6167**. No es un fallo: es el borde declarado del instrumento.
5. **Dominio del umbral sellado** (§4): la ventana de 20 periodos del sello queda **17 órdenes** por debajo
   de `eps`. Se declara; **no se baja el umbral**.
6. **F2 tiene dominio declarado** (`sin_ruido`), conforme al sello; **F6 declarada y no adjudicada** (una
   tirada por celda).

---

## §10. CORRECCIONES DE ESTE CICLO (cifras mías, caducadas o mal rotuladas)

1. **Identidad del driver — mi cifra anterior era CADUCA.** La nota previa decía «565 l · 23 523 B · sha16
   `790aa7ae7ea02d19`»; eso describía el **driver V1**. Medido en vivo a `2026-10-13T11:07:51Z`
   (`shasum -a 256` + `git hash-object` + `wc -l -c` + `git status`): **599 l · 25 638 B · sha256_16
   `72df3878e2245bd0` · blob `62931cf059d72f797d66b4e6ed9d1b8e0958c95e`**, limpio contra `5b064f7`. El crudo
   del extractor **ya traía la cifra correcta** (la mide en vivo) ⇒ el error era de mi nota, no del crudo.
   *Toda cifra sin hora no es cifra.*
2. **`C1` y `F5_evaluado` NO son rojos** (§2): el resumidor los mal rotulaba; sólo F1..F8 son cortes.
3. **Trampa de clave del crudo:** el modo driver **anida en `fisico`** (más un `serie` de nivel superior);
   `d["driver"]` levanta `KeyError`.
4. **Trampa del gate (medida):** un destino **no rastreado** hace que la condición «estado limpio» sea
   **estructuralmente inalcanzable** ⇒ **RC 13**; se salió con commit de custodia (`0bd4d6f`, `0feb32a`,
   precedente literal «instrumento defectuoso preservado» `d7856c1`) hasta **RC 0** a `11:01:42Z`.

---

## §11. ESTADO Y PENDIENTES

- **Criterio (3) cumplido**: C1 = 1 en los tres casos limpios (peor 4.75e-15) con cota de error mapeada
  contra SNR (§3) y contra la ventana de corte (§4, §5).
- **Criterio (4) cumplido**: `F8_caso = 0` en K1/K2/K3 ⇒ **no hay divergencia** contra Leaver; margen medido
  **1.42e-3 contra un umbral de 5e-2** (2.8 % del umbral), mientras **el propio metro del driver se queda en
  3.36e-2, el 67 % del umbral** (§7, §8). Margen cuantificado; defectos declarados, ninguno reparado bajando
  un umbral.
- **Crudos de este ciclo** (5, en `sim/data/`, pendientes de commit): `…pase2_snr_20261013T110453Z.json`
  (6 177 B) · `…pase2_ventana_20261013T110453Z.json` (5 628 B) · `…pase2_dt_20261013T110454Z.json`
  (5 916 B) · `…pase2_driver_20261013T110716Z.json` (10 840 B) ·
  `crudo_rw_zerilli_pase2fisica_20261013T110918Z.json`. Se suman a `…pase1_…T105015Z.json` y
  `…pase2_…T110322Z.json`, ya en `0bd4d6f`.
- **Limpieza:** `sim/__pycache__/` (subproducto de **mi** importación del driver a `11:05:40Z`) **borrado**
  a `11:09:52Z`.
- **Pendientes sin elevar:** el hueco de valores singulares en la serie física (¿malla? ¿cola?); si conviene
  un piso declarado para `residuo_reconstruccion_rel` (no se inventa sin medir su dominio); habilitar
  cavidades Maxwell con pérdidas (mismo extractor, otro potencial).
- **Intocables:** el driver (`sim/driver_rw_zerilli_1d.py`, SOLO LECTURA) · el pre-registro (sellado,
  append-only) · `sim/reflexion_frontera_1d.py` (otra mano).
