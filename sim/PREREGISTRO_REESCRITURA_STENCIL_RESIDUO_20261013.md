# PRE-REGISTRO DEL FRENTE DE REESCRITURA FORMAL DE STENCILS (RESIDUO DE ECUACION MODIFICADA) — 2026-10-13

HUELLA-PREREGISTRO-REESCRITURA-STENCIL-RESIDUO-20261013

T_UTC_VENTANA: 2026-10-13T22:10:42Z (reloj UTC del turno de sellado; se re-sella al primer numero).

UNIVERSO DECLARADO: este documento (1 pieza, SIN RASTREAR hasta su commit) + el arbol git
`/Users/marlene/gw-rw-zerilli` (satelite independiente, SIN submodulos, SIN dependencia de `sfqed-paper`)
+ las piezas y crudos que se CITAN por ruta, tamano y blob.

MOTOR = algebra simbolica (`python3 -B`, sympy) para los momentos. NINGUNA cifra de este documento
viaja sin su linea de comando; las dos secciones con cifras (3 y 5) llevan su comando y su crudo.

UNIDAD = orden de h (entero) / linea / encabezado / blob. VENTANA = reloj UTC de la cabecera.

`.git` NO entra en el universo. Los 30 objetos sin rastrear del arbol NO entran y NO se adjudican.

---

## Seccion 0 · Contrato de destino (A2.1)

- UBICACION_REPO: `/Users/marlene/gw-rw-zerilli`
- HEAD en el sello: `f8b788cff91d844794cf36e8cbc18c10a22ab980` (`feat(sim): certificar Gate 2D-F2 en VERDE`)
- TARGET: `sim/PREREGISTRO_REESCRITURA_STENCIL_RESIDUO_20261013.md`
- BLOB_PRE: **AUSENTE** · LINEAS_PRE: **0**
- HUELLA DEL BLOB (fila unica de la cabecera): `HUELLA-PREREGISTRO-REESCRITURA-STENCIL-RESIDUO-20261013`
- GATE PRE (arnes `tools/gate_pre_escritura.sh` de `platino-labs`, corrida 2026-10-13T22:10:42Z):

  ```
  COLISION: sim/PREREGISTRO_REESCRITURA_STENCIL_RESIDUO_20261013.md no existe.
  PRE_RC=10
  ```

  RC 10 = objeto inexistente ⇒ **creacion autorizada**. Cero escrituras antes de esta corrida.
- GATE POST esperado: **RC 11** (la huella ya habita el destino ⇒ cumplimiento pasivo, cero escrituras nuevas).
- Contencion: este acta **no parchea** ninguna pieza sellada; solo escribe su propia fila. Frontera en la Seccion 7.

---

## Seccion 1 · Invariante de Ortogonalidad de Orden (advertencia del dueno — se incorpora al metodo)

**Enunciado.** El certificador de este frente opera sobre el espacio semantico de la **ecuacion modificada
espacial** (`D_x -> d_x`). Es **ciego por construccion** al integrador temporal, al numero de CFL y a la
simetria del dato inicial de Cauchy (`t = 0`).

**Forma algebraica (el por que, no la advertencia).** Sea el operador compuesto `C(dt,h) = T(dt) . S(h)`.
Su residuo respecto del exacto `T_ex . S_ex` es

```
R_C = T(dt) S(h) - T_ex S_ex
    = [T(dt) - T_ex] S(h) + T_ex [S(h) - S_ex]
    = R_T . S(h) + T_ex . R_S
```

con `R_S = S(h) - S_ex` (espacial, EL QUE ESTE FRENTE MIDE) y `R_T = T(dt) - T_ex` (temporal, FUERA).
El segundo sumando no es `R_S` solo: es `T_ex . R_S`, que contiene el **termino cruzado `R_T . R_S`**
(los dos factores multiplicados, `O(dt . h^p)`).

**Corolario que la advertencia exige.** El orden del compuesto **no se deriva** del orden de los factores:
`p_C != min(p_S, p_T)` en general, y **el termino cruzado no es visible desde ningun factor por separado**.
Certificar `R_S` **NO** certifica `R_C`.

**Que ve y que no ve este motor (declarado, no supuesto):**

