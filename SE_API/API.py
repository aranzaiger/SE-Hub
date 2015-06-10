__author__ = 'sagi'
import json
from GithubAPI.GithubAPI import GitHubAPI_Keys

from google.appengine.ext import db
import requests
import uuid

from flask import Flask, request, render_template, redirect, abort, Response

from flask.ext.github import GitHub
from flask.ext.cors import CORS, cross_origin
from flask.ext.autodoc import Autodoc

# DB Models
from models.User import User
from models.Campus import Campus

#Validation Utils Libs
from SE_API.Validation_Utils import *




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

@app.route('/api/help')
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
        return Response(response=u.to_JSON(),
                    status=201,
                    mimetype="application/json")  # Real response!

    return Response(response=json.dumps({'message' : 'No User Found'}),
                    status=400,
                    mimetype="application/json")



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

    tempName = ";"

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


@app.route('/api/Campuses/<string:token>', methods=['GET'])
@auto.doc()
def get_campuses(token):
    """
    This Call will return an array of all Campuses available
    :param token: user seToken
    :return:
    code 200:
    [
    {
                'title': 'JCE',
                'email_ending': '@post.jce.ac.il',
                'master_user_id': 123453433341, (User that created the campus)
                'avatar_url': 'http://some.domain.com/imagefile.jpg'
    },
    ....
    {
    ...
    }
    ]

    code 403: Forbidden - Invalid Token
    code 500: internal server error
    """
    if is_user_token_valid(token):
        arr = []
        query = Campus.all()
        for c in query.run():
            arr.append(dict(json.loads(c.to_JSON())))
        print arr
        if len(arr) != 0:
            return Response(response=json.dumps(arr),
                            status=200,
                            mimetype="application/json")
        else:
            return Response(response=[],
                            status=200,
                            mimetype="application/json")
    else:
        return Response(response=json.dumps({'message': 'Invalid Token'}),
                        status=403,
                        mimetype="application/json")



@app.route('/login')
@cross_origin('*')
def login():
    return github.authorize()




def cookieMonster(uid):
    redirect_to_home = redirect('/home')
    response = app.make_response(redirect_to_home )
    response.set_cookie('com.sehub.www',value=uid)
    return response
