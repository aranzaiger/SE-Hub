import json

__author__ = 'Aran'
from google.appengine.ext import db

class Task(db.Model):
    title = db.StringProperty(required=True)
    courseName = db.StringProperty(required=True)
    description = db.StringProperty(required=True,default=" ")
    dueDate = db.DateProperty(required=True)
    isProject = db.BooleanProperty(required=True)
    isClose = db.BooleanProperty(required=True, default=False)
    isDone = db.BooleanProperty(required=True, default=False)
    taskGrade = db.IntegerProperty(required=True, default=0)

    def to_JSON(self):
        data = {'title' : self.title,
                'courseName' : self.course,
                'description' : self.description,
                'dueDate' : self.dueDate,
                'isProject' : self.isProject,
                'isClose' : self.membersId,
                'isDone' : self.isDone,
                'taskGrade' : self.taskGrade,
                }
        return json.dumps(data)
