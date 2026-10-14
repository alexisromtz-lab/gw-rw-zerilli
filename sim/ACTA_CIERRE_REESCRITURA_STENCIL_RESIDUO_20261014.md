# ACTA DE CIERRE DEL FRENTE DE REESCRITURA FORMAL DE STENCILS (RESIDUO DE ECUACION MODIFICADA) — LINEA A

HUELLA-ACTA-CIERRE-REESCRITURA-STENCIL-20261014

- Fecha de cierre: 2026-10-14
- Hora de la ultima medicion que sostiene esta acta: 2026-10-14T01:09:24Z
- Casa: `gw-rw-zerilli/sim/`
- Modo de cierre: **CERRADO POR COLISION** (cumplimiento pasivo A2.1, cero escrituras duplicadas)
- Cierra: el frente de reescritura formal de stencils (residuo de ecuacion modificada), abierto en `sim/PREREGISTRO_REESCRITURA_STENCIL_RESIDUO_20261013.md`

UNIVERSO DECLARADO: 1 pieza (el certificador citado en la Seccion 3) + 1 acta de pre-registro + su crudo de ejecucion; casa = `gw-rw-zerilli/sim/`; motor = `python3 -B` 3.14.7 + `sympy` 1.14.0. Toda cifra de esta acta se mide con comando sobre ese universo y trae su hora.

---

## Seccion 0 · Contrato de destino (A2.1) de esta misma acta

```
TARGET      : sim/ACTA_CIERRE_REESCRITURA_STENCIL_RESIDUO_20261014.md
BLOB_PRE    : NO_EXISTE_PRE10
HUELLA      : HUELLA-ACTA-CIERRE-REESCRITURA-STENCIL-20261014
LINEAS_PRE  : 0
RC esperado : 10 (AUTORIZACION DE CREACION — objetivo nuevo)
```

Crudo literal del gate PRE, corrido con TARGET ABSOLUTO antes de cualquier escritura:

```
COLISION: /Users/marlene/gw-rw-zerilli/sim/ACTA_CIERRE_REESCRITURA_STENCIL_RESIDUO_20261014.md no existe.
PRE_RC=10
```

Sonda de ausencia companera (antes de escribir): `huella_en_repo=0` · `acta_existe=NO`.
GATE POST esperado: **RC 11** (la huella ya habita el destino ⇒ cumplimiento pasivo, cero escrituras nuevas).
Nota de orden: esta acta no lleva signo monetario en su texto (`dolar_en_acta=0`).

---

## Seccion 1 · Resolucion por COLISION

**Resultado: el frente se cierra sin una sola linea escrita por esta mano para el certificador.**

Secuencia medida:

1. Sonda de ausencia sobre el objetivo del certificador: `2026-10-13T22:59:41Z` ⇒ el artefacto **no existia**.
2. Gate A2.1 PRE sobre ese mismo objetivo, con TARGET absoluto: `2026-10-13T23:59:24Z`.
3. El gate devolvio **RC 11**, no RC 10. La condicion de huella se disparo antes que cualquier otra: `la huella '<H>' ya habita en <T> ⇒ Abortando escritura`.

⇒ Entre la sonda de ausencia y el gate cupo **otra mano**. La pieza fue escrita, y sellada en git (Seccion 2), dentro de esa ventana.

**Consecuencia ejecutada:** cero escrituras. No se reescribio el certificador, no se renumero, no se creo un gemelo, no se copio a `/tmp`. El cierre del frente es **pasivo**: se reconoce el objeto existente y se lo audita contra el contrato ya ratificado, en vez de duplicarlo.

**Leccion que el caso paga (se declara, no se adjudica):** la sonda de ausencia **caduca**. "Medir que la fila no exista" y "escribir" son dos instantes distintos, y en medio cabe otra mano. Lo que convierte una sonda caduca en comprobacion es el **gate**: su RC 11 cerro el frente en lugar de duplicarlo.

---

## Seccion 2 · Identidad del commit base

