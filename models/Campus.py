__author__ = 'sagi'

import json

from google.appengine.ext import db

class Campus(db.Model):
    title = db.StringProperty(required=True)
    avatar_url = db.StringProperty(required=True)
    email_ending = db.StringProperty(required=True)
    master_user_id = db.IntegerProperty(required=True)

    def to_JSON(self):
        dick = {'title': self.username,
                'email_ending': self.email_ending,
                'master_user_id': self.master_user_id,
                'avatar_url': self.avatar_url
                }
        return json.dumps(dick)


"""
DEBUG Script - To create a campus:

"""