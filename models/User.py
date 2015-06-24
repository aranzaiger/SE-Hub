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
    campusName = db.StringProperty(required=True, default=" ")
    campuses_id_list = db.StringListProperty(default=[])
    courses_id_list = db.StringListProperty(default=[])
    projects_id_list = db.StringListProperty(default=[])

    def to_JSON(self):
        data = {'username' : self.username,
                'name' : self.name,
                'email' : self.email,
                'isLecturer' : self.isLecturer,
                'avatar_url' : self.avatar_url,
                'isFirstLogin' : self.isFirstLogin,
                'campusName': self.campusName,
                'campuses_id_list': self.campuses_id_list,
                'courses_id_list': self.courses_id_list,
                'projects_id_list': self.projects_id_list
                }
        return json.dumps(data)
