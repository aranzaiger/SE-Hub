import json

__author__ = 'Aran'
from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    isLecturer = db.BooleanProperty(required=True)
    accessToken = db.StringProperty(required=True)
    seToken = db.StringProperty(required=True)
    avatar_url = db.StringProperty(required=True)
    isFirstLogin = db.BooleanProperty(default=True)
    campuses_id_list = db.StringListProperty()
    classes_id_list = db.StringListProperty()

    def to_JSON(self):
        data = {'username' : self.username,
                'name' : self.name,
                'email' : self.email,
                'isLecturer' : self.isLecturer,
                'seToken' : self.seToken,
                'avatar_url' : self.avatar_url,
                'isFirstLogin' : self.isFirstLogin,
                'campuses_id_list': self.campuses_id_list,
                'classes_id_list': self.classes_id_list
                }
        return json.dumps(data)
