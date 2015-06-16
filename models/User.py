import json

__author__ = 'Aran'
from google.appengine.ext import db

class User(db.Model):
    username = db.StringProperty(required=True)
    name = db.StringProperty(required=False)
    email = db.StringProperty(required=True)
    isLecturer = db.BooleanProperty(required=True)
    accessToken = db.StringProperty(required=True)
    seToken = db.StringProperty(required=True)
    avatar_url = db.StringProperty(required=True)
    isFirstLogin = db.BooleanProperty(default=True)
    campusName = db.StringProperty(default="")
    campuses_id_list = db.StringListProperty(default=[])
    classes_id_list = db.StringListProperty(default=[])

    def to_JSON(self):
        data = {'username' : self.username,
                'name' : self.name,
                'email' : self.email,
                'isLecturer' : self.isLecturer,
                'seToken' : self.seToken,
                'avatar_url' : self.avatar_url,
                'isFirstLogin' : self.isFirstLogin,
                'campusName': self.campusName,
                'campuses_id_list': self.campuses_id_list,
                'classes_id_list': self.classes_id_list
                }
        return json.dumps(data)
