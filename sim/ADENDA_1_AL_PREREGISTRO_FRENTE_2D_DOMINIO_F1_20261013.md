# ADENDA 1 AL PREREGISTRO DEL FRENTE 2D — DOMINIO MEDIDO DEL GATE 2D-F1

HUELLA-ADENDA-1-DOMINIO-F1-2D-20261013

- Fecha: 2026-10-13 · Repo: `gw-rw-zerilli` · Frente: 2D axisimetrico (t, r*, theta)
- Relacion con lo sellado: APENDICE. El pre-registro sellado es append-only: **no se edita**, solo recibe apendices.
- Estado de este documento: CRUDO REGISTRADO. El estado de "gate validado" lo mueve el dueño, no el instrumento.

---

## §0. CONTRATO A2.1 Y POSTURA DE COLISION

Orden recibida: pre-registrar el **Gate 2D-F1** (prueba nula bidimensional de d'Alembert en espacio plano, `V = 0`, a CFL optimo 2D `1/sqrt(2)`, exigiendo residuo nulo a `< 1e-13`).

Target que la orden implicaba: `sim/PREREGISTRO_FRENTE_2D_CQG_20261013.md`.

Medido ANTES de escribir (A2.1, gate determinista, RC = 10 = ausencia; y luego identidad del objeto hallado):

| propiedad | valor medido |
|---|---|
| existencia | YA EXISTE |
| sello | 100 l · 11465 B · blob git `2b2dd0fa898cf9de29434899eb2de07f6bbadfca` |
| commit | `2eebc3b` ("sello(frente2d): preregistro sellado del frente 2D …") |
| huella propia | `HUELLA-PREREGISTRO-FRENTE-2D-CQG-TEUKOLSKY-20261013` |
| ventana declarada por el | `T_UTC_VENTANA: 2026-10-13T18:52:00Z` |
| encabezados `^#` | 11 |
| signos monetarios | 0 |

**ESTADO: YA ESCRITO · HUELLA IDENTIFICADA EN TARGET · CERO ESCRITURAS.**

No se duplica el pre-registro. No se edita el pre-registro. No se renumera nada.

**Lo que el pre-registro sellado NO cubre** (y por eso esta adenda existe): sus cortes empiezan en **F8** (§6) y terminan en F14. **No tiene F1.** El Gate 2D-F1 ordenado, y sobre todo su **DOMINIO**, no estaban registrados en ninguna parte. Esta adenda los registra, con crudo.

---

## §1. UNIVERSO / UNIDAD / VENTANA / COMANDO / IDENTIDADES

Verbatim del instrumento (no se retipea ninguna cifra):

- **UNIVERSO DECLARADO**: malla 2D periodica 128 x 128, h = 0.100000, L = 12.800000, cfl = 0.7071067812 (= 1/sqrt(2)), T = 10.000, modos enteros (mx,my), residuo L2 relativo.
- **QUEDA FUERA** (no se mide aqui): capa absorbente de perimetro · fondo curvo M > 0 · eje theta = 0, pi (regularidad polar) · angulo rasante · no linealidad.
- **UNIDAD**: residuo L2 relativo `||u_num - u_exacta|| / ||u_exacta||` (adimensional).
- **VENTANA**: T = 10.0 fijo; n = round(T/dt) pasos.
- **UMBRAL**: 1e-13.
- **NULO**: el MISMO operador con el medio paso CONTINUO sobre la MISMA familia. Si el nulo bajara tanto como el objeto, el gate no discriminaria nada.
- **COMANDO**: `python3 -B sim/sonda_2d_f1_dominio.py --estricto`

Identidades (medidas en disco, no impresas por la pieza):

| objeto | ruta | l · B | sha256 | blob git |
|---|---|---|---|---|
| instrumento | `sim/sonda_2d_f1_dominio.py` | 252 · 11357 | `5f77b302d3b9f8bc00c40879e2432e52f29583b450c970e6bec0c82b34fe5165` | `781212b7eacfe12d2b708ef6f28add93d807bf53` |
| crudo | `sim/data/crudo_2d_f1_dominio_20261013T192021Z.txt` | 74 · 4008 | `5f74eb8023e8ce1ce9b5256db42f87e6b31e023d5e9e9ae04fbf6a770ee6910d` | (untracked) |

- El sha256 que el instrumento imprime de si mismo (`HUELLA DEL INSTRUMENTO`) **coincide** con el del archivo en disco ⇒ el que corrio es el que esta.
- **INSTANTE UTC** impreso por la corrida: `2026-10-13T19:20:21Z`. El nombre del crudo se tomo de ese instante; no se eligio a mano.
- **RC_ESTRICTO = 0** (`VEREDICTO 2D-F1 (--estricto): VERDE`).
- **Desviacion declarada de convencion**: los crudos del repo son `crudo_*.json`; este es `.txt` porque es la **salida verbatim** del instrumento y no se retipea ninguna cifra.

---

## §2. QUE MIDE ESTE INSTRUMENTO (alcance)

Caso plano `M = 0`, toro periodico, modos exactos de la malla. En 2D el operador añade el acoplamiento angular `L2_theta`; la exactitud que se mide es de la **familia diagonal** (mx == my) a CFL optimo exacto.

Esto es un instrumento de ESQUEMA + DATO. **No es evidencia fisica** y no abre Kerr ni el eje polar.

---

## §3. SIMBOLO: LA EXACTITUD ES UNA IDENTIDAD, NO UNA CONVERGENCIA

`|xi - w*dt| / (w*dt)`, sin integrar (algebra pura):

| (mx,my) | ang_deg | desvio |
|---|---|---|
| (2,0) | 0.00 | 2.008823e-04 |
| (3,1) | 18.43 | 3.215860e-04 |
| (2,1) | 26.57 | 9.039931e-05 |
| (3,2) | 33.69 | 9.664291e-05 |
| (1,1) | 45.00 | **0.000000e+00** |
| (2,2) | 45.00 | 1.413580e-16 |
| (3,3) | 45.00 | **0.000000e+00** |
| (1,0) | 0.00 | 5.020470e-05 |

Mecanismo: a `cfl = 1/sqrt(2)` con `kx = ky = k`, `S = 2 sin^2(kh/2)` ⇒ `xi = k h = w dt` exacto. Fuera de la diagonal `xi > w dt` (error de fase O(angulo)).

⇒ La exactitud del simbolo vale **solo** sobre `mx == my` a `cfl = 1/sqrt(2)` **exacto**. Es una identidad algebraica; no es convergencia. Por eso el control que la vuelve evidencia es un control **10 ordenes** lejos (abajo), no una repeticion.

---

## §4. ESQUEMA vs DATO: EL HALLAZGO

Residuo L2 relativo a T = 10, N = 128, cfl = 1/sqrt(2). Objeto = medio paso DISCRETO; nulo = medio paso CONTINUO:

| (mx,my) | ang_deg | residuo (dato = disc) | residuo (dato = cont) |
|---|---|---|---|
| (2,0) | 0.00 | 7.459319e-04 | 7.538481e-04 |
| (3,1) | 18.43 | 1.185170e-03 | 1.200305e-03 |
| (2,1) | 26.57 | 1.900558e-02 | 1.932764e-02 |
| (3,2) | 33.69 | 4.434818e-03 | 4.572708e-03 |
| (1,1) | 45.00 | **3.444081e-15** | 1.828039e-06 |
| (2,2) | 45.00 | **2.573674e-14** | 6.505644e-05 |
| (3,3) | 45.00 | **1.423329e-14** | 1.863998e-04 |
| (1,0) | 0.00 | 1.337203e-03 | 1.351430e-03 |

Familia diagonal, mas modos (dato = disc | dato = cont | disc con referencia simbolica):

| m | disc | cont (nulo) | disc, ref=sim |
|---|---|---|---|
| 1 | 3.444081e-15 | 1.828039e-06 | 3.444081e-15 |
| 2 | 2.573674e-14 | 6.505644e-05 | 2.668732e-14 |
| 3 | 1.423329e-14 | 1.863998e-04 | 1.423329e-14 |
| 4 | 1.967306e-14 | 1.058347e-04 | 1.967306e-14 |
| 6 | 8.744309e-15 | 4.411139e-04 | 8.744309e-15 |
| 8 | 8.185048e-14 | 3.099581e-03 | 8.313321e-14 |

**Lectura**: sobre la diagonal el nulo queda 9 a 11 ordenes por encima del objeto. El defecto que las versiones v1/v2 atribuian al ESQUEMA era del **DATO**: con el medio paso **discreto** (xi del simbolo discreto) el esquema es exacto al piso de redondeo. Con el medio paso continuo se acumula `~ theta^4 / 3` por paso, lineal en n.

Frase que NO se puede escribir: "el esquema leapfrog 2D es exacto". Lo que se escribe: "con el dato discreto, sobre la familia diagonal a CFL optimo exacto, el residuo es el piso de redondeo".

---

## §5. EL PISO DE REDONDEO TIENE FIRMA DE IDENTIDAD (no de convergencia)

Refinado con `mx = my = 2`, dato = disc, CFL = 1/sqrt(2), T = 10:

| N | h | residuo 2D diag | residuo 2D eje (mx=2,my=0) | residuo 1D equivalente |
|---|---|---|---|---|
| 64 | 0.200 | 1.409270e-14 | 3.633376e-03 | 3.633376e-03 |
| 128 | 0.100 | 2.573674e-14 | 7.459319e-04 | 7.459319e-04 |
| 256 | 0.050 | 1.508196e-14 | 2.073124e-04 | 2.073124e-04 |
| 512 | 0.025 | 1.831377e-14 | 5.184681e-05 | 5.184681e-05 |

Dos lecturas, **dos metros distintos**:

1. **Diagonal**: 1.41e-14, 2.57e-14, 1.51e-14, 1.83e-14 ⇒ **independiente de h**. Un esquema convergente bajaria O(h^2). Que no baje es la firma de una **identidad**; el valor es el piso de redondeo de la malla doble (≈ 1e-14).
2. **Eje**: 3.63e-03, 7.46e-04, 2.07e-04, 5.18e-05 ⇒ factor 4 por halving ⇒ **O(h^2) limpio**; y el 1D equivalente da **identico digito a digito** en las cuatro filas. ⇒ El caso eje del 2D **reproduce el esquema 1D exactamente**: esto es el nulo de reduccion 2D a 1D (N-2D-0 del pre-registro sellado, §5), aqui medido, no postulado.

---

## §6. AGUDEZA DEL CFL: LA EXACTITUD ES UN PUNTO, NO UNA VECINDAD

`mx = my = 2`, dato = disc, N = 128:

| cfl | residuo | n |
|---|---|---|
| 0.500000 | 1.077678e-02 | 200 |
| 0.600000 | 6.825919e-03 | 167 |
| 0.700000 | 4.580104e-04 | 143 |
| **0.707107** | **2.573674e-14** | 141 |
| 0.707200 | 4.869481e-06 | 141 |
| 0.750000 | 2.922646e+24 | 133 |
| 1.000000 | 1.586612e+61 | 100 |

- **Exceso del desvio `cfl = 0.707200` sobre el optimo `1/sqrt(2)`**: observado `4.869481e-06` contra esperado `2.573674e-14` ⇒ **exceso absoluto 4.869481e-06**; razon del mismo hecho: **x 1.892e+08**.
- Un CFL **0.007 %** arriba del optimo queda **4.9e+07 veces** por encima del umbral 1e-13. `cfl = 0.75` ya es divergente (2.9e+24); `cfl = 1.0` es divergente puro (1.6e+61).
- **Metrica**: con un solo punto de comparacion se reporta **exceso absoluto**; la razon se imprime como lectura del mismo hecho, **no se promueve** (una metrica con n chico no se eleva).

---

## §7. DOMINIO DEL UMBRAL (la adjudicacion que faltaba)

El umbral `residuo < 1e-13` del Gate 2D-F1 **no es un enunciado universal**. Vale solo sobre las tres condiciones simultaneas:

- **(i) familia de malla DIAGONAL** `mx == my` (angulo 45 grados exacto);
- **(ii) `cfl = 1/sqrt(2)` EXACTO** (no aproximado: 0.707200 ya no califica);
- **(iii) medio paso DISCRETO** (xi del simbolo discreto), no el continuo.

Control negativo, modos NO diagonales al MISMO cfl optimo (dato = disc), que **no deben caer**:

| modo | residuo |
|---|---|
| (2,1) | 1.900558e-02 |
| (3,1) | 1.185170e-03 |
| (0,2) | 7.459319e-04 |

Y fuera de (iii): m = 1 → 1.828039e-06 … m = 8 → 3.099581e-03. Y fuera de (ii): 4.869481e-06.

⇒ **Enunciado correcto del Gate 2D-F1**: "en el caso plano periodico, sobre la familia diagonal, a CFL optimo **exacto** y con el medio paso **discreto**, el residuo L2 relativo a T = 10 es el piso de redondeo (1e-13 con margen de 1 a 2 ordenes)". Fuera de esas tres condiciones el gate es **ROJO legitimamente** y ese rojo NO es un defecto del objeto: es su dominio.

⇒ **Regla aplicada**: un umbral sellado puede comparar dos objetos distintos; su dominio se mide **antes** de dispararlo. Aqui se midio y se declara. **No se baja el umbral** en ninguna de las tres direcciones.

---

## §8. CUATRO DEFECTOS DE METRO DECLARADOS (ninguno compensado)

**(a) v1 — dato NO periodico.** `kx = k*cos(ang)` no es multiplo de `2*pi/L` ⇒ discontinuidad en la costura del toro ⇒ `np.roll` radia ⇒ residuo O(1), **maximo a 45 grados y nulo sobre los ejes**. Defecto del **METRO**, no del objeto: la refutacion que v1 produjo no era del esquema.

**(b) v2 — medio paso CONTINUO.** Acumula `~ theta^4/3` por paso, lineal en n. Defecto del **DATO**, no del esquema. Es el que separa "esquema inexacto" de "dato mal puesto" (esta es la correccion de la correccion).

**(c) v4.a — ASERCION INVERTIDA (mio, de este ciclo).** El predicado de agudeza de CFL se escribio de modo que **enrojecia exactamente cuando el objeto se comportaba bien**: el desvio de CFL debe EMPEORAR el residuo, no mejorarlo. Medido: `rd2 = 2.573674e-14` vs `rdet = 4.869481e-06` ⇒ `VEREDICTO 2D-F1 (--estricto): ROJO  rojos=1` con `RC = 1`. **No se bajo ningun umbral y no se re-toco ninguna cifra**: se corrigio la **direccion** del predicado y se imprimio el exceso. Instrumento retirado ANTES de sellar y conservado **fuera** del repo:
  - fuente: `sonda_2d_f1_v4a_invertida_20261013.py` · blob `9d3445863ceb1d25ed77cf81609742634d3db0b3` · sha256 `566c0bfb5fb6761474785bd94796c8b1017aa5e415bb52d0675484a4cf5d40dd` · 239 l · 10522 B;
  - crudo: `crudo_v4a_invertido_20261013T191833Z.txt` · sha256 `73a53548d7ffc963c4962bb5137b6b7f9c67b9dcb5bf842dd306eba49bbe0187` · 71 l · 3825 B · `RC_ESTRICTO = 1`.
  
  Sin esa copia del instrumento defectuoso, el crudo intermedio seria **irreproducible**.
  
  **Control de la reparacion**: los **55 renglones de DATOS** de v4.b son **IDENTICOS** a los del crudo v3 (`diff` = 0 lineas) ⇒ el cambio de version fue de cabecera y veredicto y **no movio ninguna cifra**.
  
  Familia ya conocida: *"un rango hecho con enumerate puede quedar invertido"* (el instrumento enrojece a su propio control) y *"un rotulo fijo que afirma lo que la linea siguiente desmiente no protege: informa"*.

**(d) `sim/reflexion_escala_D.py` — `ajuste()` ajusta UNA sola forma.** Ajusta `ln y = a*x + b` (exponencial) unicamente ⇒ su veredicto sobre la ley de la capa probo **una** forma. Con eso **no** se puede declarar que la forma de potencia no existe. Medido sobre las 24 filas unicas: residuo relativo maximo **3.02 %** (potencia `R_t = 9.8807e-02 * D^(-1.3936)`, p = 3) contra **23.2 %** (exponencial `4.0183e-03 * exp(-0.04368*D)`). ⇒ Mi dictamen previo ("la unica forma validada es la exponencial") es **ERRONEO tal como esta enunciado**. Se declara; no se corrige en silencio. (Familia: *un chequeo que busca UNA forma no certifica la ausencia de las otras*.)

---

## §9. LA LEY DEL 1D NO SE TRANSFIERE AL 2D (coincide con lo sellado, §3)

`-1.3936` es un **interpolante local de potencia** sobre D en unidades de x (1 ud = 20 celdas a h = 0.05), con residuo de ajuste 3.0 %; **no** es una ley de escala geometrica, y la propia acta del 1D lo declara. El pre-registro sellado ya lo prohibe (§3 y §7) y su gate **F11** ordena **re-medir** la ley en 2D. Esta adenda **COINCIDE**: se cita, no se re-escribe. Cualquier capa absorbente 2D de este frente se dimensiona con la ley **de su propia fuente**.

---

## §10. ESTADO, PROPIEDAD Y LO QUE ESTO NO ES

- Estado de **este** instrumento: **CRUDO REGISTRADO** (`RC_ESTRICTO = 0`). No es "gate validado": ese estado lo mueve el dueño.
- El Gate 2D-F1 aqui medido es de **instrumento** (esquema + dato, caso plano). **No es evidencia fisica.**
- **F8..F14** del pre-registro sellado siguen **sin crudo**. El paper no empieza hasta que tengan crudo registrado.
- `driver_rw_zerilli_1d.py` es READ-ONLY: no se toca.

---

## §11. ARBOL EN MOVIMIENTO (declarado, no adjudicado)

- HEAD avanzo durante la sesion: `4206b50` → `2eebc3b`.
- Otra mano trabaja **en vivo**: `sim/harness_multimodo_snr.py`, `sim/PREREGISTRO_EXTRACTOR_MULTIMODO_SNR_20261013.md`, `sim/ACTA_MP_M1_ARNES_MULTIMODO_SNR_20261013.md`, `sim/data/crudo_multimodo_mp_m1_20261013T191007Z.json` (19:10:07Z). No se toca nada de eso; no se adjudica.
- `gw-rw-zerilli` **si** es arbol git (el gate puede validar identidad). El workspace de direccion (`platino-labs`, donde vive `tools/gate_pre_escritura.sh`) **no** lo es ⇒ el gate se corre desde su ruta absoluta.

---

## §12. POSTURA DEL GATE SOBRE UN CRUDO VERBATIM (defecto de contrato declarado)

El crudo es la salida **verbatim** del instrumento: no se retipea y **no se le inyecta** una linea de huella. Consecuencia medida:

- huella `HUELLA-CRUDO-2D-F1-DOMINIO-20261013` en el crudo: `grep -c` = **0** ⇒ gate POST con esa huella devuelve **RC 12** (`DESFASE DE OBJETO: esperado AUSENTE, medido fcc6795ebc2fcb93d06f0e739c312a14980d9b08`). Ese 12 es un rojo sobre **mi declaracion** (declare AUSENTE un objeto que existe y sin huella), **no** sobre el objeto.
- gate POST honesto: huella que SI habita el crudo, `HUELLA-SONDA-2D-F1-DOMINIO-20261013` (`grep -c` = **1**) ⇒ **RC 11** (colision = fila escrita).

La identidad del crudo queda clavada por sha256 + bytes + el instante que el **mismo** imprimio.

---

## §13. SIGUIENTE PASO AUTORIZABLE

**Uno solo**: la **ratificacion del dueño** sobre la **§4** del pre-registro sellado. Sin ella **no** se escribe el driver 2D.

Cuando la haya, el driver implementa el **Gate 2D-F1** con el dominio de §7 y dimensiona su capa absorbente de perimetro con la **ley re-medida de su propia fuente** (gate F11) — nunca con `-1.3936` heredado.

---

## §14. FIGURAS SIN COMANDO

**Ninguna.** Cada cifra de esta adenda proviene de:

- `sim/data/crudo_2d_f1_dominio_20261013T192021Z.txt` (74 l · 4008 B · sha256 `5f74eb8023e8ce1ce9b5256db42f87e6b31e023d5e9e9ae04fbf6a770ee6910d`), producido por `sim/sonda_2d_f1_dominio.py --estricto` (sha256 `5f77b302d3b9f8bc00c40879e2432e52f29583b450c970e6bec0c82b34fe5165`);
- o de las actas citadas por su slug completo (`ACTA_REFLEXION_FRONTERA_SOMMERFELD_VS_PML_20261013.md` l.20/106/111/112 · `ADENDA_1_AL_ACTA_DE_REFLEXION_FRONTERA_SOMMERFELD_VS_PML_20261013.md` l.80), transcriptas en el pre-registro sellado l.28/50/53/77/86/100 — **citadas**, no re-medidas aqui.
