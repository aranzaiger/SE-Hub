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

@project_routes.route('/api/projects/Create/<string:token>/<string:id>', methods=['POST'])
@auto.doc()
def create_project(token,id):
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
        project = Project(projectName=payload['projectName'], masterId=user.key().id(), gitRepository=payload['gitRepository'], membersId=[token])
    except Exception as e:
        print e
        return bad_request()

    db.put(project)
    db.save
    return Response(response=project.to_JSON(),
                                status=201,
                                mimetype="application/json")





@project_routes.route('/api/projects/get/<string:token>', methods=['GET'])
@auto.doc()
def get_projects(token):
    """
    <span class="card-title">This Call will return an array of all projects available</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
    <br>
    <br>
    <b>Payload</b><br>
     - NONE <br>
    <br>
    <br>
    <b>Response</b>
    <br>
    200 - JSON Array, Example:<br>
    [<br>
    {
                'title': 'JCE',<br>
                'email_ending': '@post.jce.ac.il',<br>
                'master_user_id': 123453433341, (User that created the campus)<br>
                'avatar_url': 'http://some.domain.com/imagefile.jpg'<br>
    },<br>
    ....<br>
    {<br>
    ...<br>
    }req<br>
    ]<br>
    <br>
    403 - Invalid Token<br>
    500 - Server Error
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
        return forbidden("Invalid Token")



@project_routes.route('/api/Projects/<string:token>', methods=['GET'])
@auto.doc()
def get_campuses(token):
    pass