```
commit      : b01076890c07040e53184cb2f380b7adcc52fafc
padre       : f9745784ec88c4b5f94ec4e4b36ed65d9dd1b67a
autor       : Jose Alexis Roman Martinez (identidad git de la casa)
fecha       : Tue Oct 13 17:22:12 2026 -0600
asunto      : feat(symbolic): certificar Linea A (stencils por Taylor, banco must-fail 4/4 discriminado)
estadistica : 2 files changed, 644 insertions(+)
```

Archivos del commit:

```
sim/PREREGISTRO_REESCRITURA_STENCIL_RESIDUO_20261013.md | 303 ++++++++++++++++++
sim/certificador_reescritura_stencil_residuo.py         | 341 +++++++++++++++++++++
```

Lectura del acto: el pre-registro (303 lineas) y el certificador (341 lineas) fueron **sellados en un solo commit** (303 + 341 = 644). El artefacto no nacio suelto: nacio con su contrato de aceptacion ya escrito.

---

## Seccion 3 · Identidad del artefacto

`sim/certificador_reescritura_stencil_residuo.py`

```
lineas            : 341
bytes             : 13623
sha256            : d6eacf02a071e24f8ed523367b7294f75955dd9b774f635ce333d433c6f670e0
blob (disco)      : b647d613f1d6c5550e99cabda16206160be2749a
blob (HEAD)       : b647d613f1d6c5550e99cabda16206160be2749a
mtime (UTC)       : 2026-10-13T23:05:19Z
dolar_en_pieza    : 0
imports           : 5  (argparse, json, sys, sympy, __future__)
escritura_a_disco : 0  (solo `print` a stdout)
contacto_arnes    : 2 lineas, ambas comentario (l.7 y l.35; la l.35 declara "CERO CONTACTO")
```

Consecuencia de identidad: **blob de disco == blob de HEAD** ⇒ la pieza sellada y la pieza en disco son el mismo objeto. No hay deriva entre el commit y el disco.

Trampa del propio metro, declarada: un contador con el patron `json\.dump` devuelve **2** sobre esta pieza, y las dos son `json.dumps` — el serializador a stdout, no una escritura. Es la familia "el cero puede ser del metro": aqui el falso positivo tambien lo era. Contado con el patron anclado, `escritura_a_disco = 0`.

Pieza vecina citada (no editada, ver Seccion 6):

```
sim/PREREGISTRO_REESCRITURA_STENCIL_RESIDUO_20261013.md
lineas: 303 · bytes: 15911
sha256: 909d971b600b2d09...
blob (disco): 116d679a6ca5eb2fe67ae34fd0913b9d07ac26f5
blob (HEAD) : 116d679a6ca5eb2fe67ae34fd0913b9d07ac26f5
```

---

## Seccion 4 · Vector de falsacion

Modo `--must-fail`, `eps = 1/1000` congelado **antes** de la primera cifra.

```
VECTOR RC = C0:0 E1:2 E2:3 E3:1
vector esperado = C0:0 E1:2 E2:3 E3:1 (pre-registrado)
BANCO OK
banco_ok = True
```

Causas tipadas, una por control rechazado:

```
E1  rc 2  RESIDUO_DISIPATIVO_DETECTADO              (O(h^2) != 0)
E2  rc 3  RESIDUO_DISPERSIVO_DETECTADO              (O(h^3) != 0)
E3  rc 1  RESIDUO_DE_ORDEN_INFERIOR_DETECTADO       (O(h^1) != 0)
C0  rc 0  VERDE: ORDEN p = 4 CERTIFICADO            (coef = -prod(s-a)/24)
```

Lectura del vector: los cuatro controles caen en **cuatro valores distintos** (`0, 2, 3, 1`) y el vector medido **coincide** con el pre-registrado. Un banco que devolviera el mismo codigo para todos los controles no discriminaria; este discrimina por clase de residuo, no por "hay residuo".

