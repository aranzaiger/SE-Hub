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
from models.User import User
from models.Course import Course

#Validation Utils Libs
from SE_API.Validation_Utils import *
from SE_API.Respones_Utils import *


user_routes = Blueprint("user_routes", __name__)
auto = Autodoc()




#----------------------------------------------------------
#                     POST
#----------------------------------------------------------

#----------------------------------------------------------
#                     PUT
#----------------------------------------------------------

@user_routes.route('/api/users/updateUser/<string:token>', methods=["PUT"])
@auto.doc()
def updateUser(token):
    """
    <span class="card-title">>This Call will update user details</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
    <br>
    <br>
    <b>Payload</b><br>
     - JSON Object, Example: <br>
     {<br>
         'name': 'new name',<br>
         'isLecturer': true,<br>
         'campusName': 'JCE'<br>
    }<br>
    <br>
    <b>Response</b>
    <br>
    200 - User updated
    <br>
    400 - Bad Request
    """

    if not request.data:
        return bad_request()

    try:
        payload = json.loads(request.data)
    except Exception as e:
        return bad_request()

    user = get_user_by_token(token)
    if user is None:
        return bad_request("Not a user!")

    try:
        user.name = payload['name']
    except Exception:
        pass

    try:
        user.campusName = payload['campusName']
    except Exception:
        pass

    try:
        user.isLecturer = payload['isLecturer']
    except Exception as e:
        print e

    db.put(user)
    db.save
    return ok("User updated")

@user_routes.route('/api/users/addUserToCourse/<string:token>', methods=["PUT"])
@auto.doc()
def addUserToCourse(token):
    """
    <span class="card-title">>This Call will add a course to user course list</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
    <br>
    <br>
    <b>Payload</b><br>
     - JSON Object, Example: <br>
     {<br>
         'courseId': 1234567890<br>
    }<br>
    <br>
    <b>Response</b>
    <br>
    200 - User updated
    <br>
    400 - Bad Request
    """

    if not request.data:
        return bad_request()

    try:
        payload = json.loads(request.data)
    except Exception as e:
        return bad_request()

    #check user exists
    user = get_user_by_token(token)
    if user is None:
        return bad_request("Not a user!")

    #check course Exists
    course = Course.get_by_id(payload['coursesId'])
    if course is None:
        return bad_request("No such Course!")

    try:
        user.courses_id_list.append(payload['coursesId'])
    except Exception as e:
        print e
        return bad_request()

    db.put(user)
    db.save
    return Response(response=user.to_JSON(),
                        status=200,
                        mimetype="application/json")  # Real response!




@user_routes.route('/api/users/addUserToCampus/<string:token>', methods=["PUT"])
@auto.doc()
def addUserToCampus(token):
    """
    <span class="card-title">>This Call will add a Campus to user Campus list</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
    <br>
    <br>
    <b>Payload</b><br>
     - JSON Object, Example: <br>
     {<br>
         'campusId': 1234567890<br>
    }<br>
    <br>
    <b>Response</b>
    <br>
    200 - User updated
    <br>
    400 - Bad Request
    """

    if not request.data:
        return bad_request()

    try:
        payload = json.loads(request.data)
    except Exception as e:
        print e
        return bad_request()

    if not is_lecturer(token):  #todo: change to lecturer id
        return forbidden("Invalid token or not a lecturer!")

    user = get_user_by_token(token)

    #check Campus Exists
    campus = Campus.get_by_id(payload['campusId'])
    if campus is None:
        return bad_request("No such Campus!")

    try:
        if str(payload['campusId']) in  user.campuses_id_list:
            return accepted("Already a member of that campus")

        user.campuses_id_list.append(str(payload['campusId']))
    except Exception as e:
        print e
        return bad_request()


    db.put(user)
    db.save
    return Response(response=user.to_JSON(),
                            status=200,
                            mimetype="application/json")  # Real response!


#----------------------------------------------------------
#                     GET
#----------------------------------------------------------


@user_routes.route('/api/users/getUserByToken/', defaults={'token': None})
@user_routes.route('/api/users/getUserByToken/<string:token>', methods=["GET"])
@auto.doc()
def getUserByToken(token):
    """
    <span class="card-title">>This Call will return a user by a given token</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
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
        'username': 'DarkLord',<br>
        'name': 'Darth Vader',<br>
        'email': 'darkLord@death.planet,<br>
        'isLecturer': 'True',<br>
        'seToken': 'xxxxxx-xxxxx-xxxxx-xxxxxx',<br>
        'avatar_url': 'http://location.git.com/somthing'<br>
        'isFirstLogin': False,<br>
        'campuses_id_list': [{<br>
                            'master_user_id': 111,<br>
                            'id': 5629499534213120,<br>
                            'email_ending': "@post.jce.ac.il",<br>
                            'avatar_url': "https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg",<br>
                            'title': "JCE"
            }],<br>
        'courses_id_list': ['a','b','c']<br>
        }
    </code>
    <br>
    403 - No User Found
    """
    if token is None:
        return no_content("Token Is Empty, No User Found")

    query = User.all()
    query.filter("seToken =", token)

    for u in query.run(limit=5):
        for index, c in enumerate(u.campuses_id_list):
            c = json.loads(Campus.get_by_id(int(c)).to_JSON())
            u.campuses_id_list[index] = c

        return Response(response=u.to_JSON(),
                        status=200,
                        mimetype="application/json")  # Real response!

    return no_content("No User Found")

