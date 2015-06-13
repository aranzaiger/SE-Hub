import json

__author__ = 'Aran'
from google.appengine.ext import db

class Course(db.Model):
    courseName = db.StringProperty(required=True)
    campusName = db.StringProperty(required=True)
    projects = db.StringListProperty(required=True)
    startDate = db.DateProperty(required=True)
    endDate = db.DateProperty(required=False)
    taskFlag = db.BooleanProperty(required=True)

    def to_JSON(self):
        data = {'courseName' : self.courseName,
                'campusName' : self.campusName,
                'projects' : self.projects,
                'startDate' : self.startDate,
                'endDate' : self.endDate,
                'taskFlag' : self.taskFlag,
                }
        return json.dumps(data)
