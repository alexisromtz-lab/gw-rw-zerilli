# ERRATA 1 — PRE-REGISTRO GATE 2D-F3 (ZERILLI M>0)
HUELLA: HUELLA-ERRATA-1-PREREGISTRO-GATE-2D-F3-20261013

- **FECHA:** 2026-10-14T00:16:29Z (hora UTC real del acto; medida con TZ=UTC date -u).
- **MOTOR:** python3.14 + numpy (sin scipy, sin red, sin aleatoriedad, sin estado oculto; mismo argv ⇒ misma salida). Ninguna cifra de este acto proviene de un integrador.
- **CASA:** /Users/marlene/gw-rw-zerilli (carpeta sim/).
- **PADRE (append-only, NO se edita):** sim/PREREGISTRO_GATE_2D_F3_ZERILLI_CURVATURA_20261013.md · 365 l · 23787 B · sha256 b19176d9747d6f4ec982b0e38834a1d7a8a95868029c5a439e08fb31bd28149e · blob b43403a8b881a05adf24389b3cd9432446677865 · POST RC 11 a 2026-10-14T00:09:21Z.
- **ORDEN:** «DICTAMEN DE DIRECCIÓN: ADJUDICACIÓN DE DEFECTOS D1–D5 EN PRE-REGISTRO GATE 2D-F3». Adenda breve que asienta las cinco resoluciones vinculantes antes de la tupla del arnés numérico.
- **ORDEN A2.1 (verbatim):**
  - TARGET: sim/ERRATA_1_PREREGISTRO_GATE_2D_F3_20261013.md
  - BLOB_PRE: NO_EXISTE_PRE10
  - HUELLA: HUELLA-ERRATA-1-PREREGISTRO-GATE-2D-F3-20261013
  - LINEAS_PRE: 0
  - RC esperado: 10 (AUTORIZACIÓN DE CREACIÓN)
- **GATE PRE (verbatim):** bash /Users/marlene/platino-labs/tools/gate_pre_escritura.sh /Users/marlene/gw-rw-zerilli/sim/ERRATA_1_PREREGISTRO_GATE_2D_F3_20261013.md NO_EXISTE_PRE10 HUELLA-ERRATA-1-PREREGISTRO-GATE-2D-F3-20261013 0 ⇒ COLISION: ... no existe. · RC_GATE_PRE=10 a 2026-10-14T00:15:30Z.
- **ESTADO:** ADENDA SELLADA AL ESCRIBIR. Cero código numérico. Cinco resoluciones asentadas (§R1–§R5). Pausa de código mantenida hasta que esta errata quede sellada en Git.

## UNIVERSO DECLARADO
UNIVERSO DECLARADO: este acto (creación), leído contra el padre sim/PREREGISTRO_GATE_2D_F3_ZERILLI_CURVATURA_20261013.md (365 l · blob b43403a8…). Ninguna cifra del arnés (que no existe) entra: las cifras de §F se miden en este acto; las del padre se citan con su hora y no se re-miden. Este acto NO reescribe el padre (§B–§H del padre quedan como están).

## §0. Objeto y lugar del acto
No re-mide el objeto del padre ni adjudica física nueva: asienta la resolución del dueño para cada defecto §C-Dn del padre y declara —donde la hay— la divergencia entre la resolución y la fórmula congelada en el padre. Donde §R difiera de §B del padre, manda §R.

## §R1. D1 — Acoplamiento λ (ℓ = 2)
- Resolución (vinculante): λ = 2 estricto, por la definición λ = ½(ℓ−1)(ℓ+2) = ½(1)(4) = 2. El «λ = 3» del dictado anterior fue desliz aritmético.
- Cifra (medida, §F): λ = 2 · 2(λ+1) = 6 · ℓ(ℓ+1) = 6 ⇒ coinciden, condición de la reducción plana exacta (C0).
- Efecto sobre el padre: el padre ya tomó λ=2 (§B.3, corrección de oído declarada). Sin divergencia: la resolución confirma el padre.

