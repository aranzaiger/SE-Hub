import json

__author__ = 'Aran'
from google.appengine.ext import db

class Task(db.Model):
    title = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
    dueDate = db.DateProperty(required=True)
    isProject = db.BooleanProperty(required=True)
    isClose = db.BooleanProperty(required=True)
    isDone = db.BooleanProperty(required=True)
    taskGrade = db.IntegerProperty(required=True)

    def to_JSON(self):
        data = {'title' : self.title,
                'description' : self.description,
                'dueDate' : self.dueDate,
                'isProject' : self.isProject,
                'isClose' : self.membersId,
                'isDone' : self.isDone,
                'taskGrade' : self.taskGrade,
                }
        return json.dumps(data)