| | el certificador de este frente |
|---|---|
| VE | los pesos del stencil, los momentos de Taylor, el orden algebraico local del operador espacial |
| NO VE | `dt`, CFL, la condicion inicial, la fase del esquema kick-drift, la estabilidad, la frontera |

**Relacion con Richardson.** El dictamen es **ortogonal**, no sustituto. Richardson audita la convergencia
**global** de la trayectoria en el plano `(dt, h)`; este motor audita el **orden algebraico local** del
operador espacial. La reescritura (E-graphs / saturacion de igualdades) es un **linter algebraico a priori**:
**no reemplaza a Richardson, lo PRECEDE**. Un VERDE de este motor no autoriza la Seccion 6.

---

## Seccion 2 · Objeto de analisis (alcance delimitado al stencil)

- **Identidad del objeto** (medida, 2026-10-13T22:10:06Z): `sim/driver_rw_zerilli_1d.py`
  `lines=708 bytes=33290 sha256=45e63b3803a51595 blob=d6b899c6d142254d mtime=2026-10-13T18:33:47Z`.
- **Casa**: `sim/driver_rw_zerilli_1d.py:218` (`def cubic_stencil(rs, x0):`), con el comentario
  `# Stencil de interpolacion cubica (Lagrange, 4 nodos) en un punto fisico fijo`. Uso: `:308`
  (`oidx, wobs = cubic_stencil(rs, obs_x)`).
- **Operador**: interpolacion de Lagrange de **4 nodos** (grado 3) evaluada en un punto fisico fijo `x0`.
- **Geometria del stencil (MEDIDA en el codigo, no supuesta)**: `j = searchsorted(rs, x0) - 1` con
  `j = clip(j, 0, n-4)` ⇒ el soporte es `{j, j+1, j+2, j+3}` y `x0` cae entre `x_j` y `x_{j+1}`.
  Con `x0 = x_j + s·h` se tiene `s in [0,1)`: el stencil es en general **UNILATERAL (sesgado hacia
  adelante)**, no centrado. `s in [0,1)` es **hecho del codigo**, no una eleccion de modelado.
- **QUEDA FUERA (declarado, no adjudicado)**: el integrador temporal (leapfrog escalonado) · la capa
  esponja y Mur-1 · el laplaciano y el potencial · el arnes 2D y el polar · la no linealidad · la
  condicion inicial · el propio **observador** `obs` (interpolar el observable es OTRO uso del mismo
  stencil: este frente certifica el **OPERADOR**, no el observable).
- **El stencil NO se edita.** Este frente solo CERTIFICA su orden. Cualquier reparacion exige orden aparte.

---

## Seccion 3 · Ecuacion modificada de `cubic_stencil` (formulacion matematica)

**Comando** (casa `sim/`, `python3 -B`):

```
python3 -B -c "
import sympy as sp
s=sp.symbols('s')
nodes=[0,1,2,3]
w=[sp.simplify(sp.prod([(s-b) for b in nodes if b!=a])/sp.prod([(a-b) for b in nodes if b!=a])) for a in nodes]
mu=lambda w,m: sp.simplify(sum(w[a]*nodes[a]**m for a in range(4)))
print('sum_w =', sp.simplify(sum(w)))
for a in range(4): print('w_%d ='%a, w[a])
for m in range(5): print('mu_%d ='%m, mu(w,m))
print('mu4_menos_s4 =', sp.simplify(mu(w,4)-s**4))
print('prod_s_menos_a =', sp.simplify(sp.prod([s-a for a in nodes])))
print('CHECK_mu4 =', sp.simplify((mu(w,4)-s**4)+sp.prod([s-a for a in nodes]))==0)
"
```

**Crudo** (2026-10-13T22:10:06Z):

```
sum_w = 1
w_0 = -(s-3)(s-2)(s-1)/6
w_1 =  s(s-3)(s-2)/2
w_2 = -s(s-3)(s-1)/2
w_3 =  s(s-2)(s-1)/6
mu_0 = 1
mu_1 = s
mu_2 = s**2
mu_3 = s**3
mu_4 = s(6 s^2 - 11 s + 6)
mu4_menos_s4 = -s (s-3) (s-2) (s-1)
prod_s_menos_a = s**4 - 6 s**3 + 11 s**2 - 6 s
CHECK_mu4 = True
```

