import smtplib
from email.message import EmailMessage


from celery import Celery

from config import SMTP_USER, SMTP_PASS

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465


celeryApp = Celery(broker='redis://localhost:6379')


def get_email_template(username: str):
    print('Form email')
    email = EmailMessage()
    email['Subject'] = 'SMTP test'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(f'<div><h1 style="color:red">Hello {username}</h1></div>', subtype='html')
    return email


@celeryApp.task
def send_email_report(username: str):
    email = get_email_template(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        print('Send email')
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)
