# ADENDA 1 -- RATIFICACION DE LA SECCION 4 Y ESQUEMA 2D RATIFICADO

HUELLA-ADENDA-1-RATIFICACION-SECCION-4-Y-ESQUEMA-2D-RATIFICADO-20261013

T_UTC_VENTANA : 2026-10-13T19:23:31Z

UNIVERSO DECLARADO : este archivo (1 pieza) + sim/PREREGISTRO_FRENTE_2D_CQG_20261013.md
                     (1 pieza, blob 2b2dd0fa898cf9de29434899eb2de07f6bbadfca, commit 2eebc3b).
MOTOR              : no aplica (registro), salvo los crudos de terceros que se CITAN por ruta y tamano.
UNIDAD             : linea / encabezado / archivo.
VENTANA            : reloj UTC impreso arriba; el .git del arbol queda FUERA del universo contado.

Objeto de esta adenda: (1) registrar la RATIFICACION del dueno sobre la seccion 4 del pre-registro
sellado; (2) declarar que la via modal de esa seccion queda SUPERADA (la pieza sellada NO se parchea:
recibe apendice); (3) registrar el DOMINIO MEDIDO del umbral de F1, hallado en el sandbox antes de
disparar el gate.

---

## Seccion 1 -- Contrato de destino (A2.1)

TARGET        : /Users/marlene/gw-rw-zerilli/sim/ADENDA_1_RATIFICACION_SECCION_4_Y_ESQUEMA_2D_RATIFICADO_20261013.md
BLOB_PRE      : AUSENTE
HUELLA        : HUELLA-ADENDA-1-RATIFICACION-SECCION-4-Y-ESQUEMA-2D-RATIFICADO-20261013
LINEAS_PRE    : 0
GATE_PRE      : RC 10 (el objetivo no existe) -- corrido 2026-10-13T19:23:31Z
COLISION      : 0 ocurrencias de la huella y de la huella del driver 2D en el arbol a esa hora.
Este archivo es NUEVO: no abre ni muta ninguna pieza existente.

---

## Seccion 2 -- La ratificacion del dueno

Citas recibidas (letra tal cual, transcripcion de sesion):

  (a) "Se autoriza la redaccion del esqueleto del driver 2D en gw-rw-zerilli/sim/ unicamente cuando
      este listo para someterse a su tupla A2.1."
  (b) "Procede con el ensamblado de la tupla para el driver 2D cuando el codigo en papel este listo."
  (c) "La primera corrida obligatoria debe ser el Gate 2D-F1 (prueba nula en espacio plano M=0 a CFL
      constante) antes de inyectar el potencial de Schwarzschild."
  (d) "Manten bloqueados los archivos del frente de reflexion y el extractor."

Transcripcion TECNICA del cuerpo ratificado (declarada como interpretacion, no verbatim):

  R1. Malla 2D axisimetrica pura en (r*, theta), m = 0. PROHIBIDA la descomposicion modal desacoplada:
      proyectar en Y_l0 reduciria el problema a lineas 1D independientes y haria desaparecer la
      fisica 2D (frontera y dispersion) que este frente existe para medir.
  R2. Cota de paso: dt <= CFL * [ 1/(dr*)^2 + 1/( r(r*)^2 (dtheta)^2 ) ]^(-1/2) con CFL <= 0.50.
  R3. Dominio angular theta en [0, pi/2], con condicion de NEUMANN ecuatorial d_theta Psi = 0 en
      theta = pi/2 (simetria de reflexion: duplica la resolucion efectiva). El polo theta = 0 se
      regulariza por paridad / L'Hopital discreto: Laplaciano angular -> 2 d_theta_theta.
  R4. La inversion r(r*) por Newton-Raphson, monotona y exacta (precalculada una sola vez para no
      inyectar ruido en el factor de escala angular).
  R5. La ley de capa que gobierne el 2D es la de su propia fuente (gate F11); queda PROHIBIDO heredar
      el exponente 1D -1.3936 para dimensionar absorbentes 2D.
  R6. Los frentes de reflexion (, reflexion_frontera_1d.py) y extractor (, extractor_polos_matrixpencil.py
      y sus piezas) permanecen BLOQUEADOS: se declaran, no se tocan y no se adjudican.

