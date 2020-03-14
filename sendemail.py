import pandas as pd
import numpy as np
from flask import Flask
from flask_mail import Mail, Message
import os


def sendmail():
    data = pd.read_json(
        "quotes.json")
    data.drop(["Author", "Popularity", "Tags"], axis=1, inplace=True)
    n = len(list(data["Category"].values))
    quote = data["Quote"][np.random.randint(0, n)]

    app = Flask(__name__)

    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_PORT": 465,
        "MAIL_USERNAME": 'noreply.ardos@gmail.com',
        "MAIL_PASSWORD": 'Ardos1234',

    }

    app.config.update(mail_settings)
    mail = Mail(app)

    if __name__ == '__main__':
        with app.app_context():
            msg = Message(sender=app.config.get(
                "MAIL_USERNAME"), recipients=["sheth.bhavya06@gmail.com"])

            msg.subject = "Greetings, we have a new quote for you this week"

            msg.html = """<html><body bgcolor="#E6E6FA"><p>"""+quote+"""</p></body></html>"""

            mail.send(msg)
