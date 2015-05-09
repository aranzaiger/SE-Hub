__author__ = 'sagi'
from google.appengine.ext import db

class GitHubAPI_Keys():

    def __init__(self):
        self.__clientID = None
        self.__clientSecret = None
        q = KEYS.all()
        for k in q.run(limit=5):
            self.__clientID = k.client_id
            self.__clientSecret = k.client_secret
            break

    def getId(self):
        return self.__clientID

    def getSecret(self):
        return self.__clientSecret

class KEYS(db.Model):
    client_id = db.StringProperty()
    client_secret = db.StringProperty()
