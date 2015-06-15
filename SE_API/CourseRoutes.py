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
    This call will create a new campus in the DB
    :param token:  user seToken
    Payload
    {
     'courseName': self.courseName,
     'campusName': self.campusName,
     'projects': self.projects
     'startDate': self.startDate
     'endDate': self.endDate
     'taskFlag': self.taskFlag
    }

    :return:
    code 200
    """
    if not request.data:
        return bad_request()
    payload = json.loads(request.data)
    if not is_lecturer(token):  #todo: change to lecturer id
        return forbidden("Invalid token or not a lecturer!")

    user = get_user_by_token(token)

    #todo: check legality


    try:
        start_date = datetime.date(payload['startDate']['year'],payload['startDate']['month'],payload['startDate']['day'])
        end_date = datetime.date(payload['endDate']['year'],payload['endDate']['month'],payload['endDate']['day'])

        course = Course(courseName=payload['courseName'], campusName=payload['campusName'],
                        startDate=start_date, endDate=end_date)

        try:
            course.projects=payload['projects']
        except Exception:
            pass


    except Exception:
        return bad_request()



    db.put(course)
    db.save
    return Response(response=course.to_JSON(),
                                status=201,
                                mimetype="application/json")



@course_routes.route('/api/courses/help')
def documentation():
    return auto.html()