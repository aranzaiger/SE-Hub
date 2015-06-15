__author__ = 'Aran'

from flask import Blueprint
import json
from GithubAPI.GithubAPI import GitHubAPI_Keys

from google.appengine.ext import db
import requests
import datetime

from flask import Flask, request, render_template, redirect, abort, Response

from flask.ext.github import GitHub
from flask.ext.cors import CORS, cross_origin
from flask.ext.autodoc import Autodoc

# DB Models
from models.Project import Project

#Validation Utils Libs
from SE_API.Validation_Utils import *
from SE_API.Respones_Utils import *



project_routes = Blueprint("project_routes", __name__)
auto = Autodoc()

@project_routes.route('/api/projects/create/<string:token>', methods=['POST'])
@auto.doc()
def create_project(token):
    """
    <span class="card-title">This call will create a new project in the DB</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
    <br>
    <br>
    <b>Payload</b><br>
     - JSON Object, Example: <br>
     {<br>
     'title': 'Campus name',<br>
     'email_ending': '@campus.ac.com',<br>
     'avatar_url': 'http://location.domain.com/image.jpg'<br>
    }<br>
    <br>
    <br>
    <b>Response</b>
    <br>
    201 - Created
    <br>
    403 - Invalid Token/Forbidden
    """
    if not request.data:
        return bad_request()
    payload = json.loads(request.data)
    if not is_lecturer(token):  #todo: change to lecturer id
        return forbidden("Invalid token or not a lecturer!")

    user = get_user_by_token(token)

    #todo: check legality

    try:
        project = Project(projectName=payload['projectName'], courseName=payload['courseName'], masterId=user.key().id(), gitRepository=payload['gitRepository'], membersId=[token])
    except Exception as e:
        print e
        return bad_request()

    db.put(project)
    db.save
    return Response(response=project.to_JSON(),
                                status=201,
                                mimetype="application/json")





@project_routes.route('/api/projects/getProjectsByCourseName/<string:name>', methods=["GET"])
@auto.doc()
def getProjectsByCourseName(name):
    '''
    <span class="card-title">This Function is will Activate a user and add tha campus to it</span>
    <br>
    <b>Route Parameters</b><br>
        - validation_token: 'seToken|email_suffix'
    <br>
    <br>
    <b>Payload</b><br>
     - NONE
    <br>
    <br>
    <b>Response</b>
    <br>
    200 - JSON Example:<br>
    <code>
        {<br>
        'username' : 'github_username',<br>
        'name' : 'Bob Dylan',<br>
        'email' : 'email@domain.com',<br>
        'isLecturer' : true,<br>
        'seToken' : 'dds2d-sfvvsf-qqq-fdf33-sfaa',<br>
        'avatar_url' : 'http://location.domain.com/image.jpg',<br>
        'isFirstLogin' : false,<br>
        'campuses_id_list': ['22314','243512',...,'356'],<br>
        'classes_id_list': ['22314','243512',...,'356']<br>
        }
    </code>
    <br>
    403 - Invalid Token
    '''

    arr = []
    query = Project.all()
    query.filter("courseName = ", name)

    for p in query.run():
        arr.append(dict(json.loads(p.to_JSON())))
    print arr
    if len(arr) != 0:
        return Response(response=json.dumps(arr),
                        status=200,
                        mimetype="application/json")
    else:
        return Response(response=[],
                        status=200,
                        mimetype="application/json")




@project_routes.route('/api/projects/help')
def documentation():
    return auto.html()