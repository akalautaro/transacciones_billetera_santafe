#!/usr/bin/env python3
import argparse
from datetime import datetime
import billetera_cliente as bsfe
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Obtiene resultados de ventas del día de Billetera Santa Fe')
    parser.add_argument('--fecha_desde', help='Fecha desde la cual buscar movimientos',
                        default=datetime.today().strftime('%Y-%m-%d'))
    parser.add_argument('--fecha_hasta', help='Fecha hasta la cual buscar movimientos',
                        default=datetime.today().strftime('%Y-%m-%d'))
    parser.add_argument('--suc', help='Nro de sucursal')
    parser.add_argument('--caja', help='Nro de caja de la sucursal')
    parser.add_argument('--estado', help='Estado de la transacción', default=3)  # 3 es realizada

    args = parser.parse_args()

    bsf = bsfe.BilleteraSF('__GUID_COMERCIO__', '__FRASE_COMERCIO__')

    check_api = bsf.check_status()
    if check_api is True:
        movimientos = bsf.get_movimientos_realizados(fecha_desde=args.fecha_desde, fecha_hasta=args.fecha_hasta,
                                                     nro_sucursal=args.suc.zfill(10))
    else:
        print('Servicio no disponible')
