__author__ = 'sagi'

import json

from google.appengine.ext import db

class Campus(db.Model):
    title = db.StringProperty(required=True)
    avatar_url = db.StringProperty(required=True)
    email_ending = db.StringProperty(required=True)
    master_user_id = db.IntegerProperty(required=True)
    membersId = db.StringListProperty(required=True, default=[])


    def to_JSON(self):
        data = {'title': self.title,
                'email_ending': self.email_ending,
                'master_user_id': self.master_user_id,
                'avatar_url': self.avatar_url,
                'membersId': self.membersId,
                'id' : self.key().id()
                }
        return json.dumps(data)


"""
DEBUG Script - To create a campus:
"""
is_jce_in = False
query = Campus.all()
query.filter('title =', 'JCE')
for c in query.run():
    is_jce_in = True
if not is_jce_in:
    jce = Campus(title='JCE', email_ending='@post.jce.ac.il', master_user_id=111, avatar_url='https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg')
    db.put(jce)