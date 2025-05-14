import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.common.configuration import conf
from src.user.models import User


async def send_email(user: User, message: MIMEMultipart) -> None:
    message_data = message.as_bytes()
    try:
        with smtplib.SMTP(conf.smtp.server, conf.smtp.port) as server:
            server.starttls()
            server.login(conf.smtp.username, conf.smtp.password)
            server.sendmail(conf.smtp.username, user.email, message_data)
            logging.info(f"Email sending successfully. Email: {user.email}")
    except Exception as e:
        logging.error(f"Error sending email. Email: {user.email} Error: {e}")


async def send_password_reset_email(user: User) -> None:
    password_reset_link = f"{conf.base.domain}/restore_password/{user.reset_password_token}"

    message = MIMEMultipart("alternative")
    message["From"] = conf.smtp.username
    message["To"] = user.email
    message["Subject"] = "Смена пароля на сайте map.ncpti.ru"

    body = f"""
    <html>
        <body>
            <p>Здравствуйте, {user.name}.</p>
            <p>Ссылка для смены пароля:</p>
            <p><a href="{password_reset_link}">Изменить пароль</a></p>
        </body>
    </html>
    """

    message.attach(MIMEText(body, "html"))
    await send_email(user, message)
