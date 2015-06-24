import json

__author__ = 'Aran'
from google.appengine.ext import db

class Message(db.Model):
    groupId = db.IntegerProperty(required=True)
    message = db.StringProperty(required=True)
    msgDate = db.DateTimeProperty(required=True)
    master_id = db.IntegerProperty(required=True)
    isProject = db.BooleanProperty(default=False)

    def to_JSON(self):
        data = {
                'groupId' : self.groupId,
                'message' : self.message,
                'date' : {
                    'year': self.msgDate.year,
                    'month': self.msgDate.month,
                    'day': self.msgDate.day,
                    'hour': self.msgDate.hour,
                    'minute': self.msgDate.minute
                },
                'id' : self.key().id(),
                'master_id' : self.master_id,
                'isProject' : self.isProject
        }
        return json.dumps(data)