Precision de unidad, para no confundir dos cifras: `RC_MUSTFAIL = 0` es el **RC del banco** (el banco corrio y paso); el **discriminante** vive en la columna `rc` de cada control. Son dos numeros distintos del mismo crudo y ninguno sustituye al otro.

JSON del modo base (recorte literal):

```
rc = 0
adaptacion_declarada = operador IDENTIDAD (1*u / 0*u' / 0*u'' / 0*u''')
par_simbolico = [4, "s*(-s**3 + 6*s**2 - 11*s + 6)/24"]
coef_lider_en_s = "5/128"   (s_materializa = 1/2)
coincide_forma_cerrada = true
cross_check_sustrato = true
```

---

## Seccion 5 · Crudo literal (modo base)

```
UNIVERSO DECLARADO: operador I = cubic_stencil (Lagrange, 4 nodos 0..3) sobre u suave; malla UNIFORME (h constante); s simbolica generica; eps_must_fail = 1/1000; controles = {C0, E1, E2, E3}; casa = sim/; motor = python3 -B + sympy.
huella = HUELLA-CERTIFICADOR-REESCRITURA-STENCIL-RESIDUO-20261013
modo = base (identidad simbolica, s generica)
premisa = malla UNIFORME (h constante entre los 4 nodos)
sum_w = 1
mu_0 - s^0 = 0
mu_1 - s^1 = 0
mu_2 - s^2 = 0
mu_3 - s^3 = 0
orden_detectado = 4
PAR (orden | coef_lider) = (4 | s*(-s**3 + 6*s**2 - 11*s + 6)/24)   [identidad simbolica en s]
coef_esperado_forma_cerrada = -s*(s - 3)*(s - 2)*(s - 1)/24
coincide_forma_cerrada = True
PAR en s = 1/2  = (4 | 5/128)
cross_check_sustrato = True
rc = 0
causa = VERDE: ORDEN p = 4 CERTIFICADO (coef = -prod(s-a)/24)
```

```
RC_BASE=0
```

## Seccion 5b · Crudo literal (modo must-fail)

```
UNIVERSO DECLARADO: operador I = cubic_stencil (Lagrange, 4 nodos 0..3) sobre u suave; malla UNIFORME (h constante); s simbolica generica; eps_must_fail = 1/1000; controles = {C0, E1, E2, E3}; casa = sim/; motor = python3 -B + sympy.
huella = HUELLA-CERTIFICADOR-REESCRITURA-STENCIL-RESIDUO-20261013
modo = must-fail (eps = 1/1000, congelado antes de la primera cifra)
control  delta                         rc  primer_orden_no_nulo  causa
C0       [0, 0, 0, 0]                  0   ninguno<5             VERDE: ORDEN p = 4 CERTIFICADO (coef = -prod(s-a)/24)
E1       [1, -1, -1, 1]                2   2                     RECHAZO: RESIDUO_DISIPATIVO_DETECTADO (O(h^2) != 0)
E2       [1, -3, 3, -1]                3   3                     RECHAZO: RESIDUO_DISPERSIVO_DETECTADO (O(h^3) != 0)
E3       [1, 0, 0, -1]                 1   1                     RECHAZO: RESIDUO_DE_ORDEN_INFERIOR_DETECTADO (O(h^1) != 0)
firmas (eps * sum_a delta_a a^m):
  C0 d0=0 d1=0 d2=0 d3=0
  E1 d0=0 d1=0 d2=1/250 d3=9/500
  E2 d0=0 d1=0 d2=0 d3=-3/500
  E3 d0=0 d1=-3/1000 d2=-9/1000 d3=-27/1000
VECTOR RC = C0:0 E1:2 E2:3 E3:1
vector esperado = C0:0 E1:2 E2:3 E3:1 (pre-registrado)
BANCO OK: el metro distingue orden 4 de orden < 4, con causa tipada en los 4 casos.
```

```
RC_MUSTFAIL=0
```