**Sustitucion de Taylor.** Con `x0 = x_j + s·h` y `u` suave,

```
L_s[u](x_j) = sum_{a=0}^{3} w_a(s) u(x_j + a h)
u(x_j + a h) = sum_{m>=0} (a h)^m / m! . u^{(m)}(x_j)
=>  L_s[u](x_j) = sum_{m>=0} [ mu_m(s) / m! ] h^m u^{(m)}(x_j),   mu_m(s) = sum_a w_a(s) a^m
    u(x0)       = sum_{m>=0} [ s^m / m! ] h^m u^{(m)}(x_j)
```

**Ecuacion modificada (residuo local del operador espacial).**

```
R_s[u] := L_s[u](x_j) - u(x0) = sum_{m>=4} [ (mu_m(s) - s^m) / m! ] h^m u^{(m)}(x_j)
```

porque los momentos coinciden **EXACTAMENTE** hasta `m = 3` (medido: `mu_m = s^m` para `m = 0,1,2,3`).
El primer termino no nulo es `m = 4` y su coeficiente se factoriza:

```
R_s[u] = - [ s(s-1)(s-2)(s-3) / 24 ] h^4 u^{(4)}(x_j) + O(h^5)
```

**⇒ ORDEN NOMINAL `p = 4`.** Coeficiente lider `= - prod_{a=0}^{3}(s-a) / 24`.
Cross-check medido a `s = 1/2`: `coef_lider = 5/128` y `-prod/24 = 5/128` (**coinciden**).

**Anclas y bordes declarados.**
1. Ancla ya sellada, misma casa: `sim/PREREGISTRO_RICHARDSON_2D_F2_20261013.md:115` dice
   *"`p` mide el interpolador. El arnes debe imprimir el error de interpolacion medido (`cubic_stencil`, orden 4)"*
   ⇒ **COINCIDE**: `p = 4` es el mismo numero, obtenido por otra via (identidad simbolica vs. medicion ejecutada).
2. **Borde**: en `s = 0` y `s = 1` el producto `prod(s-a) = 0` ⇒ residuo nulo (interpolacion exacta en nodos).
   El orden 4 es generico para `s in (0,1)`; **NO se reclama orden 4 en `s` entero**.
3. **Advertencia de metro**: `p` mide el **OPERADOR** simbolico. El error espacial EJECUTADO en un arnes
   lleva ademas el error del dato y de la malla (el mismo aviso que F2 ya escribio en `:115`) ⇒ este frente
   no mide lo segundo.

---

## Seccion 4 · Contrato de aceptacion de orden (lo que el certificador debe emitir)

**ADAPTACION DECLARADA (no se copia la plantilla a ciegas).** La plantilla del dueno esta escrita para un
operador **DERIVADA** (termino de orden 0 `= 0·u`, orden 1 `= 1·u'`). El objeto de este frente es el
operador de **EVALUACION / INTERPOLACION** (la identidad `I`), no una derivada ⇒ el contrato se lee con su
propia convencion, y **el cambio se declara** (declarar la convencion es el acto que evita el error de conteo):

| orden | termino | valor exigido | causa de rechazo si no se cumple |
|---|---|---|---|
| 0 | `1·u` | **exactamente 1** (particion de la unidad) | `RECHAZO: NORMA_ROTA (sum w != 1)` |
| 1 | `h·u'` | **exactamente 0** | `RECHAZO: TERMINO_ESPURIO_O(h^1)` |
| 2 | `h^2·u''` | **exactamente 0** | `RECHAZO: TERMINO_ESPURIO_O(h^2)` |
| 3 | `h^3·u'''` | **exactamente 0** | `RECHAZO: TERMINO_ESPURIO_O(h^3)` |
| 4 | `h^4·u^(4)` | PRIMER termino no nulo, coeficiente `-prod(s-a)/24` | (aqui YA no hay rechazo: es el orden nominal) |

