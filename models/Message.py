import json

__author__ = 'Aran'
from google.appengine.ext import db
from models.User import User

class Message(db.Model):
    groupId = db.IntegerProperty(required=True)
    message = db.StringProperty(required=True)
    msgDate = db.DateTimeProperty(required=True)
    master_id = db.IntegerProperty(required=True)
    isProject = db.BooleanProperty(default=False)

    def to_JSON(self):
        user = User.get_by_id(self.master_id)
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
                'isProject' : self.isProject,
                'user': json.loads(user.to_JSON())
        }
        return json.dumps(data)