Declaracion de procedencia: las dos lineas `RC_BASE=0` y `RC_MUSTFAIL=0` son del **arnes de invocacion** (el shell), no del programa; el programa no imprime su propio RC. Se citan con esa marca para que ninguna de las dos se lea como salida del certificador.

---

## Seccion 6 · Declaracion de estado

**Linea A: formalmente CONCLUIDA.** El objeto de analisis (`cubic_stencil`, Lagrange de 4 nodos) quedo certificado como **orden p = 4** con forma cerrada del coeficiente lider y con un banco must-fail que **discrimina** — no que pasa.

Reposicion de premisas caducas. El pre-registro sellado se **cita, no se edita** (esta en git, blob `116d679a6ca5eb2f`); lo que estaba caduco en el lo repone esta acta:

- **Seccion 0** del pre-registro (l.20) — contrato de destino A2.1 de **aquel** documento: declaraba `BLOB_PRE: AUSENTE` y `LINEAS_PRE: 0`, y su POST esperaba RC 11. **Caduco por consumido**: el documento existe, su huella habita en el, y ambos valores ya no describen ningun estado vivo. Estado hoy: cumplido.
- **Seccion 8** del pre-registro (l.275) — "Pendiente: tupla A2.1 del certificador (a emitir por el dueno)". **Caduco por satisfecho**: la tupla dejo de ser un pendiente en el instante en que el certificador entro sellado en `b010768` (Seccion 2), con las 341 lineas y el blob `b647d613f1d6c555`. Estado hoy: no hay pendiente.

Regla aplicada: la pieza vieja **no se parchea jamas**; recibe apendice. Esta acta es ese apendice, en archivo propio.

---

## Seccion 7 · Frontera y prohibiciones vigentes

- **VETO ESTRICTO sobre Richardson 2D-F2.** `sim/arnes_richardson_2d_f2.py` permanece en ` M` inerte como testigo de fondo. No se limpia, no se adjudica. Medido hoy: `32 14 sim/arnes_richardson_2d_f2.py` (numstat, `+32 -14`). **Cero acciones.**
- **Los 29 objetos no rastreados: intactos.** Cero de ellos fue tocado, movido ni borrado por este cierre.
- **El ciclo de curvatura F3 NO ha concluido** (esto es lo que manda la pausa). Medido hoy `2026-10-14T01:08:31Z`: `sim/arnes_zerilli_curvatura_2d_f3.py` tiene blob HEAD `fa536467da94830360445ebaf54292166b70d95a` contra blob de disco `c3348c5598869c82f6fac0ea7a12cc96486b8430`, con **1011** lineas (`+3 -1` respecto de su sello) ⇒ **otra mano esta escribiendo en el ahora mismo**. Bajo el veto vigente: **no se toca**.
- **El gate de pre-vuelo: declarado, no reparado.** Su trampa de `TARGET` relativo (que produce RC 128 y enmascara las condiciones 3–5) sigue en pie a proposito, como frontera declarada.
- Atribucion que **no** debe arrastrarse: la reparacion de una linea del arnes de curvatura pertenece a `bad0358`, **nunca** a `f8b788c`.

---

## Seccion 8 · Ratificacion (lo que requiere dictamen del dueno)

1. Se ratifica el cierre de Linea A por **colision**, con cero escrituras duplicadas.
2. Se ratifica `b010768` como **commit base** del frente (2 archivos, 644 inserciones, padre `f974578`).
3. Se ratifica el blob `b647d613f1d6c5550e99cabda16206160be2749a` como **identidad congelada** del certificador.
4. Se ratifica el vector `[C0: 0, E1: 2, E2: 3, E3: 1]` con `banco_ok = True` como **vector de falsacion** del frente.
5. Se ratifica la reposicion de las premisas caducas (Seccion 0 y Seccion 8 del pre-registro) **por apendice**, sin editar la pieza sellada.
6. Se declara abierta la **PAUSA DE CUSTODIA DEFINITIVA** en espera de la evolucion de F3.

HUELLA-ACTA-CIERRE-REESCRITURA-STENCIL-20261014