**Regla de la puerta.** "exactamente 0" significa **CERO SIMBOLICO** (`simplify(expr) == 0`), no "menor que
una tolerancia": una tolerancia aqui no mide nada (el objeto es algebraico). Un termino espurio no nulo ⇒ REVOCA.
Si el primer termino no nulo cae en `m < 4` ⇒ `RECHAZO: ORDEN_INFERIOR_AL_NOMINAL (orden_detectado = m, p = 4)`.
Si los ordenes 0..3 caen exactos y el primero no nulo es `m = 4` ⇒ `VERDE: ORDEN p = 4 CERTIFICADO (coef = -prod(s-a)/24)`.

**Unidad de la salida.** El certificador imprime el **PAR** `(orden | coeficiente lider)` **y la `s`** a la
que midio. Un veredicto sin su `s` **no es una medicion** (el coeficiente depende de `s`; el orden no).

---

## Seccion 5 · Control falsable obligatorio (must-fail)

**Contrato.** Un control positivo **no discriminante** no certifica nada. Este control **inyecta un termino
de orden inferior conocido** perturbando los pesos y el certificador **DEBE ENROJECER con causa tipada**.
**Si el control sembrado NO enrojece, el instrumento se declara INVALIDO** (fail-closed).

**Perturbacion.** `w -> w + eps·delta`, con `delta` **fijo antes de la primera cifra** y `eps = 1/1000`.
Comando: el mismo bloque de la Seccion 3 con `firma(nom, delta)`, que reporta `delta_mu_0..3` y el primer
orden `m` con `delta_mu_m != 0`.

**Crudo** (2026-10-13T22:10:22Z):

| control | delta | primer orden no nulo | causa tipada esperada |
|---|---|---|---|
| C0 (positivo, SIN perturbacion) | `(0,0,0,0)` | 4 (`ninguno < 5`) | `VERDE: ORDEN p = 4` |
| E1 DISIPATIVO (par) | `(1,-1,-1,1)` | **2** (`d2 = 1/250`) | `RECHAZO: RESIDUO_DISIPATIVO_DETECTADO (O(h^2) != 0)` |
| E2 DISPERSIVO | `(1,-3,3,-1)` | **3** (`d3 = -3/500`) | `RECHAZO: RESIDUO_DISPERSIVO_DETECTADO (O(h^3) != 0)` |
| E3 ADVECTIVO | `(1,0,0,-1)` | **1** (`d1 = -3/1000`) | `RECHAZO: RESIDUO_DE_ORDEN_INFERIOR_DETECTADO (O(h^1) != 0)` |

Crudo literal de la corrida:

```
C0 sin perturbacion          delta=(0,0,0,0)      delta_mu0=0 d1=0 d2=0 d3=0        primer_orden_no_nulo=ninguno<5
E1 disipativo (par)          delta=(1,-1,-1,1)    delta_mu0=0 d1=0 d2=1/250 d3=9/500 primer_orden_no_nulo=2
E2 dispersivo h^3            delta=(1,-3,3,-1)    delta_mu0=0 d1=0 d2=0 d3=-3/500    primer_orden_no_nulo=3
E3 advectivo h^1             delta=(1,0,0,-1)     delta_mu0=0 d1=-3/1000 d2=-9/1000 d3=-27/1000 primer_orden_no_nulo=1
```

**Lectura (los controles cubren las tres simetrias, no una sola).** `E1` es **par** respecto del centro
`c = 3/2` (`a -> 3-a` deja `delta` igual) ⇒ ensucia en `u''` (disipativo). `E2` cae en `h^3` ⇒ `u'''`
(dispersivo): **es el control que el dueno pidio** ("perturbar los pesos simetricos con `eps·h·u'''`") y su
firma medida es `d3 = -3/500` con primer orden no nulo `3`. `E3` es **impar** ⇒ `u'` (advectivo, error de
fase). Los tres violan la cadena de momentos **en el orden que su simetria declara**, y ninguno en otro.

**Frontera del control.** El must-fail prueba que **el METRO distingue orden 4 de orden < 4** sobre una
perturbacion conocida. **NO** prueba que el operador real tenga orden 4 — eso lo dice la Seccion 3, por
identidad simbolica. Los dos veredictos **no son el mismo metro**.

---

## Seccion 6 · PROHIBICION: consistencia de Cauchy sin integrador temporal acoplado

**Se prohibe** — y se deja escrito, no confiado a la memoria — extraer de este frente **cualquier**
afirmacion sobre:

