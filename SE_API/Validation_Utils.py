__author__ = 'sagi'
from google.appengine.ext import db
from models.User import User
from google.appengine.api import mail


def is_user_token_valid(token):
    query = User.all()
    query.filter("seToken = ", token)

    for u in query.run():
        return True
    return False

def send_validation_email(token, email, name):
    message = mail.EmailMessage(sender="SE-Hub Support <se-hub@appspot.gserviceaccount.com>",
                            subject="SE-Hub Activate Account")

    message.to = email

    message.body = """
    Dear """+name+""":

    To Activate your SE-Hub Account please click on the link below:<br>
    http://se-hub.appspot.com/api/validatation/confirm/"""+token+"""
    to access you virtual class.

    Please let us know if you have any questions.

    SE-Hub (c) 2015 niptop Team.
    """

    message.html = """
    <html><head></head><body>
        <div>
        <center>
            <img src='https://cloud.githubusercontent.com/assets/2984053/6825467/7c9d0402-d303-11e4-9827-62a6d66f937a.png'>
        </center>
        </div>
        <div style='width:70%'>
            <h1>Hey """+name+"""- Just one More Step...</h1>
            <h3>Dear """+name+""":</h3>

            To Activate your SE-Hub Account please click on the link below:<br>
            http://se-hub.appspot.com/api/validatation/confirm/"""+token+"""<br><br>

            to access you virtual class.
        </div>
        <br><br>
        Please let us know if you have any questions.
        <br>
        SE-Hub (c) 2015 niptop Team.
    </body>
    </html>
    """

    message.send()
