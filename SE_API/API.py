__author__ = 'sagi'
import json
from GithubAPI.GithubAPI import GitHubAPI_Keys

from google.appengine.ext import db
import requests
import uuid

from flask import Flask, request, render_template, redirect, abort
# from User import User
from flask.ext.github import GitHub
from flask.ext.cors import CORS, cross_origin
from flask.ext.autodoc import Autodoc




app = Flask(__name__, static_folder='../templates')

githubKeys = GitHubAPI_Keys()

app.config['GITHUB_CLIENT_ID'] = githubKeys.getId()
app.config['GITHUB_CLIENT_SECRET'] = githubKeys.getSecret()

github = GitHub(app)
cross = CORS(app)
auto = Autodoc(app)

@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('views/404/index.html')

@app.route('/')
def wellcomePage():
    return app.send_static_file('index.html')

@app.route('/api/documentation')
def documentation():
    return auto.html()

@app.route('/home')
def returnHome():
    try:
        return app.send_static_file('views/index.html')
    except Exception:
        abort(404)



@app.route('/api/getUserByToken/<string:token>', methods=["GET"])
@auto.doc()
def getUserByToken(token):
    '''
    param: String - token: users se-Token
    return: JSON object of the user
    if no valid seToken, return message: No User Found
    '''
    query = User.all()
    query.filter("seToken = ", token)

    for u in query.run(limit=5):
        return u.to_JSON()

    return json.dumps({'message' : 'No User Found'}), 403


@app.route('/githubOAuth')
@cross_origin('*')
@github.authorized_handler
def oauth(oauth_token):
    if oauth_token is None:
        return render_template("index.html", messages={'error': 'OAuth Fail'})
    try:
        response = requests.get("https://api.github.com/user?access_token=" + oauth_token)
        user_data = json.loads(response.content)
        response = requests.get("https://api.github.com/user/emails?access_token=" + oauth_token)
        userEmails = json.loads(response.content)
    except Exception:
        return "<h1>Max Retries connection To Github</h1><p>github has aborted connection due to to many retries. you need to wait</p>"

    resault = User.all()
    resault.filter("username =", str(user_data["login"]))

    print user_data["login"]

    for u in resault.run(limit=5):
        print "Exists!!!"
        u.seToken = str(uuid.uuid4())
        u.accessToken = oauth_token
        u.put()
        return cookieMonster(u.seToken)

    if user_data["name"] == "":
        tempName = ";"
    else:
        tempName = user_data["name"]

    if user_data["email"] == "":
        for email in userEmails:
            if email["primary"] and email["verified"]:
                tempEmail = email["email"]
    else:
        tempEmail = user_data["email"]


    user = User(username=user_data["login"], name=tempName, avatar_url=user_data["avatar_url"], email=tempEmail, isLecturer=False, accsessToken=oauth_token, seToken=str(uuid.uuid4()))
    db.put(user)
    db.save
    return cookieMonster(user.seToken)




@app.route('/login')
@cross_origin('*')
def login():
    return github.authorize()




def cookieMonster(uid):
    redirect_to_home = redirect('/home')
    response = app.make_response(redirect_to_home )
    response.set_cookie('com.sehub.www',value=uid)
    return response




class User(db.Model):
    username = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    isLecturer = db.BooleanProperty(required=True)
    accsessToken = db.StringProperty(required=True)
    seToken = db.StringProperty(required=True)
    avatar_url = db.StringProperty(required=True)
    isFirstLogin = db.BooleanProperty(default=True)

    def to_JSON(self):
            return json.dumps(self, default=lambda o: o.__dict__,
                sort_keys=True, indent=4)