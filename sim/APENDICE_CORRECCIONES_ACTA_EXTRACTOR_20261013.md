# APÉNDICE DE CORRECCIONES AL ACTA DEL EXTRACTOR ESPECTRAL

**Huella de este apéndice:** HUELLA-APENDICE-CORRECCIONES-ACTA-EXTRACTOR-20261013
**Acta madre:** `sim/ACTA_EXTRACTOR_ESPECTRAL_CALIBRACION_20261013.md`
**Blob sellado de la madre:** `6bf81d8464261f92cec4c8792131df55a7e77b1a` (abreviado: `6bf81d84…`)
**Commit del sello:** `6d73a15` — **líneas:** 307 · **sha16:** `33c0768870dc7c42` · **bytes:** 20 319
**Ventana de medición (UTC):** `2026-10-13T17:45:22Z` (pre-vuelo) · `2026-10-13T17:45:29Z` (cadena de commits) · `2026-10-13T17:45:41Z` (líneas citadas)

## 0. Contrato de custodia y contrato de escritura

- **A2.1 pre-vuelo (corrido ANTES de escribir, no al cerrar):** `TARGET=sim/APENDICE_CORRECCIONES_ACTA_EXTRACTOR_20261013.md` · `BLOB_PRE=AUSENTE` · `LINEAS_PRE=0` · `HUELLA=HUELLA-APENDICE-CORRECCIONES-ACTA-EXTRACTOR-20261013` ⇒ **RC=10** (destino nuevo, cero colisión), medido a `17:45:22Z` con `existe_destino=NO` y `porcelain_destino=[]`.
- **La madre NO se muta.** Medido a `17:45:29Z`: `blob(HEAD:acta)=6bf81d8` · `blob(6d73a15:acta)=6bf81d8` · `blob(disco)=6bf81d8` · `porcelain(acta)=[]` ⇒ **byte-idéntica en las tres puntas; cero escrituras sobre ella.**
- **Motivo del apéndice:** la corrección métrica existía **sólo en la memoria volátil del chat**. En el repositorio los literales corregidos tenían **cero ocurrencias** (`2 de 3`=0 · `1.877080`=0 · `2.84`=0 · `1.418505`=0, medidos a `17:33:04Z`). Este archivo es su **primera casa en disco**. Un acta sellada jamás se parchea: toda corrección entra por apéndice.

## 1. Fe de erratas — línea 100 de la madre

**Texto vigente en la madre** (l.100, verbatim, 112 columnas de contenido; la línea **termina en «polos»** y el párrafo continúa en l.101):

```
  1e+05 de SNR ⇒ pendiente ≈ 1.0). **A 20 dB se pierde la mitad del objeto**: `n_recuperados = 1` (dos polos
```

**Defecto:** la frase «se pierde la mitad del objeto» **no nombra su denominador**, y su unidad adjetiva («la mitad») corresponde a un cociente distinto del que la propia línea imprime a continuación.

**Corrección asentada:** a 20 dB se pierden **2 de 3 polos** — es decir, **2/3 del objeto perdido**, no la mitad.

- **Denominador estricto: los 3 polos inyectados** (bloque sellado, `K = 3`).
- **Conteo medido en la madre:** la fila de 20 dB (l.97) imprime `n_recuperados = 1` ⇒ recuperados **1**, perdidos **3 − 1 = 2**.
- **Fila citada** (l.97, verbatim): `| 20 | 19.8947 | 7.2208e-02 | **1** | 1.0785e+00 | 1.5527 | 0.192560 |`
- **Control de la serie:** las celdas de 140 → 40 dB dan `n_recuperados = 3` (**3 de 3**) ⇒ el defecto es **propio de la celda de 20 dB**, no de la calibración entera.
- **El literal «la mitad» ocurre 1 vez en la madre** (l.100) ⇒ la errata es puntual y tiene una sola casa.

## 2. Tabla de discrepancias numéricas con denominador explícito

**UNIVERSO DECLARADO:** los dos estimadores monomodales —MPM con `K=1` y el ajuste paramétrico del driver— sobre la misma serie, contra la referencia analítica de Leaver (`l=2`, `n=0`). **MOTOR:** los crudos `sim/data/crudo_extractor_pase2_*.json` y la madre; más `grep -rlF` para fiscalizar cada literal. **UNIDAD:** desviación relativa adimensional. **VENTANA:** `2026-10-13T17:33Z`–`17:45Z` (UTC).

