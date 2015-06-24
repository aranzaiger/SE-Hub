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

#----------------------------------------------------------
#                     POST
#----------------------------------------------------------

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
     'projectName': 'Advance Math',<br>
     'courseName': 'JCE',<br>
     'logo_url': 'http://location.domain.com/image.jpg',<br>
     'gitRepository': 'http://location.git.com/somthing'<br>
    }<br>
    <br>
    <br>
    <b>Response</b>
    <br>
    201 - Created
    <br>
    400 - Bad Request
    <br>
    403 - Invalid token or not a lecturer
    """
    if not request.data:
        return bad_request()
    try:
        payload = json.loads(request.data)
    except Exception as e:
        return bad_request("invalid JSON format")
    #if not is_lecturer(token):  #todo: change to lecturer id
     #   return forbidden("Invalid token or not a lecturer!")

    user = get_user_by_token(token)
    if user is None:
        return bad_request("Wrong user Token")

    #todo: check legality


    try:
        project = Project(projectName=payload['projectName'], courseName=payload['courseName'], master_id=user.key().id(), gitRepository=payload['gitRepository'], membersId=[token])
    except Exception as e:
        print e
        return bad_request()

    db.put(project)

    #update user projects list
    user.projects_id_list.append(str(project.key().id()))

    db.put(user)
    db.save
    return Response(response=project.to_JSON(),
                                status=200,
                                mimetype="application/json")

#----------------------------------------------------------
#                     PUT
#----------------------------------------------------------

@project_routes.route('/api/projects/joinProject/<string:token>/<string:projectId>', methods=["PUT"])
@auto.doc()
def joinProject(token, projectId):
    """
    <span class="card-title">This call will add the user (by token) to a specific project</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'<br>
        - projectId: 123456789
    <br>
    <br>
    <b>Payload</b><br>
     - None <br>
    <br>
    <b>Response</b>
    <br>
    202 - Accepted
    <br>
    400 - Bad Request
    <br>
    403 - Invalid token or not a lecturer
    """

    user = get_user_by_token(token)
    if user is None:
        return bad_request("Wrong user Token")

    project = Project.get_by_id(int(projectId))
    if project is None:
        return bad_request("No such Project")

    if user.key().id() in project.membersId:
        return no_content("User is already member in Project")

    project.membersId.append(str(user.key().id()))

    db.put(project)
    db.save

    return Response(response=project.to_JSON(),
                        status=202,
                        mimetype="application/json")



#----------------------------------------------------------
#                     GET
#----------------------------------------------------------

@project_routes.route('/api/projects/getProjectsByCourseName/<string:name>', methods=["GET"])
@auto.doc()
def getProjectsByCourseName(name):
    """
    <span class="card-title">>This Call will return an array of all projects in a given course</span>
    <br>
    <b>Route Parameters</b><br>
        - name: 'course name'
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
        'projectName': 'Advance Math',<br>
        'courseName': 'JCE',<br>
        'grade': 98,<br>
        'logo_url': 'http://location.domain.com/image.jpg',<br>
        'gitRepository': 'http://location.git.com/somthing',<br>
        'membersId': ['bob', 'dylan', 'quentin', 'terentino'],<br>
        'id' : 1234567890<br>
        }
    </code>
    <br>
    """

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



@project_routes.route('/api/projects/getProjectsByUser/<string:token>', methods=["GET"])
@auto.doc()
def getProjectsByUser(token):
    """
    <span class="card-title">>This Call will return an array of all projects in a given course</span>
    <br>
    <b>Route Parameters</b><br>
        - token: 'SEToken'
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
        'projectName': 'Advance Math',<br>
        'courseName': 'JCE',<br>
        'grade': 98,<br>
        'logo_url': 'http://location.domain.com/image.jpg',<br>
        'gitRepository': 'http://location.git.com/somthing',<br>
        'membersId': ['bob', 'dylan', 'quentin', 'terentino'],<br>
        'id' : 1234567890<br>
        }
    </code>
    <br>
    """

    user = get_user_by_token(token)
    if user is None:
        return bad_request("Bad Token")


    arr = []
    for p in user['projects_id_list']:
        project = Project.get_by_id(int(p))
        arr.append(dict(json.loads(project.to_JSON())))

    if len(arr) != 0:
        return Response(response=json.dumps(arr),
                        status=200,
                        mimetype="application/json")
    else:
        return Response(response=[],
                        status=200,
                        mimetype="application/json")



#----------------------------------------------------------
#                     DELETE
#----------------------------------------------------------



@project_routes.route('/api/projects/deleteProject/<string:token>/<string:projectId>', methods=['DELETE'])
@auto.doc()
def deleteProject(token,projectId):
    """
    <span class="card-title">This Call will delete a specific Project</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
        - projectId: 'projectid'
    <br>
    <br>
    <b>Payload</b><br>
     - NONE <br>
    <br>
    <br>
    <b>Response</b>
    <br>
    202 - Deleted Project
    <br>
    ....<br>
    {<br>
    ...<br>
    }req<br>

    ]<br>
    400 - no such Project
    <br>
    403 - Invalid token or not the owner of Project!<br>
    """

    # if not is_lecturer(token):  #todo: change to lecturer id
    #     return forbidden("Invalid token or not a lecturer!")

    user = get_user_by_token(token)
    if user is None:
        return bad_request("Bad user Token")
    p = Project.get_by_id(int(projectId))

    if p is None:
        return bad_request("no such Project")

    if p.master_id == user.key().id():
        db.delete(p)
        db.save
        return accepted("Project deleted")

    return forbidden("user is not owner of Project")




#----------------------------------------------------------
#                     DOCUMENTATION
#----------------------------------------------------------

@project_routes.route('/api/projects/help')
def documentation():
    return auto.html()