1. **Consistencia respecto de la ecuacion de Cauchy** (que el esquema converja a la solucion del problema
   de valores iniciales);
2. **Aislamiento del error `O(dt)`** (la separacion del error temporal del espacial);
3. **Estabilidad, CFL o simetria del dato inicial** (`d_t Psi = 0`).

**Razon.** El motor es ciego por construccion a `dt` (Seccion 1) ⇒ su dictamen es un residuo **espacial
puro**. La consistencia de Cauchy exige el operador **COMPUESTO** y **su residuo no se factoriza**: el
termino cruzado `R_T . R_S = O(dt . h^p)` **no se ve desde ningun factor por separado**.

**Casa del precedente que este error ya cobro a mano** (citado por ruta, blob y linea, no de memoria):
`sim/arnes_aislamiento_piso_2d.py:54` (`blob 251a448805a9f892`, 593 lineas) —
*"El bucle es PATEAR-LUEGO-ARRASTRAR (kick-drift) con v escalonada en n-1/2: la inicializacion correcta"* —
y el commit **`bad0358`** (`frente 2D: Gate 2D-F1 VERDE ... Reparacion de una linea: v^{-1/2} en la
inicializacion del bucle kick-drift`). Ese hallazgo se obtuvo **A MANO**: este frente **NO reclama haberlo
producido**; lo **CITA** como el coste que motiva la separacion de planos.

**Enlace declarado.** El aislamiento `O(dt)` pertenece a `sim/arnes_aislamiento_piso_2d.py` + la escalera
de Richardson (`sim/arnes_richardson_2d_f2*.py`), **NO** a este motor. Los dos planos **no se suman**:
se declaran ortogonales.

---

## Seccion 7 · Frontera con lo ya sellado (no se renumera, no se parchea)

- `PREREGISTRO_RICHARDSON_2D_F2_20261013.md` (`blob c91d8447816b9373`, `sha256 f6effc452daea9dd`,
  `204` lineas) — se **cita**, no se edita. Sus anclas F2/F9/F11 quedan **intactas**.
- `PREREGISTRO_EXTRACTOR_POLOS_...` (2026-10-13) y el resto de pre-registros del dia — **no se renumeran**.
- Los **30** objetos sin rastrear del arbol (`git status --porcelain -uall | wc -l` = 30, 22:10:06Z)
  **no entran** al universo de este acta y **no se adjudican** (familia "el universo se movio mientras se mediu").
- Este acta **solo escribe su propia fila**. Ningun otro archivo se abre ni se muta.

---

## Seccion 8 · Pendiente: tupla A2.1 del certificador (a emitir por el dueno)

El **certificador** (pieza ejecutable: lee los pesos del stencil, computa `mu_m` por simbolico y emite el
par `(orden | coeficiente)` + la causa tipada) **NO se construye en este turno**. Espera su contrato:

```
TARGET      = sim/<nombre_del_certificador>.py
BLOB_PRE    = AUSENTE
LINEAS_PRE  = 0
HUELLA      = <fila unica del certificador>
```

Sin los cuatro parametros: **rechazo por defecto de contrato**, no se escribe (A2.1).

---

## Seccion 9 · Ratificacion (lo que requiere dictamen del dueno)

1. **Nombre y slug** del frente: *Reescritura formal de stencils (residuo de ecuacion modificada)*,
   `PREREGISTRO_REESCRITURA_STENCIL_RESIDUO_20261013.md`.
2. **La adaptacion declarada de la Seccion 4** (operador identidad: `1·u` / `0·u'` / `0·u''` / `0·u'''` /
   primer no nulo `O(h^4)`) en lugar de la plantilla de derivada (`0·u` / `1·u'`). Es la unica desviacion
   de la letra de la orden, y se declara.
3. **El juego de controles must-fail** con `eps = 1/1000` fijado antes de la primera cifra
   (`C0 / E1 / E2 / E3`), y `E2` como el control literal pedido.
4. **La prohibicion de la Seccion 6** (no se extrae consistencia de Cauchy sin integrador acoplado).
5. **La frontera de la Seccion 7** (no se renumera, no se parchea, 30 objetos sin adjudicar).

*Razonamiento declarado, para ratificacion. Cero escrituras fuera de esta fila.*
