import json

__author__ = 'Aran'
from google.appengine.ext import db
from models.User import User
from models.Project import Project
from models.Course import Course

class Message(db.Model):
    groupId = db.IntegerProperty(required=True)
    message = db.StringProperty(required=True)
    msgDate = db.DateTimeProperty(required=True)
    master_id = db.IntegerProperty(required=True)
    isProject = db.BooleanProperty(default=False)

    def to_JSON(self):
        user = User.get_by_id(self.master_id)
        if self.isProject:
            group = Project.get_by_id(self.groupId)
        else:
            group = Course.get_by_id(self.groupId)
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
                'user': json.loads(user.to_JSON()),
                'group': json.loads(group.to_JSON())
        }
        return json.dumps(data)
