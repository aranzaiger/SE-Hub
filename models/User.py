import json

__author__ = 'Aran'
from google.appengine.ext import db


class User(db.Model):
    username = db.StringProperty(required=True)
    name = db.StringProperty(required=False)
    email = db.StringProperty(required=True)
    isLecturer = db.BooleanProperty(required=True)
    accessToken = db.StringProperty(required=True)
    seToken = db.StringProperty(required=True)
    avatar_url = db.StringProperty(required=True)
    isFirstLogin = db.BooleanProperty(default=True)
    campuses_id_list = db.StringListProperty(default=[])
    courses_id_list = db.StringListProperty(default=[])
    projects_id_list = db.StringListProperty(default=[])

    def to_JSON(self):
        data = {'username' : self.username,
                'name' : self.name,
                'email' : self.email,
                'isLecturer' : self.isLecturer,
                'avatar_url' : self.avatar_url,
                'isFirstLogin' : self.isFirstLogin,
                'campuses_id_list': self.campuses_id_list,
                'courses_id_list': self.courses_id_list,
                'projects_id_list': self.projects_id_list,
                'id' : self.key().id(),
                'stats': get_stats(self)
                }
        return json.dumps(data)

def get_stats(user):
    from models.Project import Project
    from models.Message import Message
    labels = ['Commits', 'Open Issues Assigned', 'Messages', 'Unfinished Tasks']
    data = [0, 0, 0, 0]
    for pid in user.projects_id_list:
        project = Project.get_by_id(int(pid))
        info = json.loads(project.info)
        stats = info["stats"]['micro']
        p_data = stats['data']
        p_series = stats['series']
        user_index = p_series.index(user.username)
        #adding commits
        data[0] = data[0] + p_data[user_index][0]
        #adding open issues
        data[1] = data[1] + p_data[user_index][1]
    messages = Message.all().filter('master_id =', user.key().id())
    for m in messages.run():
        data[2] = data[2] + 1

    #need to do tasks
    ####

    data = [data]
    return {'data': data, 'labels': labels}

"""
info: Object
commits: Array[30]
info: Object
issues: Array[7]
stats: Object
macro: Object
micro: Object
data: Array[4]
0: Array[2]
0: 13
1: 1
length: 2
__proto__: Array[0]
1: Array[2]
2: Array[2]
3: Array[2]
length: 4
__proto__: Array[0]
labels: Array[2]
0: "Commits"
1: "Open Issues"
length: 2
__proto__: Array[0]
series: Array[4]
0: "etyemy"
1: "devMatan"
2: "aranzaiger"
3: "sagidayan"
"""