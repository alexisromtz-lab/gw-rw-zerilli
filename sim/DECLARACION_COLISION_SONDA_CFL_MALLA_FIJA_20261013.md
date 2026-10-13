# DECLARACION DE COLISION — SONDA CFL A MALLA FIJA (2026-10-13)

HUELLA-DECLARACION-COLISION-SONDA-CFL-MALLA-FIJA-20261013

ESTADO: DECLARACION. NO es acta de cierre de F9/F2. CERO commits. CERO escrituras de sonda
nueva. El objeto ordenado YA ESTABA MEDIDO por otra mano cuando la orden llego; la tarea se
cumple PASIVAMENTE (A2.1, codigo 11).

UNIVERSO DECLARADO: 1 pieza nueva (este archivo). Objetos CITADOS, no tocados:
  sim/arnes_aislamiento_piso_2d.py                         (mano ajena)
  sim/data/crudo_aislamiento_piso_2d_20261013T200929Z.json (crudo de esa mano)
  sim/arnes_richardson_2d_f2_v3.py                         (reparado; C3a/C3b ratificados)
  sim/data/crudo_2d_f2_richardson_20261013T201320Z.txt     (crudo coupled de F2)
MOTOR  : zsh + python3 -B (3.14.7) + numpy 2.4.6. Sin red, sin aleatoriedad, sin estado oculto.
UNIDAD : linea / celda / exponente.  VENTANA: reloj UTC impreso en cada cifra.

---------------------------------------------------------------------------
## 1. LA ORDEN (verbatim del dueno)

"Se autoriza la ejecucion de la sonda CFL a malla fija bajo una directiva tecnica precisa."

  1. Malla espacial fija: congelar la resolucion espacial en un unico nivel (nr_0 = 128).
  2. Refinamiento temporal diadico estricto: dt, dt/2, dt/4 (equivalente a CFL 0.50, 0.25, 0.125).
  3. Verificacion de arranque: asegurar que la evolucion utilice el paso de Cauchy exacto validado
     en el aislamiento (v^{-1/2} = (u^0 - u^{-1})/dt).
  4. Metrica a reportar: ||Psi_dt - Psi_dt/2|| y ||Psi_dt/2 - Psi_dt/4||, razon d1/d2 y exponente
     p_t = ln(d1/d2)/ln(2). Criterio declarado: p_t en 2.00 +- 0.02.

---------------------------------------------------------------------------
## 2. PRE-VUELO: LA FILA SE MIDE ANTES DE ESCRIBIR (no al cerrar)

