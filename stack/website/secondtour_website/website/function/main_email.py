import smtplib
import logging
from email.message import EmailMessage
import os

EMAIL_ADDRESS = 'secondtourdubac@gmail.com'
EMAIL_PASSWORD = 'ScruMdeLamort1412!-'


def send_email(email, token):

    msg = EmailMessage()
    msg['Subject'] = 'Veuillez cliquer sur le lien pour activer votre compte'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content('''
    <!DOCTYPE html>
    <html
        style="height: 100%; width:100%; font-family:system-ui,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,'Noto Sans','Liberation Sans',sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji'">

    <body style=" height: 100%;width:100%; margin:0 0">
        <div class="main" style="width: 100%; height:100%;background-color:#4c5cff; margin-bottom:5rem">
            <div style="width: 100%; padding-top:2rem;" align="center">
                <img src="https://www.linkpicture.com/q/logo_159.png" style="width: 15%;height: auto;">
            </div>
            <div style="background-color: white; border-radius:3px 3px; margin: 3rem 3rem; padding-bottom:3rem;"
                align="center">
                <h1 style="text-align: center; color:#333333">Invitation à créer son compte</h1>
                <p style="text-align: center; color:#444444; font-size: 20px">Bonjour le lycée Vieljeux vous invite à créer
                    votre compte pour pouvoir accéder en direct à vôtre emploi
                    du temps pour le second tour du bac</p>
                <a href="''' + os.getenv("WEBSITE_URL") + '''register?token=''' + str(token) + '''"
                    style="font-size: 14px; padding: 6px 12px; margin-bottom: 0; display: inline-block; text-decoration: none; text-align: center; white-space: nowrap; vertical-align: middle;    background-image: none; border: 1px solid transparent; padding: 0.375rem 0.75rem; font-size: 1rem; border-radius: 0.25rem; color: #fff; background-color: #198754; border-color: #198754; margin: 0.25rem 0.125rem; width: 50%"
                    align="center">Cliquez
                    ici pour créer votre compte</a>
            </div>
        </div>
    </body>

    </html>
    ''', subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        logging.warning('Email envoyé à ' + email + ' | token : ' + str(token))
