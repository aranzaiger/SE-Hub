__author__ = 'sagi'
from google.appengine.ext import db
from models.User import User
from models.Campus import Campus
from google.appengine.api import mail


def get_user_by_token(token):
    query = User.all()
    query.filter("seToken = ", token)

    for u in query.run(limit = 1):
        return u
    return None

def get_campus_by_suffix(suffix):
    query = Campus.all()
    query.filter("email_ending = ", suffix)

    for c in query.run(limit = 1):
        return c
    return None

def is_user_token_valid(token):
    user = get_user_by_token(token)
    if user is not None:
        return True
    return False

def is_lecturer(token):
    user = get_user_by_token(token)
    if user is None:
        return False
    return user.isLecturer


def send_validation_email(token, email, name):
    emailSuffix = str(email).split('@')[1]
    message = mail.EmailMessage(sender="SE-Hub Support <se-hub@appspot.gserviceaccount.com>",
                                subject="SE-Hub Activate Account")

    message.to = email

    message.body = """
    Dear """+name+""":

    To Activate your SE-Hub Account please click on the link below:<br>
    http://se-hub.appspot.com/api/validation/confirm/"""+token+"""|"""+emailSuffix+"""
    to get access to your Campus :)

    Please let us know if you have any questions.

    SE-Hub (c) 2015 niptop Team.
    """

    message.html = """
    <html><head></head><body>
        <div>
        <center>
            <img src='https://cloud.githubusercontent.com/assets/2984053/6825467/7c9d0402-d303-11e4-9827-62a6d66f937a.png'>
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" type="text/css" rel="stylesheet" />
        </center>
        </div>
        <div style='width:70%'>
            <h1>Hey """+name+"""- Just one More Step...</h1>
            <h3>Dear """+name+""":</h3>

            To Activate your SE-Hub Account please click on the link below:<br>
            http://se-hub.appspot.com/api/validation/confirm/"""+token+"""|"""+emailSuffix+"""

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
