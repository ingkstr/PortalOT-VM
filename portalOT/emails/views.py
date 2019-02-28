"""Función view de envio de correos"""

import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from catalogos.models import AgenteCorreo

def send_email(tomail, subject, contain):
    """Función principal de emails"""
    try:
        # Create message container - the correct MIME type is multipart/alternative.
        correo = None
        password = None
        agentes = AgenteCorreo.objects.all()
        for agente in agentes:
            correo = agente.correo
            password = agente.password


        msg = MIMEMultipart('alternative')

        msg['From'] = correo
        msg['To'] = tomail
        msg['Subject'] = subject

        # see the code below to use template as body
        body_text = contain

        # Create the body of the message (a plain-text and an HTML version).
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(contain, 'plain')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)

        # Send the message via local SMTP server.

        mail = smtplib.SMTP("smtp.outlook.office365.com", 587, timeout=20)

        # if tls = True
        mail.starttls()

        recepient = [tomail]

        mail.login(correo, password)
        mail.sendmail(correo, recepient, msg.as_string())
        mail.quit()
    except Exception as e:
        raise e
