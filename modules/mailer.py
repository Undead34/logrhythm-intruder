import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .constants import config

def send_email(message: str, subject: str = "Trend Vision One - Error Report"):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        smtp_config = config.get("smtp", None)

        if not smtp_config:
            server.quit()
            return

        username: str | None = smtp_config.get("username", None)
        password: str | None = smtp_config.get("password", None)
        recipient: str | None = smtp_config.get("report_to", None)

        if not username or not password or not recipient:
            server.quit()
            return

        mime = MIMEMultipart("alternative")
        mime["Subject"] = subject
        mime["From"] = f"Trend Vision One <{username}>"
        mime["To"] = recipient

        text = MIMEText(message, "plain")
        mime.attach(text)

        try:
            server.login(username, password)
            server.sendmail(username, recipient.split(","), mime.as_string())
        except smtplib.SMTPAuthenticationError:
            print("No se ha podido iniciar sesión en el servidor de correo.")
            print("Por favor, compruebe que el nombre de usuario y la contraseña son correctos.")
            print("Para más información, visite el siguiente enlace: https://support.google.com/mail/?p=BadCredentials")
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            server.quit()