## §R2. D2 — Potencial 2D: curvatura neta U(r*)
- Resolución (vinculante): el operador diagonal 2D es U(r) = V_Zerilli(r) − (1 − 2M/r)·ℓ(ℓ+1)/r², con ℓ = 2; por construcción lim_{M→0} U(r) ≡ 0.0.
- Fundamento asentado: en (r*, θ) el operador −(1/r²)L̂² ya inyecta la barrera ℓ(ℓ+1)/r² por modo angular; inyectar V_Z en bruto la duplicaría en M = 0.
- DIVERGENCIA DECLARADA (corrige el padre §B.3): el padre congeló U(r) = V_Z(r) − ℓ(ℓ+1)/r² SIN el factor métrico (1 − 2M/r). La resolución lo lleva. En M = 0 las dos formas coinciden (f = 1); en M > 0 difieren en (2M/r)·ℓ(ℓ+1)/r².
- Cifra (medida, §F): con 2M = 3.0 (M = 1.5), la diferencia máxima contra la forma del padre sobre r ∈ [4, 90] es max|(2M/r)·6/r²| = 0.281250 — mismo orden que U mismo ⇒ la corrección no es cosmética.
- Nota de convención: en un potencial RW/Zerilli la barrera vive dentro de V_Z como f·ℓ(ℓ+1)/r²; por eso el operador angular explícito carga f para no duplicarla. Se asienta; no se adjudica más.

