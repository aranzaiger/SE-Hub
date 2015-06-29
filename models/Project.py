import json

__author__ = 'Aran'
from google.appengine.ext import db

class Project(db.Model):
    projectName = db.StringProperty(required=True)
    courseId = db.IntegerProperty(required=True)
    master_id = db.IntegerProperty(required=True)
    grade = db.IntegerProperty(required=True, default=0)
    logo_url = db.StringProperty(required=False)
    gitRepository = db.StringProperty(required=True)
    membersId = db.StringListProperty(required=True)

    def to_JSON(self):
        data = {'projectName' : self.projectName,
                'courseId' : self.courseId,
                'master_id' : self.master_id,
                'grade' : self.grade,
                'logo_url' : self.logo_url,
                'gitRepository' : self.gitRepository,
                'membersId' : self.membersId,
                'id' : self.key().id()
                }
        return json.dumps(data)
