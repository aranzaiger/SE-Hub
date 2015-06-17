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
from models.Course import Course

#Validation Utils Libs
from SE_API.Validation_Utils import *
from SE_API.Respones_Utils import *



course_routes = Blueprint("course_routes", __name__)
auto = Autodoc()


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
        }
    </code>
    <br>
    """
    arr = []
    query = Course.all()
    query.filter("campusName = ", name)

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


@course_routes.route('/api/courses/help')
def documentation():
    return auto.html()