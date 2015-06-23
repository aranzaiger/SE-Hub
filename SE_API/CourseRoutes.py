__author__ = 'Aran'

from flask import Blueprint
import json
from GithubAPI.GithubAPI import GitHubAPI_Keys

from google.appengine.ext import db
import requests
import datetime
from operator import itemgetter


from flask import Flask, request, render_template, redirect, abort, Response

from flask.ext.github import GitHub
from flask.ext.cors import CORS, cross_origin
from flask.ext.autodoc import Autodoc

# DB Models
from models.Course import Course
from models.Campus import Campus
from models.Message import Message

#Validation Utils Libs
from SE_API.Validation_Utils import *
from SE_API.Respones_Utils import *



course_routes = Blueprint("course_routes", __name__)
auto = Autodoc()



#----------------------------------------------------------
#                     POST
#----------------------------------------------------------
@course_routes.route('/api/courses/create/<string:token>', methods=['POST'])
@auto.doc()
def create_course(token):
    """
    <span class="card-title">This call will create a new course in the DB</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
    <br>
    <br>
    <b>Payload</b><br>
     - JSON Object, Example: <br>
     {<br>
     'courseName': 'Advance Math',<br>
     'campusName': 'JCE',<br>
     'startDate': {'year': 2015, 'month' : 4, 'day' : 3}<br>
     'endDate': {'year': 2016, 'month' : 5, 'day' : 14}<br>
     'taskFlag': false<br>
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
        return bad_request("no data")
    if not is_lecturer(token):  #todo: change to lecturer id
        return forbidden("Invalid token or not a lecturer!")

    user = get_user_by_token(token)

    #try to parse payload
    try:
        payload = json.loads(request.data)
    except Exception as e:
        return bad_request()

    try:
        start_date = datetime.date(payload['startDate']['year'],payload['startDate']['month'],payload['startDate']['day'])
        end_date = datetime.date(payload['endDate']['year'],payload['endDate']['month'],payload['endDate']['day'])

        if end_date <= start_date:
            return bad_request("end date cant be before (or same day) start date")

        course = Course(courseName=payload['courseName'], campusName=payload['campusName'], master_id=user.key().id(),
                        startDate=start_date, endDate=end_date)
        #check if name already exists
        try:
            query = Course.all()
            query.filter("courseName = ", payload['courseName'])
            for c in query.run(limit=1):
                return forbidden("Course with same name already exists")
        except Exception as e:
            print e


    except Exception as e:
        print e
        return bad_request()

    db.put(course)
    db.save
    return Response(response=course.to_JSON(),
                                status=201,
                                mimetype="application/json")




@course_routes.route('/api/courses/createMessage/<string:token>', methods=['POST'])
@auto.doc()
def createMessage(token):
    """
    <span class="card-title">This call will create a new Message in the DB</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
    <br>
    <br>
    <b>Payload</b><br>
     - JSON Object, Example: <br>
     {<br>
     'courseName': 'Advance Math',<br>
     'message': 'The lecture today is canceled'<br>
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
        return bad_request("no data")
    if not is_lecturer(token):  #todo: change to lecturer id
        return forbidden("Invalid token or not a lecturer!")

    user = get_user_by_token(token)

    #try to parse payload
    try:
        payload = json.loads(request.data)
    except Exception as e:
        return bad_request("here")

    try:
        msg = Message(courseName=payload['courseName'], message=payload['message'], msgDate=datetime.datetime.now())
    except Exception as e:
        print e
        return bad_request("there")

    db.save(msg)
    db.save
    return created()



#----------------------------------------------------------
#                     GET
#----------------------------------------------------------


@course_routes.route('/api/courses/getCourseByCampusName/<string:name>', methods=["GET"])
@auto.doc()
def getCourseByCampusName(name):
    """
    <span class="card-title">>This Call will return an array of all courses in a given campus</span>
    <br>
    <b>Route Parameters</b><br>
        - name: 'campus name'
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
        'courseName': 'Advance Math',<br>
        'campusName': 'JCE',<br>
        'startDate': '2015-14-3'<br>
        'endDate': '2015-29-6'<br>
        'taskFlag': 'False'<br>
        'id' : 1234567890<br>

        }
    </code>
    <br>
    """
    arr = []
    query = Course.all()
    query.filter("campusName=", name)

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

@course_routes.route('/api/courses/getMessagesByCourseName/<string:name>', methods=["GET"])
@auto.doc()
def getMessagesByCourseName(name):
    """
    <span class="card-title">>This Call will return an array of all courses in a given campus</span>
    <br>
    <b>Route Parameters</b><br>
        - name: 'campus name'
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
        'courseName': 'Advance Math',<br>
        'campusName': 'JCE',<br>
        'startDate': '2015-14-3'<br>
        'endDate': '2015-29-6'<br>
        'taskFlag': false,<br>
        'id' : 1234567890<br>

        }
    </code>
    <br>
    """
    arr = []
    query = Message.all()
    query.filter("courseName = ", name)

    for m in query.run():
        msgDic = dict(json.loads(m.to_JSON()))
        #add a key 'forSortDate' for sorting dates
        msgTime = datetime.datetime(msgDic['date']['year'], msgDic['date']['month'], msgDic['date']['day'], msgDic['date']['hour'], msgDic['date']['minute'])
        msgDic['forSortDate'] = msgTime
        arr.append(msgDic)

    arr = sorted(arr, key=itemgetter('forSortDate'), reverse=False)
    for i in arr:
        del i['forSortDate']
    print arr

    if len(arr) != 0:
        return Response(response=json.dumps(arr),
                        status=200,
                        mimetype="application/json")
    else:
        return Response(response=[],
                        status=200,
                        mimetype="application/json")

#----------------------------------------------------------
#                     PUT
#----------------------------------------------------------




#----------------------------------------------------------
#                     DELETE
#----------------------------------------------------------



@course_routes.route('/api/courses/deleteCourse/<string:token>/<string:courseid>', methods=['DELETE'])
@auto.doc()
def deleteCourse(token,courseid):
    """
    <span class="card-title">This Call will delete a specific Course</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
        - courseid: 'courseid'
    <br>
    <br>
    <b>Payload</b><br>
     - NONE <br>
    <br>
    <br>
    <b>Response</b>
    <br>
    202 - Deleted Course
    <br>
    ....<br>
    {<br>
    ...<br>
    }req<br>

    ]<br>
    400 - no such Course
    <br>
    403 - Invalid token or not a lecturer or lecturer is not owner of Course!<br>
    """

    if not is_lecturer(token):  #todo: change to lecturer id
        return forbidden("Invalid token or not a lecturer!")

    user = get_user_by_token(token)
    c = Course.get_by_id(int(courseid))

    if c is None:
        return bad_request("no such course")


    if c.master_id == user.key().id():
        db.delete(c)
        db.save
        return accepted("course deleted")

    return forbidden("lecturer is not owner of course")


@course_routes.route('/api/courses/deleteCoursesByCampus/<string:token>/<string:campusName>', methods=['DELETE'])
@auto.doc()
def deleteCoursesByCampus(token,campusName):
    """
    <span class="card-title">This Call will delete a specific campus's courses</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
        - title: 'campusName'
    <br>
    <br>
    <b>Payload</b><br>
     - NONE <br>
    <br>
    <br>
    <b>Response</b>
    <br>
    202 - Deleted campus
    <br>
    204 - No Matching Campus Found
    <br>
    ....<br>
    {<br>
    ...<br>
    }req<br>

    ]<br>
    400 - Bad Request
    <br>
    403 - Invalid token or not a lecturer!<br>
    """

    if not is_lecturer(token):  #todo: change to lecturer id
        return forbidden("Invalid token or not a lecturer!")


    user = get_user_by_token(token)
    campus = get_campus_by_campusName(campusName)
    if campus is None:
        return bad_request("Not a campus!")

    #check user is owner of campus
    if campus.master_user_id != user.key().id():
        return forbidden("lecturer is not owner of campus!")

    query = Course.all()

    try:
        query.filter('campusName =', campusName)
    except Exception as e:
        print e
        return bad_request("invalid course title attribute")

    for c in query.run():
        db.delete(c)
        db.save

    return no_content()



#----------------------------------------------------------
#                     DOCUMENTATION
#----------------------------------------------------------

@course_routes.route('/api/courses/help')
def documentation():
    return auto.html()