## §R3. D3 — Escala de masa y ubicación del pico
- Resolución (vinculante): se fija 2M = 3.0 (M = 1.5).
- Fundamento asentado: con la malla sellada en F11 (r*_min = 2.0), 2M = 1.0 deja el pico de V_Z en r* ≈ 0.95, fuera del dominio computable (padre §C-D3: déficit −1.049542). Con 2M = 3.0 el pico escala dentro del interior libre y no altera los anchos de esponja de F11 (L = 24.0).
- Cifra (derivada, §F): ley de escala medida en el padre r*_pico(2M) = 0.950458302187064 × (2M); a 2M = 3.0 ⇒ r*_pico = 2.851374906561190 ∈ [2.0, 98.0], margen sobre el borde interno 0.851374906561190.
- Efecto sobre el padre: supersede la elección in-situ de §B.1 (2M = 1.0) y la escalera de masas de §C-D3. La geometría de esponja (L = 24.0 · ancho 96.0 · r*_min 2.0 · r*_max 98.0) no cambia.
- Consecuencia declarada (trampa §B.2 del padre): ahora 4M = 6.0 > r*_min = 2.0 ⇒ en todo el dominio útil falla la contracción del punto fijo (g'(r) = 2M/(r−2M) < 1 ⇔ r* > 4M); la inversa r(r*) exige Lambert W₀ / Newton amortiguado en todo el rango (antes era un borde; ahora es el régimen).

## §R4. D4 — Metro para la localización del pico (C1)
- Resolución (vinculante): C1 se bifurca:
  - C1a (analítico continuo): raíz de dV_Z/dr* = 0 por Newton/Brent con tolerancia ≤ 1e−12.
  - C1b (consistencia de rejilla): |r*_grid_max − r*_teorico| ≤ ½·Δr*.
- Fundamento asentado: un argmax de rejilla no alcanza 1e−12 (Δr* ~ 2e−5). El padre midió |r*_grid − r*_raiz| = 1.943e-05 con paso de sonda 1.9667e-05 ⇒ el residuo medía el metro, no el objeto.
- Efecto sobre el padre: corrige el banco §D-D4 (C1 único con tolerancia 1e−12 ⇒ inalcanzable). Reparto: C1a juzga la raíz; C1b juzga la rejilla. El RC es condición necesaria; la causa impresa distingue cuál falló.

## §R5. D5 — Dato de C2 (interacción con la curvatura)
- Resolución (vinculante): C2 usa un paquete con componente incidente hacia la barrera, colocado en r* = 10.0 con reposo inicial (v⁰ = 0); el frente entrante colisiona con U(r*) y el saliente alcanza la capa F11.
- Fundamento asentado: el dato del padre, puramente saliente y centrado en p_efectivo = 50.12532637075718 (σ = 2.0), viaja directo a la esponja: sobre su soporte |U| ≤ 3.5e−5 ⇒ no toca el potencial y mide la capa, no la curvatura (C2 vacuo).
- Efecto sobre el padre: sustituye el dato heredado de F11 para el caso C2. Declarado; no se repara en el padre (append-only).

## §R6. Consecuencias declaradas sobre el futuro arnés (no ejecutadas)
- Dato con contenido angular ℓ=2: debe portar L̂²Ψ = 6Ψ (el dato de F11 era θ-independiente: C6 variacion_theta_max = 0.0).
- C9: se mantiene la propuesta del padre — round-trip |r*(r(r*)) − r*| ≤ 1e−13 sobre [2.0, 98.0]; el padre midió 1.421e-14.
- Malla sellada (nr0, hr, dt, CFL, nsteps): no se decide aquí. r* es la misma coordenada y la esponja no cambia; su re-chequeo pertenece a la tupla del arnés.
- Cero código numérico: esta errata no escribe ni corre integrador alguno.

## §F. Figuras selladas por este acto
UNIVERSO DECLARADO: rejillas analíticas — r ∈ [2.0, 98.0] (M = 0) y r ∈ [4.0, 90.0] (2M = 3.0; sin horizonte: r > 3.0). Sin integrador. Hora de la medida: 2026-10-14T00:15:36Z.

Comando (reproducible, sin escribir .pyc):
    python3 -B - <<'PY'
    import numpy as np
    l=2; lam=(l-1)*(l+2)/2
    print("lambda=%g  2(lam+1)=%g  l(l+1)=%g"%(lam,2*(lam+1),l*(l+1)))
    def VZ(r,M):
        num=2*lam**2*(lam+1)*r**3+6*lam**2*M*r**2+18*lam*M**2*r+18*M**3
        den=r**3*(lam*r+3*M)**2
        return (1-2*M/r)*num/den
    r0=np.linspace(2.0,98.0,400001)
    print("max|U(M=0)| = %.6e"%np.max(np.abs(VZ(r0,0.0)-6/r0**2)))
    M=1.5; r1=np.linspace(4.0,90.0,400001)
    print("max_delta_D2(2M=3.0) = %.6f"%np.max(np.abs((2*M/r1)*6/r1**2)))
    print("r*_pico(2M=3.0) = %.15g"%(0.950458302187064*3.0))
    print("4M = %g   r*_min = 2.0"%(4*M))
    PY
Salida (verbatim):
    lambda=2  2(lam+1)=6  l(l+1)=6
    max|U(M=0)| = 4.440892e-16
    max_delta_D2(2M=3.0) = 0.281250
    r*_pico(2M=3.0) = 2.85137490656119
    4M = 6   r*_min = 2.0

Lectura: max|U(M=0)| = 4.440892e-16 es el cero de máquina de la resta 6/r² − 6/r² ⇒ U(M=0) ≡ 0 a precisión IEEE-754; NO es un cero exacto y se declara como tal.

## §G. Gate PRE (registro)
- Tupla A2.1 (arriba) · invocación absoluta (arriba) · RC_GATE_PRE = 10 a 2026-10-14T00:15:30Z.
- POST (posterior a la escritura) esperado RC 11 (la huella ya habita el destino) = fila escrita; si diera 12, se declara DESINCRONIZADO y no se re-escribe.

## §H. Alcance
Cero código numérico. Nada calculado sobre malla curvada. El arnés sim/arnes_zerilli_curvatura_2d_f3.py queda bloqueado hasta la tupla A2.1 del dueño. Pestaña en reposo pasivo.
