import os
from threading import Thread
from datetime import datetime

from flask import current_app
from flask_mail import Message

from app import mail


def send_mail_async(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, to, text_body, html_body):
    """Send email asynchronously"""
    try:
        app = current_app._get_current_object()
        app.logger.info(
            f"[ start ] sending email; recipients: {to}; subject: {subject}"
        )

        message = Message(
            subject,
            recipients=to,
            # recipients=["hillarykamau.g@gmail.com"],
            body=text_body,
            html=html_body,
            sender=os.getenv("MAIL_DEFAULT_SENDER"),
        )
        thread = Thread(
            target=send_mail_async, args=(app, message), name="MailerThread"
        )
        thread.start()
    except Exception as e:
        app.logger.error(f"[ 500_error ] Sending mail failed; Error: {e}")
