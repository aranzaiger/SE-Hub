import json
import time
__author__ = 'Aran'
from google.appengine.ext import db


class Task(db.Model):
    title = db.StringProperty(required=True)
    courseId = db.IntegerProperty(required=True)
    description = db.StringProperty(required=True,default=" ")
    dueDate = db.DateProperty(required=True)
    isPersonal = db.BooleanProperty(required=True, default=True)

    def to_JSON(self):
        data = {'title' : self.title,
                'courseId' : self.courseId,
                'description' : self.description,
                'dueDate' : {
                    'year': self.dueDate.year,
                    'month': self.dueDate.month,
                    'day': self.dueDate.day
                },
                'isPersonal' : self.isPersonal,
                'id' : self.key().id()
                }
        return json.dumps(data)

