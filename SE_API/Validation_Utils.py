__author__ = 'sagi'
from google.appengine.ext import db
from models.User import User

def is_user_token_valid(token):
    query = User.all()
    query.filter("seToken = ", token)

    for u in query.run():
        return True
    return False
