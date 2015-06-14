import json

__author__ = 'Aran'
from google.appengine.ext import db

class Project(db.Model):
    projectName = db.StringProperty(required=True)
    masterId = db.IntegerProperty(required=True)
    grade = db.IntegerProperty(required=True, default=0)
    logo_url = db.StringProperty(required=False)
    gitRepository = db.StringProperty(required=True)
    membersId = db.StringListProperty(required=True)

    def to_JSON(self):
        data = {'projectName' : self.projectName,
                'masterId' : self.masterId,
                'grade' : self.grade,
                'logo_url' : self.logo_url,
                'gitRepository' : self.gitRepository,
                'membersId' : self.membersId,
                }
        return json.dumps(data)
