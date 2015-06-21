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
from models.TaskComponent import TaskComponent

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
        "title":"task1",<br>
        "courseName":"aran",<br>
        "description":"pls fddfsdfdsk",<br>
        "dueDate":{"year":2010,<br>
                    "month":2,<br>
                    "day":4<br>
                    },
        "isPersonal":true,<br>
        "components":[<br>
                {<br>
                "type" : "should be type1",<br>
                "label" : "should be label1",<br>
                "isMandatory" : true,<br>
                "order" : 1<br>
                },<br>
                {<br>
                "type" : "should be type2",<br>
                "label" : "should be label2",<br>
                "isMandatory" : true,<br>
                "order" : 2<br>
                },<br>
                {<br>
                "type" : "should be type3",<br>
                "label" : "should be label3",<br>
                "isMandatory" : false,<br>
                "order" : 3<br>
                }<br>
        ]<br>
}
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

        task = Task(title=payload['title'], courseName=payload['courseName'], description=payload['description'], dueDate=date)

        # print "id: ",task.key().id()
        #parse isPersonal
        try:
            task.isPersonal = payload['isPersonal']
        except Exception:
            pass
    except Exception as e:
        print e
        return bad_request()
    db.put(task)
    db.save

    #create components
    for c in payload['components']:
        try:
            component = TaskComponent(taskId=task.key().id(), userId=-1, type=c['type'], label=c['label'], isMandatory=c['isMandatory'], order=c['order'])
        except Exception as e:
            print e
            return bad_request("Bad component")
        db.put(component)
        db.save



    return created()






@task_routes.route('/api/tasks/getAllTasks/<string:courseName>', methods=["GET"])
@auto.doc()
def getAllTasks(courseName):
    """
    <span class="card-title">>This Call will return an array of all Tasks in a course by date</span>
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
        'title' : 'Task1',<br>
        'courseName' : 'advance Math',<br>
        'description' : 'prepare by sunday',<br>
        'dueDate' : {
                    'year' : 2015,
                    'month' : 12,
                    'day' : 23
                    }<br>
        'isPersonal' : true,<br>
        'task_id' : 589689456894<br>
    }<br>
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
        return no_content()


@task_routes.route('/api/tasks/getTaskComponents/<string:taskId>', methods=["GET"])
@auto.doc()
def getTaskComponents(taskId):
    """
    <span class="card-title">>This Call will return an array of all components for a given task</span>
    <br>
    <b>Route Parameters</b><br>
        - taskId: integer
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
    [
        {<br>
            'taskId' : 7589454894,
            'userId' : -1,
            'type' : 'kindOfType',
            'label' : 'kindOfLabel',
            'isMandatory' : true,
            'order' : 2
        }<br>
        {<br>
            'taskId' : 7589454894,
            'userId' : yossi,
            'type' : 'otherKindOfType',
            'label' : 'otherKindOfLabel',
            'isMandatory' : false,
            'order' : 4
        }<br>
    ]
    </code>
    <br>
    """

    arr = []
    query = TaskComponent.all()
    query.filter("taskId = ", taskId)

    for tc in query.run():
        arr.append(dict(json.loads(tc.to_JSON())))

    #sort array by order, and remove added key
    arr = sorted(arr, key=itemgetter('order'), reverse=False)

    if len(arr) != 0:
        return Response(response=json.dumps(arr),
                        status=200,
                        mimetype="application/json")
    else:
        return no_content()



@task_routes.route('/api/tasks/help')
def documentation():
    return auto.html()



@task_routes.route('/api/tasks/help')
def documentation():
    return auto.html()






# @task_routes.route('/api/tasks/getClosestTask/<string:courseName>', methods=["GET"])
# @auto.doc()
# def getClosestTask(courseName):
#     """
#     <span class="card-title">>This Call will return an array of all projects in a given course</span>
#     <br>
#     <b>Route Parameters</b><br>
#         - name: 'course name'
#     <br>
#     <br>
#     <b>Payload</b><br>
#      - NONE
#     <br>
#     <br>
#     <b>Response</b>
#     <br>
#     200 - JSON Example:<br>
#     <code>
#         {<br>
#         'projectName': 'Advance Math',<br>
#         'courseName': 'JCE',<br>
#         'grade': 98,<br>
#         'logo_url': 'http://location.domain.com/image.jpg',<br>
#         'gitRepository': 'http://location.git.com/somthing',<br>
#         'membersId': ['bob', 'dylan', 'quentin', 'terentino']<br>
#         }
#     </code>
#     <br>
#     """
#     #get all tasks for a specific course
#     arr = []
#     query = Task.all()
#     query.filter("courseName =", courseName)
#     for t in query.run():
#         count+=1
#         if t.dueDate < closestDate:
#             closestDate = t.dueDate
#             index = count
#         arr.append(dict(json.loads(t.to_JSON())))
#
#     print arr
#     if len(arr) != 0:
#         return Response(response=json.dumps(arr[index]),
#                         status=200,
#                         mimetype="application/json")
#     else:
#         return no_content("no Tasks")
#
