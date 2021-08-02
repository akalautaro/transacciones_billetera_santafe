# Transacciones_Billetera_SantaFe
Script que extrae movimientos hechos en el comercio con Billetera Santa Fe utilizando la API suministrada por PlusPagos.
Vuelca los datos de los movimientos en dos archivos, uno formato xlsx (detallado) y uno txt (resumido). 
En base a esto, arma un mensaje con la información del txt, adjunta ambos archivos y los envía por correo.

### Por qué hiciste este script si en el panel de PlusPagos podes descargar el mismo archivo?
Porque el archivo que exporta la página de PlusPagos está formateado en su totalidad como texto, por lo que dificulta una rápida consulta del mismo al no permitir utilizar, por ejemplo, función autosuma.
Y porque ganas de aprender 

#### Pendiente:
* Elección de filtro sucursal/estado transacción
* Automatizar script para que corra como servicio
* Embellecer (?) archivo xlsx