---

## Seccion 3 -- Que de la Seccion 4 sellada queda SUPERADA

La pieza sellada declaro su seccion 4 "PENDIENTE DE RATIFICACION". La ratificacion la SUPERA en cuatro
puntos y CONSERVA uno. La pieza sellada no se edita: se apunta aqui.

  Punto                               | Seccion 4 sellada                | Ratificado (R1..R6)            | Estado
  ------------------------------------|----------------------------------|--------------------------------|----------
  Esquema angular                     | proyeccion modal en Y_l0 por modo| malla (r*, theta), m = 0 pura  | SUPERADO
  Cota de paso                        | dt <= CFL dr* (herencia 1D)      | R2 con termino angular         | SUPERADO
  Rango angular y bordes              | theta en [0, pi]                 | [0, pi/2], Neumann + L'Hopital | SUPERADO
  Inversion de tortuga                | biseccion vectorizada            | Newton-Raphson monotona        | SUPERADO
  Mallas no anidadas d_k = k*d_k/3    | declarado                        | se conserva                   | CONSERVADO
  Capa absorbente                     | pendiente de F11                 | R5                             | CONSERVADO

Ecuacion maestra ratificada para el frente escalar (f = 1 - 2M/r):

    d2_t Psi = d2_{r*} Psi - (f/r^2) L^2_theta Psi - (2M f / r^3) Psi ,
    L^2_theta = -(1/sin theta) d_theta ( sin theta d_theta )

Control interno declarado: para Psi con contenido Y_l0, L^2_theta Psi = l(l+1) Psi, y la ecuacion
colapsa al potencial escalar 1D sellado  V = f [ l(l+1)/r^2 + 2M/r^3 ]. El limite M = 0 da
d2_t Psi = d2_r Psi - (1/r^2) L^2_theta Psi, que es la ecuacion de onda plana en esfericas.

---

## Seccion 4 -- Mapeo de nombres (no se renumera)

  "Gate 2D-F1" (nombre del dueno)  ==  el nulo N-2D-0 de la pieza sellada (reduccion 2D->1D con V
                                        identicamente 0) MAS su control de solucion manufacturada.
  Las etiquetas F8..F14 de la pieza sellada NO se renumeran. "2D-F1" es el nombre de la primera
  corrida obligatoria, no una etiqueta nueva de la escalera.
  La reduccion 2D->1D se prueba contra el instrumento 1D CERTIFICADO (subproceso, crudo JSON), nunca
  contra una copia del bucle dentro del mismo archivo: un instrumento que se mide a si mismo es x == x.

---

## Seccion 5 -- Hallazgo medido que cae sobre el umbral de F1 (DOMINIO DEL UMBRAL)

Medido en el sandbox (fuera del arbol git de este frente; el sandbox NO es universo del frente).
Se registra, no se adjudica. Crudos y fuentes, por ruta y tamano:

  /tmp/f4v3/sonda_2d_f1_20261013.py            3914 B   |  /tmp/f4v3/sonda_2d_f1_20261013T190602Z.txt   2783 B
  /tmp/f4v3/sonda_2d_f1_v2_20261013.py         4650 B   |  /tmp/f4v3/sonda_2d_f1_v2_20261013T190916Z.txt 2791 B
  /tmp/f4v3/sonda_2d_f1_v3_20261013.py         5794 B   |  /tmp/f4v3/sonda_2d_f1_v3_20261013T190947Z.txt 3133 B

