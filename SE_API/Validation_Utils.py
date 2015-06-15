__author__ = 'sagi'
from google.appengine.ext import db
from models.User import User
from models.Campus import Campus



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
