# Transacciones_Billetera_SantaFe
Script que extrae movimientos hechos en el comercio con Billetera Santa Fe utilizando la API suministrada por PlusPagos.
Vuelca los datos de los movimientos en dos archivos, uno formato xlsx (detallado) y uno txt (resumido). 
En base a esto, arma un mensaje con la información del txt, adjunta ambos archivos y los envía por correo.

### Por qué hiciste este script si en el panel de PlusPagos podes descargar el mismo archivo?
Porque el archivo que exporta la página de PlusPagos está formateado en su totalidad como texto, por lo que dificulta una rápida consulta del mismo al no permitir utilizar, por ejemplo, función autosuma.
Y porque ganas de aprender 

### Ejecución
##### _Importante:_ para llevar a cabo la ejecución es necesario contar con guid y frase, credenciales otorgadas por Plus Pagos para poder consumir su API.
Para ejecutar el script:
~\billetera_santafe> python3 .\main.py --fecha_desde yyyy-mm-dd --fecha_hasta yyyy-mm-dd --suc 2 --estado 3
* Las fechas son opcionales, sino toma la del día de la fecha
* Estado de la transaccion por defecto es 3 (transacción realizada)
* Sucursal es obligatorio por ahora

### Imágenes
![ResumenCorreo](https://user-images.githubusercontent.com/55287162/127890295-40985062-5c40-40f2-9170-82155ea80960.png)
![ArchivoXlsx](https://user-images.githubusercontent.com/55287162/127891592-4b7295ad-cb7e-4899-bd7e-47f4df6da762.png)

#### Pendiente:
* Elección de filtro sucursal/estado transacción
* Automatizar script para que corra como servicio
* Embellecer (?) archivo xlsx


## Contribuyendo 🖇️

_Si querés contribuir con este proyecto, no dudes en hacer una ```pull request```. Todas las ideas y sugerencias son bienvenidas!_

---
💻 En Twitter soy [akalautaro](www.twitter.com/akalautaro)
