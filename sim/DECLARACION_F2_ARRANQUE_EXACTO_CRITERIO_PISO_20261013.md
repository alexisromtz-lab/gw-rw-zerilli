# DECLARACION F2 — ARRANQUE EXACTO, ESCALERA ACOPLADA Y CRITERIO DEL PISO (13-Oct-2026)

HUELLA-DECL-F2-ARRANQUE-EXACTO-CRITERIO-PISO-20261013

UNIVERSO DECLARADO: 3 crudos `sim/data/crudo_2d_f2_richardson_post_arranque_nr0_{64,128,256}_*.json`
(medidos hoy, TZ=UTC) + `sim/arnes_richardson_2d_f2.py` (v1, el citado) + `sim/arnes_richardson_2d_f2_v2.py`
y `_v3.py` (instrumento vivo) + `sim/data/crudo_2d_f2_richardson_20261013T201320Z.txt` (crudo del piso, v1).
UNIDAD: cifras tal como las imprime el crudo (sin re-redondeo). VENTANA: los tres crudos de hoy.
CONTENCION VIGENTE: cero commits en `gw-rw-zerilli`; esto es DECLARACION, no acta de cierre de F9/F2.

## 1. La clausula ordenada YA estaba escrita (A2.1 · RC 11)

- `sim/arnes_richardson_2d_f2_v2.py` y `sim/arnes_richardson_2d_f2_v3.py` son BYTE-IDENTICOS:
  `shasum -a 256` = `baa7b652fb6d16e26532644bdc22c72766ecbeacf57e3f21203c7998c50be347` en los dos;
  779 l / 39887 B en los dos; blob de v3 = `08adc845435f34a473d13c34bef3fea591356707`.
- El arranque exacto (Cauchy simetrica) vive en `simula()` de los dos:
  `u_m1 = u + 0.5*dt*dt*a0 ; v = (u - u_m1)/dt` con los bordes Dirichlet re-puestos ⇒ equivale a
  `v^{-1/2} = -0.5*dt*a(u^0)`. El defecto v1 (`v^{+1/2} = +0.5*dt*a(u^0)`) inyecta O(dt).
- ⇒ Integrar era escribir sobre una fila ya escrita por otra mano: **cumplida pasivamente, cero escrituras**
  sobre el instrumento.
- CORRECCION DE REGISTRO: el apunte previo «v2 = 576 l / 28318 B» es CADUCO. 576 l / 28318 B y
  sha256 `89b51857c76b918de0da23bd79e260f0239832f51793e1ed208cce8a329efaf6` es **v1** (el crudo lo cita
  como `transferencia.sha256_v1`). v2 == v3, no v2 == v1.
- `sim/arnes_richardson_2d_f2_v4_arranque_exacto.py` (blob `e10a51dbeb0fa80bdbabeb5ffa7f166dcbad63e9`,
  729 l / 40920 B, 16 hunks / 547 lineas contra v3) = duplicado de lectura vieja:
  **declarado, NO adjudicado; no corrido, no parcheado, no borrado.**

## 2. La vuelta A2.1 del crudo nuevo (nr0 = 256)

- PRE (ruta absoluta): TARGET ausente ⇒ **RC 10** (autorizado) el 13-Oct-2026; stamp `20261013T203521Z`.
- Corrida: `python3 -B sim/arnes_richardson_2d_f2_v2.py --estricto --nr0 256 --json auto
  --stamp 20261013T203521Z` ⇒ **RC 1** (fail-closed por C6).
- Crudo: `sim/data/crudo_2d_f2_richardson_post_arranque_nr0_256_20261013T203521Z.json`
  · 312 l · 6924 B · sha256 `2099a561d9ad647d03de4f14353f4902eb1a3b29b93ac8af0f9dcb94b7c8c6e6`
  · `git hash-object` `9a087d40f9db04b8653ccbe3846ebcd12925a482` · duracion 4.641713857650757 s.
  `arranque = "exacto: u^{-1} = u^0 + 0.5 dt^2 a(u^0), v = (u^0 - u^{-1})/dt"`.
- POST con la huella que YO declare en el PRE (`HUELLA-CRUDO-2D-F2-POST-ARRANQUE-NR0-256-<stamp>`)
  ⇒ **RC 12** (desfase de objeto): esa huella **no viaja al objeto**.
