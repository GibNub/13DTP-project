from flask_mail import Message
from app import app, mail


def send_email(recipient, subject, template):
    message = Message(
        subject=subject,
        recipients=[recipient],
        html=template,
        sender=app.config['DEFAULT_MAIL_SENDER']
    )
    mail.send(message)