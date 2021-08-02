import xlsxwriter
from datetime import datetime
import funciones_correo as fc


class Archivos:
    """Documentación oficial de xlsxwriter: https://xlsxwriter.readthedocs.io/"""
    def __init__(self):
        ...

    def crea_txt(self, fecha_desde, fecha_hasta):
        """Crea un archivo txt que contendrá el resumen de las transacciones.
        De este se leerá la info a enviar por correo."""
        f = open(f'./Output/Resumen_transacciones_{fecha_desde}-{fecha_hasta}.txt', 'w')
        f.write(f'DNI Cliente\t\t\tImporte\t\t\tNro Transaccion\t\tFecha\t\t\t\t\t\tFecha Pago\n')
        f.close()

    def arma_txt(self, fecha_desde, fecha_hasta, info_transaccion):
        """Vuelca la información dentro del archivo txt creado con crea_txt()."""
        f = open(f'./Output/Resumen_transacciones_{fecha_desde}-{fecha_hasta}.txt', 'a')

        for li in info_transaccion:
            f.write(f'{li}\t\t\t')
        f.write('\n')
        f.close()

    def cierra_txt(self, fecha_desde, fecha_hasta, importe_total, total_transacciones):
        """Escribe importe final y también cantidad de transacciones"""
        f = open(f'./Output/Resumen_transacciones_{fecha_desde}-{fecha_hasta}.txt', 'a')
        f.write(f'\nImporte total\t\t{importe_total}\n')
        f.write(f'Cant. transacciones\t{total_transacciones}\n')

    def exporta_excel(self, fecha_desde, fecha_hasta, transacciones):
        """Crea el libro de Excel y agrega una hoja al mismo, además se llama a las funciones
        para crear un archivo txt. Además se definen formatos de celda."""
        workbook = xlsxwriter.Workbook(f'./Output/Detalle_transacciones_{fecha_desde}_a_{fecha_hasta}.xlsx')
        worksheet = workbook.add_worksheet('Transacciones')
        self.crea_txt(fecha_desde, fecha_hasta)

        bold = workbook.add_format({"bold": True})
        it = workbook.add_format({"italic": True})
        bdit = workbook.add_format({"bold": True, "italic": True})
        currency = workbook.add_format({'num_format': '$#.##0,00'})
        timestamp = workbook.add_format({'num_format': 'dd/mm/aaaa hh:mm'})
        worksheet.set_column(0, 13, 35)

        importe_total = []
        row = 0
        column = 0
        cabeceras = ['Sucursal', 'NroTransaccion', 'Estado', 'FechaTicket', "FechaPago", 'MontoBruto',
                     'MontoDescuento', 'MontoFinal', 'MedioPago', 'DNICliente', 'NombreCliente',
                     'EmailCliente', 'TelefonoCliente']

        for c in cabeceras:
            worksheet.write(row, column, c, bold)
            column += 1

        for t in transacciones:
            row += 1
            datos_transaccion = []
            sucursal = t["sucursal"]
            nro_transaccion = t["transaccionComercioId"]
            estado = t["estado"]
            fecha = t["fecha"][:16].replace('T', ' ')  # 2021-07-29T12:54:22.924911 -> 2021-07-29 13:14
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M')  # 2021-07-29T12:54:22.924911
            fecha = datetime.strftime(fecha, '%d/%m/%Y %H:%M')  # 2021-07-29T12:54:22.924911
            fecha_pago = t["fechaPago"][:16]   # 29/07/2021 12:54:22
            monto_bruto = round(t["montoBruto"], 2)
            monto_descuento = round(t["montoDescuento"], 2)
            monto_final = t["monto"]
            medio_pago = t["medioPagoNombre"]
            dni_cliente = (t["informacionPagador"]["numeroDocumento"]).zfill(8)
            nombre_cliente = t["informacionPagador"]["nombre"]
            email_cliente = t["informacionPagador"]["email"]
            telefono_cliente = t["informacionPagador"]["telefono"]
            datos_transaccion = [sucursal, nro_transaccion, estado, fecha, fecha_pago, monto_bruto, monto_descuento,
                                 monto_final, medio_pago, dni_cliente, nombre_cliente, email_cliente, telefono_cliente]

            column = 0
            for d in datos_transaccion:
                worksheet.write(row, column, d)
                column += 1

            unwanted_col = {sucursal, nombre_cliente,estado, monto_descuento, monto_final,
                            medio_pago, email_cliente, telefono_cliente}
            datos_transaccion = [d for d in datos_transaccion if d not in unwanted_col]
            datos_transaccion = [dni_cliente, monto_bruto, nro_transaccion, fecha, fecha_pago]

            importe_total.append(datos_transaccion[1])

            self.arma_txt(fecha_desde, fecha_hasta, datos_transaccion)

        total = round(sum(importe_total), 2)
        cant_transacciones = len(importe_total)

        self.cierra_txt(fecha_desde, fecha_hasta, total, cant_transacciones)

        workbook.close()
        print('Detalle de transacciones creado exitosamente')  # Debería estar dentro de un try

        mail = fc.Mail()
        mail.arma_mail(fecha)