Malla del sandbox: PERIODICA CARTESIANA N x N (no es la malla polar ratificada). Lo que se transfiere
es el AVISO, no la ley: en la malla polar el dominio se vuelve a medir.

  H1. El residuo de exactitud de maquina NO es una propiedad del esquema: tiene DOMINIO. Con dato
      discreto y referencia continua, famila diagonal (mx = my) a cfl = 1/sqrt(2):
      m = 1 -> 3.444081e-15 | m = 2 -> 2.573674e-14 | m = 3 -> 1.423329e-14 | m = 4 -> 1.967306e-14 |
      m = 6 -> 8.744309e-15 | m = 8 -> 8.185048e-14.  Modos NO diagonales al MISMO cfl: (2,1)
      1.900558e-02 | (3,1) 1.185170e-03 | (0,2) 7.459319e-04.  El umbral tiene dominio y el control
      negativo lo demuestra.
  H2. La exactitud de H1 es coincidencia de simbolo a cfl = 1/sqrt(2), NO robustez. Barrido de cfl
      sobre la diagonal: 0.5 -> 1.077678e-02 | 0.6 -> 6.92e-03 | 0.7 -> 5.40e-04 | 1/sqrt(2) ->
      2.573674e-14 | 0.75 -> 2.922646e+24 (inestable).  A CFL = 0.50 -- el sellado en R2 -- NO existe
      ese dominio en esa familia.
  H3. La reduccion 2D -> 1D es exacta y reproducible: residuo(2D eje) == residuo(1D) en las CUATRO
      resoluciones medidas (N = 64/128/256/512):
      3.633376e-03 / 7.459319e-04 / 2.073124e-04 / 5.184681e-05, identico en las dos columnas.

Consecuencia (declarada, no adjudicada): un F1 enunciado como "residuo < 1e-13" a CFL = 0.50 NO tiene
dominio medido. El gate de F1 en el driver debe publicar su umbral CON su dominio:
  F1.a EXACTITUD -- dominio: dato independiente de theta (rama l = 0), M = 0, V identicamente 0. Ahi el
       termino angular es identicamente nulo y el dato es modo discreto del propio simbolo radial: la
       exactitud de maquina es alcanzable y discriminante.
  F1.b DISPERSION -- dominio: perfil angular l = 2 vivo. No se reclama exactitud: se mide el ORDEN de
       convergencia y se exige el control negativo (termino angular apagado => NO converge).
  F1.c PAR DE DOMINIO -- se imprime el par (exacto ~1e-15 | vivo ~1e-03) en la misma corrida: un umbral
       sin su dominio es un verde falso.

---

## Seccion 6 -- Consecuencia sobre F8..F14

Los umbrales sellados de la escalera viajan con su dominio declarado, igual que F1: F8 (nulo de
reduccion, umbral 1e-12) es alcanzable en la rama independiente de theta y NO es un reclamo de maquina
en la rama con angular vivo; F9 mide orden; F10 mide fuga modal; F11 vuelve a medir la ley 2D; F12 y
F13 dependen del extractor y del arnes de SNR; F14 mide regularidad en los polos. Ninguno se dispara
contra el dominio de otro.

---

## Seccion 7 -- Bloqueados (declarados, no adjudicados)

Frente de reflexion: sim/reflexion_frontera_1d.py (40172 B, SIN RASTREAR), sim/reflexion_escala_D.py
(12738 B, SIN RASTREAR) -- con el defecto 4 abierto (ventana_ft duplicada, la viva en l.347) declarado
inmutable.
Frente extractor: sim/extractor_polos_matrixpencil.py (39590 B, rastreado, commit 75e5e27) mas cuatro
objetos SIN RASTREAR medidos a 2026-10-13T19:23:31Z: sim/PREREGISTRO_EXTRACTOR_MULTIMODO_SNR_20261013.md
(14544 B), sim/harness_multimodo_snr.py (24013 B), sim/ACTA_MP_M1_ARNES_MULTIMODO_SNR_20261013.md
(9936 B) y sim/data/crudo_multimodo_mp_m1_20261013T191007Z.json.
Ninguno se abre, se corre ni se adjudica en este ciclo.

---

## Seccion 8 -- Estado y siguiente paso

Estado: ratificacion registrada; via modal superada; dominio del umbral de F1 medido y declarado.
Siguiente paso (uno solo, y es el que el dueno autorizo): el esqueleto del driver 2D en
sim/driver_rw_zerilli_2d.py, sometido a su propia tupla A2.1, con la cota R2 literal, los bordes R3 y
la ley de capa de su propia fuente (R5). La capa absorbente 2D y el extractor NO entran en el
esqueleto: son F11 y F12/F13.
