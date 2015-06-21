__author__ = 'Aran'


import json
from google.appengine.ext import db


class TaskComponent(db.Model):
    taskId = db.StringProperty(required=True)
    courseName = db.StringProperty(required=True)
    description = db.StringProperty(required=True,default=" ")
    dueDate = db.DateProperty(required=True)
    #isProject = db.BooleanProperty(required=False)
    isClose = db.BooleanProperty(required=True, default=False)
    isDone = db.BooleanProperty(required=True, default=False)
    taskGrade = db.IntegerProperty(required=True, default=0)

    def to_JSON(self):
        data = {'title' : self.title,
                'courseName' : self.courseName,
                'description' : self.description,
                 'dueDate' : {
                    'year': self.dueDate.year,
                    'month': self.dueDate.month,
                    'day': self.dueDate.day
                },
                #'isProject' : self.isProject,
                'isClose' : self.isClose,
                'isDone' : self.isDone,
                'taskGrade' : self.taskGrade,
                }
        return json.dumps(data)