- POST con la huella que el instrumento SI emite (`HUELLA-ARNES-RICHARDSON-2D-F2-V2-20261013`)
  ⇒ **RC 11** (la huella ya habita en el target) ⇒ fila ya escrita, cerrada pasivamente.
- **REGLA QUE ESTE CRUDO DEJA, medida:** cuando el escritor es un instrumento, la huella del PRE tiene que
  ser la que el instrumento emite; si no, el POST no puede cerrar en 11 y cae en 12 (defecto mio de PRE,
  declarado; el crudo no se toca).

## 3. Escalera acoplada con arranque exacto activo en los tres niveles

UNIVERSO DECLARADO: celdas `F2 PRINCIPAL` y `C2 REDUCCION` de los tres crudos.

| nr0 | nr L0/L1/L2 | F2 d1 | F2 d2 | razon d1/d2 | p | veredicto | d2 / piso previo |
|---|---|---|---|---|---|---|---|
| 64  | 64/126/250   | 2.997601e-01 | 7.542526e-02 | 3.974267 | 1.990689 | VERDE | 6.975805 x |
| 128 | 128/254/506  | 7.415692e-02 | 1.852510e-02 | 4.003051 | 2.001100 | VERDE | 1.713318 x |
| 256 | 256/510/1018 | 1.998241e-02 | 4.985697e-03 | 4.007948 | 2.002864 | VERDE | 0.461109 x |

`dt_cota` (= T / ceil(T/dt_cota), CFL sellado 0.50, fail-closed): 64 → 4.85108880e-02 / 2.67526453e-02 /
1.46147844e-02 · 128 → 4.68635223e-02 / 2.45449584e-02 / 1.28210451e-02 · 256 → 4.16098506e-02 /
2.11914566e-02 / 1.07847285e-02. UMBRALES EN VIGOR: `p_esperado 2.0`, `umbral_p 0.05`.

- **C2 REDUCCION** (control de reduccion): razon 3.974790 / 4.003108 / 4.012232 · p 1.990879 / 2.001120 /
  2.004405 ⇒ **VERDE 3/3**.
- **C3b ANGULAR ORDEN 1** (control negativo angular): razon 3.290932 / 2.223954 / 1.980342 ·
  p 1.718496 / 1.153127 / 0.985750 ⇒ **ROJO 3/3 y NO MONOTONO** (1.72 → 1.15 → 0.99). Se declara; no se adjudica.
- **C3a RADIAL ORDEN 1** (control negativo radial): **NO MEDIBLE 3/3** (razon 1.095663e-22 · 1.898035e-45 ·
  `inf`; el control explota o se anula y la senal cae bajo el piso de redondeo). Se declara.

## 4. El criterio del piso — lectura declarada

- `REF_PISO_F2 = 1.081241e-02`, medido por **v1** (con el defecto de arranque) en
  `sim/data/crudo_2d_f2_richardson_20261013T201320Z.txt`: d1 = 5.431712e-02 · d2 = 1.081241e-02 ·
  razon = 5.023592 · p = 2.328719 · **ROJO**.
- Pregunta ordenada: «si el error del par fino cae por debajo del piso previo (1.08e-2)».
  Respuesta medida: **SI, solo en nr0 = 256** (4.985697e-03 = 0.461109 x piso; 2.169 x por debajo).
  En nr0 = 64 (6.975805 x) y nr0 = 128 (1.713318 x) **NO cae**.
- COCiente contra la referencia del paquete aislado (`ref_d2_exacto_sonda = 4.224460e-04`, arnes ajeno,
  testigo `crudo_aislamiento_piso_2d_20261013T200929Z.json`): 178.55 x / 43.85 x / 11.80 x
  (division de las cifras medidas; no es campo del crudo).
- **CAVEAT DE METRO (declarado, NO adjudicado):** el piso lo midio v1 sobre la malla de evaluacion vieja
  (anclada en `rs_min`) y v2 la ancla en las coordenadas reales del paquete (DELTA 2) ⇒ la comparacion
  **cruza dos ventanas**; y el piso es de nr0 = 64 comparado contra `d2` de nr0 = 256 ⇒ **cruza dos mallas**.
  Los dos numeros se imprimen; **ninguno se elige**.

