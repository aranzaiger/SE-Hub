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
from models.Task import Task
from models.Course import Course

#Validation Utils Libs
from SE_API.Validation_Utils import *
from SE_API.Respones_Utils import *




task_routes = Blueprint("task_routes", __name__)
auto = Autodoc()

@task_routes.route('/api/tasks/create/<string:token>', methods=['POST'])
@auto.doc()
def create_task(token):
    """
    <span class="card-title">This call will create a new Task in the DB</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
    <br>
    <br>
    <b>Payload</b><br>
     - JSON Object, Example: <br>
    {<br>
        'title' : self.title,<br>
        'courseName' : self.course,<br>
        'description' : self.description,<br>
        'dueDate' : self.dueDate,<br>
        'isClose' : self.membersId,<br>
        'isDone' : self.isDone,<br>
        'taskGrade' : self.taskGrade<br>
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
    payload = json.loads(request.data)
    if not is_lecturer(token):  #todo: change to lecturer id
        return forbidden("Invalid token or not a lecturer!")

    user = get_user_by_token(token)
    #TODO: add seconds and minutes
    #check the user(lecturer) is owner of the course
    # try:
    #     arr = []
    #     query = Course.all()
    #     query.filter('courseName =',payload['courseName'])
    #     for t in query.run():
    #         arr.append(dict(json.loads(t.to_JSON())))
    #     if len(arr) == 0:
    #         return bad_request("No such course")
    # except Exception as e:
    #     print e
    #     return bad_request("Missing courseName")


    #todo: check legality
    #create Task object
    try:
        #parse dueDate
        try:
            date = datetime.date(payload['dueDate']['year'],payload['dueDate']['month'],payload['dueDate']['day'])
        except Exception:
            return bad_request("invalid dueDate format")
        #TODO: add time. now, its only date

        task = Task(title=payload['title'], courseName=payload['courseName'], description=payload['description'], dueDate=date)

        #parse isClose
        try:
            task.isClose = payload['isClose']
        except Exception:
            pass

        #parse isDone
        try:
            task.isDone = payload['isDone']
        except Exception:
            pass

        #parse taskGrade
        try:
            task.taskGrade = payload['taskGrade']
        except Exception:
            pass

    except Exception as e:
        print e
        return bad_request()

    db.put(task)
    db.save
    return created()



@task_routes.route('/api/tasks/getClosestTask/<string:courseName>', methods=["GET"])
@auto.doc()
def getClosestTask(courseName):
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
        'membersId': ['bob', 'dylan', 'quentin', 'terentino']<br>
        }
    </code>
    <br>
    """
    #get all tasks for a specific course
    arr = []
    query = Task.all()
    query.filter("courseName =", courseName)
    index = -1
    count = -1
    closestDate = datetime.date(3000,1,1)
    for t in query.run():
        count+=1
        if t.dueDate < closestDate:
            closestDate = t.dueDate
            index = count
        arr.append(dict(json.loads(t.to_JSON())))

    print arr
    if len(arr) != 0:
        return Response(response=json.dumps(arr[index]),
                        status=200,
                        mimetype="application/json")
    else:
        return no_content("no Tasks")




@task_routes.route('/api/tasks/getAllTasks/<string:courseName>', methods=["GET"])
@auto.doc()
def getAllTasks(courseName):
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
        'membersId': ['bob', 'dylan', 'quentin', 'terentino']<br>
        }
    </code>
    <br>
    """

    arr = []
    query = Task.all()
    query.filter("courseName = ", courseName)

    for t in query.run():
        taskDic =dict(json.loads(t.to_JSON()))
        #add a key 'forSortDate' for sorting dates
        taskTime = datetime.datetime(taskDic['dueDate']['year'], taskDic['dueDate']['month'], taskDic['dueDate']['day'])
        taskDic['forSortDate'] = taskTime
        arr.append(taskDic)

    #sort array by date, and remove added key
    arr = sorted(arr, key=itemgetter('forSortDate'), reverse=False)
    for i in arr:
        del i['forSortDate']

    if len(arr) != 0:
        return Response(response=json.dumps(arr),
                        status=200,
                        mimetype="application/json")
    else:
        return Response(response=[],
                        status=200,
                        mimetype="application/json")



@task_routes.route('/api/tasks/help')
def documentation():
    return auto.html()