# ERRATA 1 — A `sim/DECLARACION_F2_ARRANQUE_EXACTO_CRITERIO_PISO_20261013.md` (13-Oct-2026)

HUELLA-ERRATA-1-DECL-F2-IDENTIDAD-V2-V3-20261013

UNIVERSO DECLARADO: los tres estados del instrumento `arnes_richardson_2d_f2_{,_v2,_v3,_v4}*.py` en el arbol
de trabajo de `gw-rw-zerilli`, medidos con `wc -l -c`, `shasum -a 256`, `git hash-object`, `git ls-files`,
`git diff --numstat`, `git rev-parse HEAD:<ruta>` (TZ=UTC, 13-Oct-2026, despues de escribir la declaracion).
UNIDAD: lineas y bytes del archivo en disco; blobs de git (sha1) y sha256 del contenido.

## 1. Se RETRACTA la identidad v2 == v3

El §1 de la declaracion afirmo: «`v2.py` y `v3.py` son BYTE-IDENTICOS, sha256
`baa7b652fb6d16e26532644bdc22c72766ecbeacf57e3f21203c7998c50be347` en los dos, 779 l / 39887 B en los dos».
**Esa mitad es FALSA a la hora de esta errata.** Medido ahora:

| pieza | rastreada | l | B | sha256 | git blob (disco) | blob en HEAD | delta vs HEAD |
|---|---|---|---|---|---|---|---|
| `sim/arnes_richardson_2d_f2_v2.py` | no (`??`) | 779 | 39887 | `baa7b652fb6d16e26532644bdc22c72766ecbeacf57e3f21203c7998c50be347` | — | — | — |
| `sim/arnes_richardson_2d_f2_v3.py` | **si** | **800** | **42099** | `2efba187cbb6a03842c76ffa52190df127324bb736571eb5993647c6ffc65529` | `08adc845435f34a473d13c34bef3fea591356707` | `72844790ba3ef2184d941ed1202c84b88771276b` | **36 insertadas / 15 borradas** (net +21 l) |
| `sim/arnes_richardson_2d_f2_v4_arranque_exacto.py` | no (`??`) | 729 | 40920 | — | `e10a51dbeb0fa80bdbabeb5ffa7f166dcbad63e9` | — | — |

- ⇒ **No hay una pieza viva, hay TRES estados** (v2 779 · v3 800 · v4 729). Y el instrumento **v3 esta
  RASTREADO y SUCIO** (HEAD `72844790…` → disco `08adc845…`): lo que corre en el disco **no es lo que un clon
  recibe** — la clase ya pagada («lo que CORRE no es lo que un CLON recibe»).
- La identidad v2 == v3 **fue cierta por su instante y caduco mientras se citaba** (pieza en vuelo de otra
  mano). La cita vale por su hora; la identidad **se retracta**, no se re-mide hasta la proxima foto.
- Corolario de registro: mi apunte «v3 git hash-object `08adc845…`» y mi apunte «sha256 de v3 `baa7b652…`»
  **no pueden ser los dos ciertos del mismo objeto** (un archivo de 779 l no da el blob de un archivo de 800 l).
  Uno de los dos era caduco; el que manda es la medicion de arriba.

## 2. Lo que la errata NO toca

- **Los tres crudos no dependen de v3.** El campo `comando` de los tres nombra
  `sim/arnes_richardson_2d_f2_v2.py`, y el campo `arranque` dice
  `exacto: u^{-1} = u^0 + 0.5 dt^2 a(u^0), v = (u^0 - u^{-1})/dt`. La escalera, las cifras F2, C2, C3a, C3b,
  el piso y el rojo C6 **quedan como estan** (v2 = 779 l / `baa7b652…` es el que corrio).
- El defecto v1 sigue en `sim/arnes_richardson_2d_f2.py` (576 l / 28318 B / sha256
  `89b51857c76b918de0da23bd79e260f0239832f51793e1ed208cce8a329efaf6`, `M`), citado como `sha256_v1` en los crudos.

## 3. Por que la errata nace como pieza compañera y no como apendice

- El apendice sobre la declaracion se intentó con el gate previo en ruta absoluta:
  `gate_pre_escritura.sh <declaracion> 877e0079e76f8ced827d8bb0e7410df42c45f595 "<huella nueva>" 129`
  ⇒ **RC 13 `ESTADO SUCIO: … tiene modificaciones no adjudicadas`** ⇒ **fail-closed: no se escribe**.
- ⇒ La correccion **no se parchea ni se apenda en el cuerpo citado**: nace como **archivo compañero** nuevo
  (RC 10, autorizado) que **retracta por slug completo** `sim/DECLARACION_F2_ARRANQUE_EXACTO_CRITERIO_PISO_20261013.md`.
- Declarado, **no adjudicado**: que mano movio v3, cuando, y si su cambio incluye el arranque exacto.
  No se le adjudica merito ni defecto; no se corre v3; no se borra v4.
