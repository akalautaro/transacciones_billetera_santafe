import requests
import json
import funciones_archivos as ef


class BilleteraSF:
    """Conexión y consumo de la API de Billetera Santa Fe."""
    BASE_URL = 'https://botonpp.asjservicios.com.ar:8082/v1'
    BASE_URL_SB = 'https://sandboxpp.asjservicios.com.ar:8082/v1'
    guid = '__GUID_COMERCIO__'
    frase = '__FRASE_COMERCIO__'
    bearer_token = ''
    sesion = requests.Session()
    a = ef.Archivos()

    def __init__(self, guid, frase):
        self.guid = guid
        self.frase = frase

    def check_status(self) -> bool:
        """Chequea la disponibilidad de la API de Billetera Santa Fe."""
        url = self.BASE_URL + '/health'
        req = requests.request('GET', url)

        response = json.loads(req.content.decode('utf-8'))
        status = response['message']

        print('Estado de la API:', status)

        if req.status_code == 200:
            return True
        else:
            return False

    def login(self):
        body = '{"guid": "' + self.guid + '", "frase": "' + self.frase + '"}'
        headers = {'Content-type': 'application/json'}

        # No verificar certificados
        self.sesion.verify = False

        url = self.BASE_URL + '/sesion'
        req = requests.Request('POST', url, headers=headers, data=body)
        prepped = req.prepare()
        prepped.body = body

        # Envío el requerimiento
        resp = self.sesion.send(prepped)
        # response = json.dumps(resp.content.decode('utf-8'), indent=4)  # Formateo para leer la respuesta
        response = json.loads(resp.content.decode('utf-8'))
        bearer_token = response['data']

        # Verificar respuesta
        if resp.status_code >= 400:
            print('Error de conexión:', resp.status_code)
        elif resp.status_code == 200:
            print(response['message'], '\n')

        self.bearer_token = bearer_token

    def get_movimientos_realizados(self, fecha_desde, fecha_hasta, nro_sucursal):
        """Movimientos por día y por sucursal. La URL debería ser como la siguiente:
        /transactions?FechaDesde=2021/07/17&FechaHasta=2021/07/26&NumeroSucursal=0000000002&EstadoTransaccion=3"""
        estado_transaccion = '3'  # Transacción realizada
        url = self.BASE_URL + f'/transactions?FechaDesde={fecha_desde}&FechaHasta={fecha_hasta}' \
                              f'&NumeroSucursal={nro_sucursal}&EstadoTransaccion={estado_transaccion}'

        self.login()

        headers = '{"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer ' \
                  + self.bearer_token + '"}'
        headers = json.loads(headers)

        # Envío la request
        r = requests.get(url, headers=headers)
        # respuesta = json.dumps(r.content.decode('utf-8'), indent=4)  # Formateo string
        if r.status_code == 200:
            # t = r.json()
            respuesta = r.content.decode('utf-8')

            with open('Old/respuesta_completa.txt', 'w') as file:
                file.write(respuesta)
            respuesta = json.loads(r.content.decode('utf-8'))  # JSON str a dict
            print(respuesta["message"])
            transacciones = respuesta["data"]["transacciones"]
            # print(respuesta["data"]["transacciones"][0])  # Test

            with open('Old/transacciones.txt', 'w') as file:
                file.write(str(transacciones))

            self.a.exporta_excel(fecha_desde, fecha_hasta, transacciones)

        else:
            print('Error al consultar las transacciones.')

    def get_otros_movimientos(self, fecha_desde, fecha_hasta, nro_sucursal):
        """Movimientos por día y por sucursal. La URL debería ser como la siguiente:
        /transactions?FechaDesde=2021/07/17&FechaHasta=2021/07/26&NumeroSucursal=0000000002&EstadoTransaccion=3"""
        estado_transaccion = '3'  # Transacción realizada
        # exclude = {"EstadoTransaccion": {"value": 3, "operator": "!="}}
        url = self.BASE_URL + f'/transactions?FechaDesde={fecha_desde}&FechaHasta={fecha_hasta}' \
                              f'&NumeroSucursal={nro_sucursal}&EstadoTransaccion={estado_transaccion}'

        self.login()

        headers = '{"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer ' \
                  + self.bearer_token + '"}'
        headers = json.loads(headers)

        r = requests.get(url, headers=headers)
        respuesta = json.dumps(r.content.decode('utf-8'), indent=4)
        print(respuesta)
