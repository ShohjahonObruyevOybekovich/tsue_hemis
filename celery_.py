from celery import Celery
import smtplib, ssl

app = Celery('celery_', broker='redis://localhost:6379/0')


@app.task
def send_email(users: list):
    for user in users:
        port = 465
        smtp_server = "smtp.gmail.com"
        sender_email = "shohjahonobruyev3@gmail.com"
        receiver_email = user
        password = "nldqpjycwnsolife"
        message = """\
        Subject: Bu birinchi task.

        This message is sent from Python."""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)