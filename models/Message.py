import json

__author__ = 'Aran'
from google.appengine.ext import db

class Message(db.Model):
    courseName = db.StringProperty(required=True)
    message = db.StringProperty(required=True)
    msgDate = db.DateTimeProperty(required=True)

    def to_JSON(self):
        data = {
                'courseName' : self.courseName,
                'message' : self.message,
                'date' : {
                    'year': self.msgDate.year,
                    'month': self.msgDate.month,
                    'day': self.msgDate.day,
                    'hour': self.msgDate.hour,
                    'minute': self.msgDate.minute
                },
                'id' : self.key().id()
        }
        return json.dumps(data)
