import os
import shutil
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
import mimetypes  # For guessing MIME type based on file name extension


class Mail:

    def __init__(self):
        ...

    def arma_mail(self, fecha_desde):
        """Arma el correo con los datos de emisor y receptor, cuerpo y otros datos necesarios.
        Documentación email.MIME: https://docs.python.org/3/library/email.examples.html"""
        directorio = r'.\Output'

        msg = EmailMessage()
        msg['Subject'] = f'[Billetera Santa Fe] Transacciones {fecha_desde}'
        msg['To'] = '__DESTINATARIO__'
        msg['From'] = '__NOMBRE_REMITENTE__ <remitente@ejemplo.com>'
        msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        for filename in os.listdir(directorio):
            path = os.path.join(directorio, filename)
            if not os.path.isfile(path):
                continue
            ctype, encoding = mimetypes.guess_type(path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(path, 'rb') as fp:
                if ctype == 'text/plain':
                    with open(path) as f:
                        contenido = f.read()
                        contenido = MIMEText(contenido, 'plain')
                        msg.attach(contenido)
                msg.add_attachment(fp.read(),
                                   maintype=maintype,
                                   subtype=subtype,
                                   filename=filename)

        enviado = self.send_mail(msg)
        if enviado is True:
            print("Correo enviado con éxito")
            self.mueve_enviados(directorio)
        else:
            pass

    def send_mail(self, msg) -> bool:
        """Hace envío del correo."""
        try:
            with smtplib.SMTP('__SERVIDOR_DE_CORREO__') as s:
                s.send_message(msg)
        except Exception as e:
            print(f"Servicio de correo no disponible, error: {e}")
            exit()

        return True

    def mueve_enviados(self, directorio):
        """Mueve de directorio los archivos que ya fueron enviados por correo."""
        enviados = './Enviados'

        for filename in os.listdir(directorio):
            ruta_anterior = os.path.join(directorio, filename)
            ruta_nueva = os.path.join(enviados, filename)
            shutil.move(ruta_anterior, ruta_nueva)