## 5. Segundo orden: restaurado

- p(F2) = 1.990689 / 2.001100 / 2.002864 con umbral `|p-2| <= 0.05` ⇒ **VERDE 3/3**
  (contra v1: p = 2.328719 ROJO con razon = 5.023592 > 4).
- razon d1/d2 = 3.974267 / 4.003051 / 4.007948 (esperado 4 para p = 2).

## 6. Triplete de residuos — y su ceguera a nr0 POR CONSTRUCCION

- `cotejo_L2` (3 renglones, uno por nivel de la escalera): `residuo_rel_max` = **1.400145e-03 /
  3.510557e-04 / 8.782769e-05** — **identico en los tres nr0**; razones 3.988 / 3.997.
- CAUSA MEDIDA (codigo leido, v3 l.244-253 y l.591-601): `certifica_L2(m)` certifica el **OPERADOR ANGULAR**
  contra referencia **analitica externa** (`L2 P_2 = 6 P_2`) sobre `mall_demo` (los tres niveles a `nt0`),
  con `u = np.tile(P_2(cos t), (m.nr, 1))`. Depende de la malla **theta** del nivel y **no de `nr`**
  ⇒ el mismo triplete en los tres nr0 **por construccion**.
- ⇒ **El triplete de residuos NO mide la malla radial: certifica el operador angular.** Un instrumento que
  no puede diferir con `nr0` no es evidencia sobre `nr0`. Se reporta con su unidad y su dominio declarados.

## 7. El unico rojo

- `rojos = ["C6 contencion: la malla de evaluacion no cubre las coordenadas reales del paquete"]`
  en los **TRES** crudos (y fue el unico rojo en los tres).
- `c6 = {banda_declarada [16,28], banda_entrante [8,20], banda_paquete [8,36], cubre_declarada true,
  cubre_entrante false, cubre_paquete false, tolerancia 0.0392156862745098}`.
- `ventana = {lo 8.0, hi 36.0, rs_e_ini 8.045751633986928, rs_e_fin 35.967320261437905,
  dr 0.0392156862745098, n_theta 33, nq 713}`.
- ⇒ **VEREDICTO DE GATE 2D-F2: ROJO (fail-closed)**, por C6 y **solo** por C6 ⇒ las cifras F2 quedan
  **provisionalmente contaminadas** mientras la contencion ventana↔paquete no se cierre (declarado; el
  instrumento **no se parchea** sin orden).

## 8. Veredicto F2 (para la orden recibida)

1. **Arranque exacto: integrado y activo** — vivia ya en el instrumento (v2 == v3); la corrida lo ejecuta y
   el crudo lo declara (`arranque = "exacto: ..."`).
2. **Segundo orden: restaurado y certificado 3/3** (p = 1.990689 / 2.001100 / 2.002864 VERDE; C2 VERDE 3/3).
3. **Criterio del piso: se cumple solo en el nivel fino nr0 = 256** (0.461109 x piso); **no** en 64 (6.98 x)
   ni en 128 (1.71 x), con el caveat de que piso y `d2` viven en ventanas y mallas distintas.
4. **F2 NO CIERRA: ROJO por C6** (contencion ventana↔paquete). **No hay rojo de fisica medido**; el rojo es
   de ventana/etiqueta de la malla de evaluacion.

## 9. Declarado sin adjudicar (en pie)

- v4: duplicado de lectura vieja (blob `e10a51db…`), no corrido.
- La huella interna de la pieza viva dice `…-F2-V2-20261013` en `_v3.py` (nombre viejo en pieza viva).
- `cotejo_L2` (triplete) ciego a `nr0` por construccion.
- C3b no monotono (1.72 / 1.15 / 0.99); C3a NO MEDIBLE 3/3.
- `orden_p` con base 2 fija; `piso_ref` inerte; `--control-orden1-*` inerte; discrepancia del Δt del §7.1;
  `ventana_ajena`; la banda del paquete [8,36] es una **etiqueta no ratificada**.
- Estado de git y de las piezas nuevas: **sin commits**; lo untracked se declara, no se adjudica.