COMANDO 1
    ls -1 sim/*cfl*
SALIDA 1
    zsh: no matches found: sim/*cfl*

  => No existia ningun archivo escrito con el nombre ordenado. El gate de pre-vuelo A2.1
     (invocado por ruta absoluta, sobre este destino) devolvio RC = 10 = objeto ausente =
     PRIMERA ESCRITURA autorizada. Ese RC es el unico permiso de escritura de este turno.

COMANDO 2
    git -C /Users/marlene/gw-rw-zerilli status --porcelain -uall -- sim/
SALIDA 2 (recorte)
     M sim/arnes_richardson_2d_f2.py
    ?? sim/arnes_aislamiento_piso_2d.py
    ?? sim/arnes_richardson_2d_f2_v3.py
    ?? sim/data/crudo_aislamiento_piso_2d_20261013T200929Z.json
    ?? sim/data/crudo_2d_f2_richardson_20261013T201320Z.txt

  => la fila NO estaba vacia por otro camino: existe un instrumento de OTRA MANO con el MISMO
     protocolo (seccion 3).

---------------------------------------------------------------------------
## 3. LA COLISION: EL OBJETO ORDENADO YA ESTABA MEDIDO

COMANDO 3
    shasum -a 256 sim/arnes_aislamiento_piso_2d.py sim/data/crudo_aislamiento_piso_2d_20261013T200929Z.json
    TZ=UTC stat -f '%Sm %z %N' -t '%Y-%m-%dT%H:%M:%SZ' <los dos>
SALIDA 3
    884a035981fcc444018f8f97d84b6b600890740c5b27baa95ab625d781f6080b  sim/arnes_aislamiento_piso_2d.py
    247c57a869d21b37da797d237339e68040fb22d036b5ef2ec87f938158589676  sim/data/crudo_aislamiento_piso_2d_20261013T200929Z.json
    2026-10-13T20:09:30Z   5103  sim/data/crudo_aislamiento_piso_2d_20261013T200929Z.json
    2026-10-13T20:16:26Z  27217  sim/arnes_aislamiento_piso_2d.py

Su cabecera declara el MISMO protocolo que la orden, verbatim:
  "Prueba A (Convergencia temporal pura): Malla espacial h_r congelada en alta resolucion
   (nr_0 = 128); barrer unicamente dt dividiendo por 2 (dt, dt/2, dt/4)."
  "Prueba B (Arranque de Cauchy): Verificar la formulacion del paso
   u^{-1} = u^0 - dt u_dot^0 + 0.5 dt^2 u_ddot^0 utilizando el operador de onda exacto para u_ddot^0."

Es decir: malla fija nr = 128 (la ordenada), escalera diadica estricta, los TRES arranques y el
triplete de errores con su razon y su exponente, por cada una de dos ventanas de observacion.

  => CONCLUSION DE LA COLISION: no se escribe sonda nueva. Duplicar el instrumento daria x == x
     (un instrumento que se mide a si mismo), no una segunda medicion.

---------------------------------------------------------------------------
## 4. LAS CIFRAS CERTIFICADAS (cada una con su comando)

COMANDO 4
    cd /Users/marlene/gw-rw-zerilli && python3 -B -c '
    import json
    d = json.load(open("sim/data/crudo_aislamiento_piso_2d_20261013T200929Z.json"))
    print("HORA", d["hora_utc"], "| segundos", d["segundos"])
    print("IDENT", d["identidad_self"]["sha256"][:16], d["identidad_self"]["lineas"], "l | huella", d["huella"])
    print("MALLA", d["malla"]); print("ESCALERA", d["escalera"])
    for k in sorted(d["celdas"]):
        c = d["celdas"][k]
        print("CELDA %-16s p=%.7f d1=%.6e d2=%.6e ver=%s d2_rel=%.4e" % (k, c["p"], c["d1"], c["d2"], c["veredicto"], c["d2_rel"]))
    c = d["c2_reduccion"]; print("C2_REDUCCION p=%.10f d1=%.6e d2=%.6e" % (c["p"], c["d1"], c["d2"]))
    print("SONDA_ARRANQUE", d["sonda_arranque"]); print("ROJOS", d["rojos"])
    print("VENTANA_AJENA", d["ventana_ajena"]); print("UMBRALES", d["umbrales"])
    print("VEREDICTO:", d["veredicto"])'

SALIDA 4 (literal)
    HORA 2026-10-13T20:09:29Z | segundos 0.6869730949401855
    IDENT 884a035981fcc444 593 l | huella HUELLA-ARNES-AISLAMIENTO-PISO-2D-20261013
    MALLA {'dt_cota': 0.04686352228078061, 'hr': 0.31496062992125984, 'hth': 0.04908738521234052, 'nr': 128, 'nt': 33, 'r_max': 42.0, 'r_min': 2.0}
    ESCALERA N [171, 342, 684] dt0 0.046783625730994149 r01 2.0 r12 2.0
    CELDA ajeno|ajena      p=1.0100585 d1=2.755088e-02 d2=1.367973e-02 ver=ROJO  d2_rel=4.7149e-03
    CELDA ajeno|total      p=1.0068098 d1=1.424432e-01 d2=7.088620e-02 ver=ROJO  d2_rel=5.0972e-03
    CELDA exacto|ajena     p=2.0005309 d1=4.279083e-04 d2=1.069377e-04 ver=VERDE d2_rel=3.7007e-05
    CELDA exacto|total     p=2.0003275 d1=1.690168e-03 d2=4.224460e-04 ver=VERDE d2_rel=3.0384e-05
    CELDA primero|ajena    p=1.0194212 d1=1.395650e-02 d2=6.884938e-03 ver=ROJO  d2_rel=2.3778e-03
    CELDA primero|total    p=1.0133667 d1=7.187325e-02 d2=3.560521e-02 ver=ROJO  d2_rel=2.5606e-03
    C2_REDUCCION p=2.0003283654 d1=3.568145e-03 d2=8.918332e-04
    SONDA_ARRANQUE 171: {'ajeno': 0.2822709686517995, 'primero': 0.1411354843258987}
                   342: {'ajeno': 0.14112291513538644, 'primero': 0.0705614575676942}
    RAZON ajeno/primero @171 = 2.0000000000
    ROJOS ['ajeno|ajena', 'ajeno|total', 'primero|ajena', 'primero|total']
    VENTANA_AJENA {'contiene_paquete': False, 'hi': 28.0, 'lo': 16.0, 'nq': 152, 'rs_e_fin': 13.981627296587927, 'rs_e_ini': 2.0918635170603674}
    UMBRALES {'c1': 2.220446049250313e-14, 'cfl_sellado': 0.5, 'p_esperado': 2.0, 'ref_piso_f2': 0.01081241, 'umbral_p': 0.05}
    VEREDICTO: EL PISO SE APAGA. Con el arranque de Cauchy EXACTO y el observable TOTAL, la malla
    congelada converge a orden 2 (|p-2| = 0.000328 <= 0.05) y el par fino baja a 4.224e-04 = 0.039 x
    REF_PISO_F2. El piso de ~1.1e-2 que midio 2D-F2 NO es del motor temporal.

COMANDO 5 (escalera y CFL efectivo, medidos sobre las cifras de la salida 4)
    python3 -B -c '...  dt_cota = 0.04686352228078061 ...'
SALIDA 5
    dt_0 = 0.046783625730994149 | N = 171 | dt*N = 8.000000000000 | dt/dt_cota = 0.998295123 | CFL_eff = 0.499147561
    dt_1 = 0.023391812865497075 | N = 342 | dt*N = 8.000000000000 | dt/dt_cota = 0.499147561 | CFL_eff = 0.249573781
    dt_2 = 0.011695906432748537 | N = 684 | dt*N = 8.000000000000 | dt/dt_cota = 0.249573781 | CFL_eff = 0.124786890
    hr = 0.31496062992125984 | hth = 0.049087385212340517
    nr0 = 128 vs niveles F2 (64/126/250): 128 NO es nivel de la terna coupled

  Declarado: la escalera es DIADICA ESTRICTA (r01 = r12 = 2.000000000000, exacto, no 1.82) y la
  malla es la ordenada (nr = 128, nt = 33). El CFL efectivo es 0.4991 / 0.2496 / 0.1248 en vez de
  0.50 / 0.25 / 0.125 clavados porque dt = T/ceil(T/dt_cota) (queda EXACTO en t = T = 8.0); el
  corrimiento es 1.7e-3 relativo y NO cambia la base de la escalera (que es lo unico que el
  exponente usa).

---------------------------------------------------------------------------
## 5. LECTURA (declaraciones, con su respaldo; nada adjudicado)

5.1  EL MOTOR TEMPORAL A MALLA FIJA **ES** DE ORDEN 2 CON EL ARRANQUE EXACTO.
     "exacto|total": d1 = 1.690168e-03, d2 = 4.224460e-04, razon = 4.000655, p = 2.0003275.
     "exacto|ajena": d1 = 4.279083e-04, d2 = 1.069377e-04, razon = 4.001062, p = 2.0005309.
     |p - 2.00| = 3.275e-04 y 5.309e-04, ambos <= 0.05 (UMBRAL_P sellado, el mismo de 2D-F2, no
     rebajado). El criterio de la orden (2.00 +- 0.02) SE CUMPLE en las dos ventanas: el resultado
     no depende de la ventana (el ancho no decide aqui: 13.9034 y 2.8897 de norma, misma p).

5.2  PERO EL CRITERIO NO DEMUESTRA LO QUE LA ORDEN ESPERABA: la causa no es (solo) el refinamiento
     no diadico de la malla coupled. Con la convencion LITERAL de v3 —v = +0.5*dt*a(u^0), que su
     propio texto comenta "# d_t Psi(0) = 0"— la MISMA malla fija, la MISMA escalera y los MISMOS
     operadores dan:
       "ajeno|total"  p = 1.0068098   ROJO      "ajeno|ajena"  p = 1.0100585   ROJO
       "primero|total" p = 1.0133667  ROJO      "primero|ajena" p = 1.0194212  ROJO
     Es decir: el arranque defectuoso contamina la escalera espacial-refinada con un termino O(dt)
     y hunde el exponente de 2.00 a 1.01. La hipotesis 3 del dueno (el arranque de Cauchy en v3)
     queda PROMOVIDA de sospecha a CAUSA MEDIDA, y con dos testigos independientes: el cruce de
     identidad declarado en 5.5 y esta escalera de arranques.

5.3  LA HIPOTESIS 1 (trampa de base en Richardson) QUEDA INVERTIDA POR ARITMETICA PROPIA.
     COMANDO 6:  p = ln(razon)/ln(r) con razon = 5.023592 (PRINCIPAL, crudo 201320Z)
     SALIDA 6:
       p_base2                                = 2.328719
       p con r = 1.8133 (dt del dueno)        = 2.712173
       p con r = 1.8305 (dt del dueno)        = 2.669822
       p con r = 1.818182 (dt del crudo)      = 2.699975
       p con r = 1.826667 (dt del crudo)      = 2.679111
       p con r = sqrt(r1*r2) = 1.822419       = 2.689503
     Corregir la base SUBE el exponente (2.3287 -> 2.67..2.71). Una base mal elegida no puede
     fabricar un exceso > 2; por tanto la hipotesis 1 no es la causa del exceso y no se sostiene
     como causa (se declara, no se adjudica el resto).

5.4  COTA ARITMETICA SOBRE LA TERNA COUPLED (misma salida 6, contexto medido con el COMANDO 7):
     factores de refinamiento medidos en el crudo coupled: hr 1.968750 -> 1.984127 (hr^2 3.875977
     -> 3.936760), hth 1.969697 -> 1.984615, dt 1.818182 -> 1.826667.
     Cualquier termino de UNA sola potencia con base <= 1.984127 da como maximo 3.936760 (q = 2) o
     1.826667 (q = 1). Las razones medidas son 4.809048 (C3b), 4.948806 (C2) y 5.023592
     (PRINCIPAL): las TRES exceden 3.936760. => la terna coupled NO es de un solo termino: exige
     AL MENOS DOS terminos de base distinta (o un termino con q > 2). Coincide con la hipotesis 2
     (acoplamiento temporal-espacial cruzado), cuyo ingrediente temporal (el arranque) acaba de
     quedar medido en 5.2. No se adjudica la particion de pesos: no se modelo.

5.5  EL DEFECTO DEL ARRANQUE ES UN TERMINO DE TAYLOR DE SEGUNDO ORDEN, IDENTICO EN LAS DOS MANOS.
     La convencion de v3 (v = +0.5*dt*a(u^0)) es LITERALMENTE el arranque "ajeno" del instrumento
     de aislamiento (u^{-1} = u^0 - 0.5 dt^2 a(u^0)); el arranque "exacto" es u^{-1} = u^0 + 0.5
     dt^2 a(u^0). Los residuos de arranque medidos por esa mano:
       |u^{-1}_ajeno   - u^{-1}_exacto| = 0.2822709686517995   (N = 171)
       |u^{-1}_primero - u^{-1}_exacto| = 0.1411354843258987   (N = 171)
       razon = 2.0000000000 exacto, y al dividir dt por 2 en N = 342: 0.14112291513538644 /
       0.0705614575676942 (misma razon 2.0000). => firma de Taylor: dt^2 |a^0| contra 0.5 dt^2
       |a^0|. Defecto local O(dt^2) que, al ser un error de DATO INICIAL en v, viaja como O(dt)
       global: eso es exactamente lo que mide 5.2 (p = 1.01, no 2).

5.6  EL PISO DE 2D-F2 (REF_PISO_F2 = 1.081241e-02, medido con nr0 = 64) NO ES DEL MOTOR TEMPORAL.
     A malla fija 128 el par fino temporal baja a d2 = 4.224460e-04 = 0.039079 x REF_PISO_F2
     (d2_rel = 3.0384e-05). Cifra CITADA del instrumento ajeno; no se re-mide aqui.

---------------------------------------------------------------------------
## 6. LO QUE NO SE ESCRIBIO, Y POR QUE

- No se escribio sonda CFL nueva: la fila estaba escrita (seccion 3). Cero escrituras, cero copias
  en /tmp. El gate de este archivo (RC = 10 previo) fue la unica escritura del turno.
- RESIDUAL 1 (no ejecutado, requiere orden): repetir la terna COUPLED de v3 con el arranque exacto.
  Es la medicion que cerraria el diagnostico de las tres causas: si la razon vuelve a ~3.90, el
  exceso de 4.81..5.02 era integramente el arranque. Exigiria mutar v3 (ratificado por C3a/C3b):
  no se toca sin orden.
- RESIDUAL 2 (no ejecutado, requiere decision): una sonda propia que importe los operadores de v3
  mediria el MISMO objeto con OTRO instrumento (confluencia entre dos implementaciones
  independientes). Es valor de control, no objeto nuevo; queda a decision del dueno.

---------------------------------------------------------------------------
## 7. DISCREPANCIAS DECLARADAS, NO ADJUDICADAS

7.1  Los dt citados en la orden (4.851088e-02 / 2.675265e-02 / 1.461478e-02 => r = 1.8133 / 1.8305)
     NO son los que imprime el crudo coupled de v3 (4.8484848485e-02 / 2.6666666667e-02 /
     1.4598540146e-02 => r = 1.818182 / 1.826667). Se imprimen LOS DOS pares y el control 5.3 se
     calcula con ambos: la direccion (la correccion SUBE p) es la misma en los cuatro casos.
7.2  El mtime del instrumento ajeno (2026-10-13T20:16:26Z) es POSTERIOR a su propio crudo
     (20:09:29Z), mientras su sha256 en disco (884a035981fcc444...) es identico al que el crudo
     declara de si mismo => el instrumento en disco es el que produjo el crudo; el mtime posterior
     se declara sin adjudicar (re-escritura con contenido identico, o toque).
7.3  La ventana "ajena" de ese instrumento NO contiene el paquete (rs_e en [2.091864, 13.981627]
     con [16.0, 28.0] pretendido; contiene_paquete = false). Es un defecto de metro DECLARADO en su
     propia cabecera y NO parcheado. Por eso las cifras que se citan como limpias son las de la
     ventana "total" (interior completo, sin ventana, sin interpolacion, sin offset), y las de
     "ajena" se citan como segunda lectura: las dos dan orden 2 con el arranque exacto, asi que el
     defecto de ventana no cambia el veredicto.
7.4  nr_0 = 128 (la malla ordenada) NO es nivel de la terna coupled de F2 (64 / 126 / 250): la
     malla fija ordenada coincide con la del instrumento de aislamiento, no con ningun nivel de F2.
     Por eso REF_PISO_F2 se usa como CITA, nunca como comparacion de igual a igual.

---------------------------------------------------------------------------
## 8. COMANDOS (reproducibles, en orden)

    ls -1 sim/*cfl*
    git -C /Users/marlene/gw-rw-zerilli status --porcelain -uall -- sim/
    shasum -a 256 sim/arnes_aislamiento_piso_2d.py sim/data/crudo_aislamiento_piso_2d_20261013T200929Z.json
    TZ=UTC stat -f '%Sm %z %N' -t '%Y-%m-%dT%H:%M:%SZ' sim/arnes_aislamiento_piso_2d.py sim/data/crudo_aislamiento_piso_2d_20261013T200929Z.json
    python3 -B -c '<extractor json de la salida 4>'
    python3 -B -c '<escalera y CFL efectivo de la salida 5>'
    python3 -B -c '<control de base de la salida 6>'
    grep -n 'nivel [0-9]:' sim/data/crudo_2d_f2_richardson_20261013T201320Z.txt

---------------------------------------------------------------------------
## 9. ESTADO

CERO commits. Contencion vigente: no se comitea nada a Git y no se redacta acta de cierre de F9/F2.
Este archivo es DECLARACION DE COLISION, no cierre. Los dos crudos de F2 siguen en disco como
testigo de calibracion intermedia no adjudicado. El arbol estaba en movimiento (otra mano escribio
arnes_aislamiento_piso_2d.py a 20:16Z): por eso se declaro por slug completo y no se toco nada ajeno.
