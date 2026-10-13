# PRE-REGISTRO SELLADO DEL BANCO 1D RW/ZERILLI (SCHWARZSCHILD NO ROTANTE) — 2026-10-13

HUELLA: HUELLA-BANCO-1D-RW-ZERILLI-SCHWARZSCHILD-NO-ROTANTE-20261013

T_UTC_VENTANA: 2026-10-13T09:59:20Z (reloj UTC del turno de sellado; se re-sella al primer número).

UNIVERSO DECLARADO: este documento (1 pieza) + el contrato de destino A2.1 + las dos precisiones ratificadas por el dueño (2026-10-13). MOTOR = ninguno: documento de sellado, las cifras se fijan por contrato, no por corrida. UNIDAD = linea / encabezado / umbral adimensional. VENTANA = reloj UTC de la cabecera.

## §0 · Contrato de destino (A2.1)

- UBICACIÓN REPO: /Users/marlene/gw-rw-zerilli (satélite independiente; SIN submódulos; SIN dependencia de sfqed-paper).
- TARGET: /Users/marlene/gw-rw-zerilli/sim/PREREGISTRO_RW_ZERILLI_20261013.md
- BLOB_PRE: AUSENTE
- LINEAS_PRE: 0
- HUELLA: la fila única de la cabecera (HUELLA-BANCO-1D-RW-ZERILLI-SCHWARZSCHILD-NO-ROTANTE-20261013).
- GATE: RC 10 (destino nuevo sin colisión) → ESCRIBIR → RC 11 (la huella ya habita el destino).
- Condición de contención estricta: repositorio git limpio (git init) antes del gate; PROHIBIDO escribir sim/driver_rw_zerilli_1d.py antes de sellar ESTE pre-registro.

## §1 · Alcance y exclusiones

- Dentro: métrica de Schwarzschild NO rotante, masa M, índice multipolar l (paridad impar de Regge-Wheeler y paridad par de Zerilli), una dimensión radial en la coordenada de tortuga.
- Fuera (AJENO, no se reclama): la detección por LIGO/Virgo opera sobre el IMF no lineal 3+1 de binarias en coalescencia y sobre el ringdown de un agujero negro de Kerr; nada de eso se mide aquí.
- Fuera (trabajo futuro): Kerr exige la ecuación de Teukolsky con armónicos esferoidales; no entra en este banco 1D.

## §2 · Las dos precisiones ratificadas (dueño, 2026-10-13)

1. Klein-Gordon escalar, no Maxwell. La ecuación maestra en tortuga

   ∂²t Ψ = ∂²r* Ψ − V(r) Ψ

   es una onda escalar DISPERSIVA por el potencial V. NO hay ligadura dinámica que preservar (contraste con la divergencia nula del campo magnético del banco FDTD). No se hereda la estructura simpléctica involutiva de Yee. Se hereda ÚNICAMENTE: (a) el integrador hiperbólico leapfrog, (b) las condiciones absorbentes a ambos extremos, (c) el análisis de estabilidad CFL bajo potencial acotado.

2. Doble control desacoplado. La isospectralidad de Darboux se clasifica estrictamente como CONTROL INTERNO: RW idéntico a Zerilli certifica que el resolvedor numérico NO sesga la paridad. El ajuste contra los modos cuasinormales de Leaver (M·omega ≈ 0.37367 − 0.08896 i para l = 2, n = 0) se clasifica como CONTROL EXTERNO, valor de referencia citado, no autogenerado.

## §3 · Ecuación maestra, potenciales y asintótica

- Tortuga: r* = r + 2M·ln(r/(2M) − 1), con r* tendiendo a menos infinito en el horizonte (r tendiendo a 2M) y a más infinito en el infinito espacial (r tendiendo a infinito).
- Potencial de Regge-Wheeler (paridad impar):
  V_RW(r) = (1 − 2M/r)·[ l(l+1)/r² − 6M/r³ ].
- Potencial de Zerilli (paridad par), con lambda = (l−1)(l+2)/2:
  V_Z(r) = (1 − 2M/r)·[ 2·lambda²·(lambda+1)·r³ + 6·lambda²·M·r² + 18·lambda·M²·r + 18·M³ ] / [ r³ · (lambda·r + 3M)² ].
- Isospectralidad de Darboux: para el mismo l, V_RW y V_Z comparten el MISMO espectro de modos cuasinormales (transformación de Darboux de primer orden).
- Asintótica: V tiende a 0 en ambos extremos (dos zonas de onda). Condición de radiación (convención declarada): saliente en el extremo del infinito espacial, ENTRANTE en el extremo del horizonte. De modo que la implementación absorbente lleva la DIRECCIÓN invertida en el extremo del horizonte respecto del infinito espacial; el banco lo verifica, no lo supone.

## §4 · Esquema numérico