@user_routes.route('/api/users/getUserById/', defaults={'token': None, 'id': None})
@user_routes.route('/api/users/getUserById/<string:token>/<string:id>', methods=["GET"])
@auto.doc()
def getUserById(token, id):
    """
    <span class="card-title">>This Call will return a user by a given UserId</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
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
        'username': 'DarkLord',<br>
        'name': 'Darth Vader',<br>
        'email': 'darkLord@death.planet,<br>
        'isLecturer': 'True',<br>
        'seToken': 'xxxxxx-xxxxx-xxxxx-xxxxxx',<br>
        'avatar_url': 'http://location.git.com/somthing'<br>
        'isFirstLogin': False,<br>
        'campuses_id_list': [{<br>
                            'master_user_id': 111,<br>
                            'id': 5629499534213120,<br>
                            'email_ending': "@post.jce.ac.il",<br>
                            'avatar_url': "https://yt3.ggpht.com/--ZkWxybWGOM/AAAAAAAAAAI/AAAAAAAAAAA/_nAICC_kzzI/s88-c-k-no/photo.jpg",<br>
                            'title': "JCE"
            }],<br>
        'courses_id_list': ['a','b','c'],<br>
        'id': 234253523<br>
        }<br>
    </code>
    <br>
    403 - No User Found
    """
    if token is None or id is None:
        return no_content("No Token/ID, No User Found")

    if get_user_by_token(token) is None:
        return forbidden('Invalid Token')

    u = get_user_by_id(int(id))
    if u is None:
        return no_content('No user Found')

    for index, c in enumerate(u.campuses_id_list):
        c = json.loads(Campus.get_by_id(int(c)).to_JSON())
        u.campuses_id_list[index] = c

        return Response(response=u.to_JSON(),
                        status=200,
                        mimetype="application/json")  # Real response!

    return no_content("No User Found")



#----------------------------------------------------------
#                     DELETE
#----------------------------------------------------------

@user_routes.route('/api/users/removeUserFromCampus/<string:token>/<string:campusId>', methods=["PUT"])
@auto.doc()
def removeUserFromCampus(token, campusId):
    """
    <span class="card-title">>This Call will remove a Campus from a user Campus list</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
        - 'campusId': 1234567890<br>
    <br>
    <br>
    <b>Payload</b><br>
     - NONE
     {<br>
    }<br>
    <br>
    <b>Response</b>
    <br>
    200 - User updated
    <br>
    400 - Bad Request
    """

    if not request.data:
        return bad_request()

    try:
        payload = json.loads(request.data)
    except Exception as e:
        return bad_request()

    if not is_lecturer(token):  #todo: change to lecturer id
        return forbidden("Invalid token or not a lecturer!")

    user = get_user_by_token(token)

    #check Campus Exists
    campus = Campus.get_by_id(int(campusId))
    if campus is None:
        return bad_request("No such Campus!")

    #check if user is owner of Campus
    if user.key().id() != campus.master_user_id:
        return forbidden("Lecturer is not owner of course")

    try:
        user.campuses_id_list.remove(campusId)
    except Exception as e:
        print e
        return bad_request("user is not listed to this campus")

    db.put(user)
    db.save
    return Response(response=user.to_JSON(),
                            status=200,
                            mimetype="application/json")  # Real response!





# @user_routes.route('/api/users/removeUserFromCourse/<string:token>/<string:courseId>', methods=["PUT"])
# @auto.doc()
# def removeUserFromCourse(token, courseId):
#     """
#     <span class="card-title">>This Call will remove a Course from a user Campus list</span>
#     <br>
#     <b>Route Parameters</b><br>
#         - seToken: 'seToken'
#         - 'courseId': 1234567890<br>
#     <br>
#     <br>
#     <b>Payload</b><br>
#      - NONE
#      {<br>
#     }<br>
#     <br>
#     <b>Response</b>
#     <br>
#     200 - User updated
#     <br>
#     400 - Bad Request
#     """
#
#     if not request.data:
#         return bad_request()
#
#     try:
#         payload = json.loads(request.data)
#     except Exception as e:
#         return bad_request()
#
#     user = get_user_by_token(token)
#     if user is None:
#         return bad_request("No such user!")
#
#
#     #check Course Exists
#     course = Course.get_by_id(int(courseId))
#     if course is None:
#         return bad_request("No such Course!")
#
#     #check if user is owner of Campus
#     if user.key().id() != course.master_id:
#         return forbidden("Lecturer is not owner of course")
#
#     try:
#         user.campuses_id_list.remove(campusId)
#     except Exception as e:
#         print e
#         return bad_request("user is not listed to this campus")
#
#     db.put(user)
#     db.save
#     return Response(response=user.to_JSON(),
#                             status=200,
#                             mimetype="application/json")  # Real response!
#
#



#----------------------------------------------------------
#                     DOCUMENTATION
#----------------------------------------------------------

@user_routes.route('/api/users/help')
def documentation():
    return auto.html()