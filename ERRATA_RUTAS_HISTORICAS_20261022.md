# Fe de erratas: rutas del entorno de ejecución en registros históricos

<!-- HUELLA-ERRATA-RUTAS-GWRW-20261022 -->

## Alcance

La auditoría de fuga pública (`fuga-publica/1`) reporta **56 referencias** al entorno de
ejecución original repartidas en **34 archivos** de este repositorio: 51 apuntan a la raíz
del propio árbol y 5 al repositorio orquestador privado desde el que se despacharon las
corridas. Ninguna vive en código ejecutable: 23 son crudos de corrida (`sim/data/*.json`,
salida literal de los instrumentos) y 11 son documentos fechados (`sim/PREREGISTRO_*`,
`sim/ACTA_*`, `sim/ADENDA_*`, `sim/ERRATA_1_*` y el manuscrito depositado).

## Determinación de inmutabilidad

Estos archivos son el registro de lo que ocurrió: pre-registros anteriores a la corrida,
actas de cierre y volcados crudos de los medidores. Reescribirlos cambiaría el contenido
sobre el que se sostienen las conclusiones publicadas y rompería la identidad del depósito
(Zenodo) y de las sumas de verificación ya emitidas. Por eso **no se editan**: la
discordancia se resuelve aquí, no en el archivo.

## Correspondencia canónica

Toda referencia a `/Users/<usuario>/gw-rw-zerilli` equivale operacionalmente a la raíz del
árbol reproducido localmente (`GW_RW_ROOT`), conservando el sufijo relativo de cada
referencia. Las 5 referencias al repositorio orquestador corresponden a la transcripción
verbatim del comando de pre-vuelo A2.1 que autorizó cada escritura; su valor probatorio es
precisamente que conservan la ruta tal como se ejecutó. Esta equivalencia documenta la
portabilidad del contexto; no garantiza por sí sola la existencia de cada archivo citado.

## Menciones al arbol de custodia

<!-- HUELLA-ERRATA-MENCIONES-CUSTODIA-20261022 -->

**10 lineas** de los registros y del expediente de deposito nombran el arbol privado
donde viven el instrumento de pre-vuelo, el catalogo interno y el corpus de trabajo.
Designan el **origen de la custodia**, no una dependencia: ningun archivo publico de este
repositorio lo importa, lo ejecuta ni lo necesita para medir.

Se conservan por la misma razon que las rutas: son la transcripcion de lo que se ejecuto y
lo que se deposito. Reescribirlas cambiaria el contenido sobre el que se sostienen las
conclusiones y el deposito. Quedan adjudicadas por huella con las demas lineas de este
libro: si alguien las edita, la huella caduca y el hallazgo vuelve a abrirse.

Nota sobre el expediente de deposito: cuando un metadato ya publicado acredita el arbol
privado como identificador relacionado, la correccion no se hace aqui — el registro
externo es inmutable en su version. Se declara en esta errata y se corrige en la version
siguiente del deposito.

## Registro

Las 54 líneas afectadas quedan adjudicadas en el libro tipado de la auditoría
(`fuga_allow.txt`) bajo `RUTA_HISTORICA_SELLADA`, en dos categorías: `REGISTRO_DE_CORRIDA`
(crudos) y `PREREGISTRO_O_ACTA_FECHADA` (documentos). La adjudicación va firmada por la
huella de la línea: si alguien edita el registro, la huella caduca y el hallazgo vuelve a
abrirse. Esa es la garantía de que esta errata no es una exención: es una custodia.