- Discretización: leapfrog simétrico escalonado (staggered) en r* para la ecuación maestra; el campo y su derivada temporal viven en tiempos entero y semi-entero según el esquema escalonado.
- Heredado del banco FDTD: el esquema, las condiciones absorbentes/PML en ambos extremos y el criterio CFL. NO heredado: la preservación de ligadura (aquí no hay ligadura que preservar).
- CFL sellado: Δt/Δr* = 0.50 (cota teórica Δt/Δr* menor que 1 para V = 0, y levemente más estricta con V acotado: Δt/Δr* menor que 1/sqrt(1 + V_max·Δr*²/4)).
- TRES MALLAS NO ANIDADAS: Δk = Δ0 / 2^k para k = 0,1,2, con offset de malla δk = k·Δk/3, de modo que NINGÚN nodo se comparte entre niveles (control contra el artefacto de nodos coincidentes que infla el orden).
- Dominio interior de medida: se excluye una capa de frontera de 8 celdas en cada extremo y el transitorio inicial.

## §5 · Nulo numérico (falsable)

- N-RW-0 (INSTRUMENTO). Con V idénticamente 0 (M = 0), la solución analítica exacta es la onda de d'Alembert, suma de un frente que viaja a derecha y otro a izquierda. El error relativo en norma L2 del solver respecto de la exacta en el dominio interior debe ser menor o igual que 1e-12 a la malla fina. Si NO, FALLO del instrumento (mal implementado) y no se reporta física.
- N-RW-1 (ORDEN). Para V distinto de 0, el orden observado p sobre las tres mallas satisface |p − 2| menor o igual que 0.15 en la ventana de campo fuerte. Si |p − 2| mayor que 0.15, se refuta la afirmación de segundo orden.
- N-RW-2 (CONTROL INTERNO). Isospectralidad de Darboux: la desviación relativa entre la frecuencia RW y la Zerilli, para el mismo l, es menor o igual que 1e-2. Si diverge, o el resolvedor sesga la paridad, o la isospectralidad no se está midiendo.

## §6 · Auto-convergencia de Richardson (regla sellada)

- Modelo: A_k = A_exacto + C·Δk^p sobre las tres resoluciones k = 0,1,2.
- Estimador: p = logaritmo en base 2 de ( (A_0 − A_1) / (A_1 − A_2) ).
- Funcional A: la amplitud extraída del campo en un r*_obs fijo (ocho instantes de extracción), con la MISMA malla física de extracción en los tres niveles (interpolación cúbica declarada).
- Piso de redondeo: si |A_0 − A_1| es menor que 100·eps·max|A| (cerca de 2.2e-14 relativo), el ORDEN NO ES MEDIBLE y se declara; no se pinta verde.
- Mallas NO anidadas (offset distinto de 0 para k mayor o igual que 1): ninguna diferencia nodal es cero por construcción.

## §7 · Criterios de corte de fallo (sellados ANTES de la primera línea de código)

| # | medida | umbral sellado | acción |
|---|---|---|---|
| F1 | error relativo del nulo d'Alembert (N-RW-0) | mayor que 1e-12 | FALLO de instrumento (abortar) |
| F2 | orden observado (N-RW-1) | valor absoluto de (p − 2) mayor que 0.15 | FALLO: segundo orden refutado |
| F3 | señal de Richardson | d1 menor que 2.2e-14 | ORDEN NO MEDIBLE (declarar, no verde) |
| F4 | reflexión de la capa absorbente | mayor que −40 dB (coeficiente de amplitud 1e-2) | FALLO de frontera (contamina la extracción) |
| F5 | isospectralidad RW vs Zerilli (N-RW-2) | desviación relativa mayor que 1e-2 | FALLO de control interno |
| F6 | nodos compartidos entre mallas | offset nulo | BANCO INVALIDADO (las mallas deben ser no anidadas) |
| F7 | contraste contra Leaver (referencia citada) | desviación relativa mayor que 5e-2 | DIVERGENCIA declarada (control externo, no fallo automático) |

## §8 · Controles desacoplados

- CONTROL INTERNO: Darboux (RW idéntico a Zerilli). Certifica que el resolvedor no sesga la paridad; no es confirmación externa.
- CONTROL EXTERNO (referencia citada): modos cuasinormales de Leaver, con M·omega ≈ 0.37367 − 0.08896 i para l = 2, n = 0. Se cita; no se autogenera; su acuerdo no se usa como prueba de la física, sólo como discrepancia declarada.

## §9 · Procedencia y no-elevación

- El número cuasinormal es valor de referencia de la literatura (Leaver), no medido en este banco.
- La isospectralidad es un hecho analítico conocido (Darboux); se usa como control, no como hallazgo.
- Ninguna afirmación se eleva con menos de dos casos. Este pre-registro sella reglas; no produce resultados.

## §10 · Estado y siguiente paso

- Orden de fases A2.1: gate PRE = RC 10 (este acto), ESCRIBIR (este acto), gate POST = RC 11 (la huella ya habita el destino).
- PROHIBIDO hasta sellar: escribir sim/driver_rw_zerilli_1d.py, correr cualquier malla, extraer cualquier modo cuasinormal.
- Siguiente paso autorizable: crear el driver SOLO tras verificar por conteo que ESTE pre-registro está sellado (huella presente, encabezados contados, signo de dinero = 0).