| Magnitud | Valor | Denominador declarado | Instrumento que la imprime |
|---|---|---|---|
| Desviación entre estimadores | `abs(s_MPM(K=1) − s_fit(driver)) / abs(s_MPM1) = 1.877080e-3` | `abs(s_MPM1)` — magnitud del polo monomodal del MPM | **NINGUNO** — `grep -rlF '1.877080' sim/data/*.json` = **0 archivos**; cifra **DERIVADA** |
| MPM(`K=1`) contra Leaver | `3.552e-2` | `abs(s_ref)` — polo de Leaver | la madre (literal `3.552` = **1** ocurrencia) |
| Ajuste del driver contra Leaver | `3.360e-2` | `abs(s_ref)` — polo de Leaver | la madre (literal `3.360` = **2** ocurrencias) |
| Margen a `K=3` contra el corte F8 | `Δs_rel = 1.418505e-3` | umbral sellado `F8 <= 0.05` | **NINGUNO** — `1.418505` = **0** ocurrencias en la madre; cifra **DERIVADA** |
| Consumo del umbral F8 | `2.84e-2` del umbral (**2.84 %** de `F8 <= 0.05`) | umbral sellado `F8 <= 0.05` | **NINGUNO** — `2.84` = **0** ocurrencias; **DERIVADA** de la fila anterior |

**Lectura, sin adjudicar:** los **dos estimadores monomodales convergen al mismo número sesgado** frente a Leaver (`3.552e-2` y `3.360e-2`), lo que es consistente con un sesgo **del instrumento monomodal**, no de uno de los dos caminos. Y el margen a `K=3` **no se compara contra el error de Leaver: se compara contra el umbral sellado F8**, del que consume exactamente **2.84 %**.

## 3. Orden de Richardson (ya presente en la madre, re-confirmado)

- `p = 2.0996` (caso RW) — el literal `2.0996` ocurre **1** vez en la madre.
- `p = 2.1087` (caso Zerilli) — el literal `2.1087` ocurre **1** vez en la madre.
- **Re-confirmado** por el commit `7f01938`: «F2 p=2.0996/2.1087 PASA abs(p-2)<=0.15». No es corrección: es **coincidencia**, y se asienta aquí para cerrar el arco de cifras.

## 4. Custodia: el árbol avanzó, el sello no

- **Punta del sello:** `6d73a15` (blob de la madre `6bf81d84…`).
- **HEAD medido a `17:45:29Z`:** `41b39ee`, **2 commits** por delante de `6d73a15`:
  - `7f01938` — «V2 crudos: F6_mallas (no-anidado=0 compartidos) + fisica (F2 p=2.0996/2.1087 PASA; F5 isoespectralidad desv=4.273e-3 PASA <=1e-2; F7 Leaver desv=3.360e-2 PASA <=5e-2) | driver blob 62931cf0».
  - `41b39ee` — «data(f4): crudo F4-frontera V2 = FALLA (der -21.68 dB / izq -19.10 dB vs umbral -40 dB); driver blob 62931cf0».
- **Ambos son crudos de otra mano** (F4-frontera, F6-mallas, física V2): **no tocan la madre ni el instrumento**.
- **Blobs sellados intactos:** madre `6bf81d84…` (idéntica en disco, en `6d73a15` y en HEAD) · instrumento `sim/extractor_polos_matrixpencil.py` blob `4fb04ab780acf4f7…` · driver `sim/driver_rw_zerilli_1d.py` blob `62931cf0…` (re-citado por los dos commits nuevos).
- ⇒ «sellado bajo `6d73a15`» queda **calificado**: el sello es del **acta** y del **instrumento**; la **punta del árbol** es `41b39ee`.

## 5. Puerta de este apéndice

- **Encabezados (gate estructural de un archivo de registro):** `^#+ ` = **7** (1 de nivel 1 + 6 de nivel 2). Se verifica por conteo al cerrar, no por lectura.
- **Signos monetarios:** **0**.
- **El acta madre permanece byte-idéntica:** este apéndice **no la parchea**; la errata vive aquí y la madre conserva su texto de `6bf81d84…`.
