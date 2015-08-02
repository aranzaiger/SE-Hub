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
from models.TaskGrade import TaskGrade

#Validation Utils Libs
from SE_API.Validation_Utils import *
from SE_API.Respones_Utils import *


task_routes = Blueprint("task_routes", __name__)
auto = Autodoc()



#----------------------------------------------------------
#                     POST
#----------------------------------------------------------

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
        "courseId":1234567890,<br>
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
        return bad_request("no payload")
    payload = json.loads(request.data)
    if not is_lecturer(token):  #todo: change to lecturer id
        return forbidden("Invalid token or not a lecturer!")

    user = get_user_by_token(token)

    #check lecturer is owner of course
    try:
        courseId = payload['courseId']
    except Exception as e:
        print e
        return bad_request("invalid courseId format")

    course = Course.get_by_id(int(courseId))
    if course is None:
        return bad_request("No such Course")

    if course.master_id != user.key().id():
        return forbidden("Lecturer is not owner of Course")

    #parse dueDate
    try:
        date = datetime.date(payload['dueDate']['year'],payload['dueDate']['month'],payload['dueDate']['day'])
    except Exception:
        return bad_request("invalid dueDate format")
    #create Task object
    try:
        task = Task(title=payload['title'], courseId=payload['courseId'], description=payload['description'], dueDate=date)
    except Exception as e:
        print e
        return bad_request("bad")
    try:
        task.isPersonal = payload['isPersonal']
    except Exception:
        pass


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

    return Response(response=task.to_JSON(),
                                status=200,
                                mimetype="application/json")


#----------------------------------------------------------
#                     PUT
#----------------------------------------------------------

#----------------------------------------------------------
#                     GET
#----------------------------------------------------------


@task_routes.route('/api/tasks/getAllTasksByCourse/<string:token>/<string:courseId>', methods=["GET"])
@auto.doc()
def getAllTasksByCourse(token, courseId):
    """
    <span class="card-title">>This Call will return an array of all Tasks in a course ordered by date</span>
    <br>
    <b>Route Parameters</b><br>
        - SeToken: token<br>
        - courseId: 1234567890
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
        'courseId' : 12345678,<br>
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
    if get_user_by_token(token) is None:
        return bad_request("Bad User Token")

    arr = []
    query = Task.all()

    try:
        query.filter("courseId = ", int(courseId))
    except Exception as e:
        return bad_request("Bad id format")

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


@task_routes.route('/api/tasks/getAllFutureCampusTasks/<string:token>/<string:courseId>', methods=["GET"])
@auto.doc()
def getAllFutureCampusTasks(token, courseId):
    """
    <span class="card-title">>This Call will return an array of all Future Tasks in a course, ordered by date</span>
    <br>
    <b>Route Parameters</b><br>
         - SeToken: token<br>
        - courseId: 1234567890
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

    if get_user_by_token(token) is None:
        return bad_request("Bad User Token")

    arr = []
    query = Task.all()

    try:
        query.filter("courseId = ", int(courseId))
    except Exception as e:
        return bad_request("Bad id format")

    for t in query.run():
        taskDic =dict(json.loads(t.to_JSON()))
        #add a key 'forSortDate' for sorting dates
        taskTime = datetime.datetime(taskDic['dueDate']['year'], taskDic['dueDate']['month'], taskDic['dueDate']['day'])
        if taskTime >= datetime.date.today():
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

@task_routes.route('/api/tasks/getAllFutureTasks/<string:token>', methods=["GET"])
@auto.doc()
def getAllFutureTasks(token):
    """
    <span class="card-title">>This Call will return an array of all Future Tasks ordered by date</span>
    <br>
    <b>Route Parameters</b><br>
         - SeToken: token<br>
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

    user = get_user_by_token(token)
    if user is None:
        return bad_request("Bad User Token")

    arr = []

    for courseId in user.courses_id_list:
        query = Task.all()

        try:
            query.filter("courseId = ", int(courseId))
        except Exception as e:
            return bad_request("Bad id format")

        for t in query.run():
            taskDic =dict(json.loads(t.to_JSON()))
            #add a key 'forSortDate' for sorting dates
            taskTime = datetime.date(taskDic['dueDate']['year'], taskDic['dueDate']['month'], taskDic['dueDate']['day'])
            if taskTime >= datetime.date.today():
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


@task_routes.route('/api/tasks/getTaskComponents/<string:token>/<string:taskId>', methods=["GET"])
@auto.doc()
def getTaskComponents(token, taskId):
    """
    <span class="card-title">>This Call will return an array of all components for a given task</span>
    <br>
    <b>Route Parameters</b><br>
         - SeToken: token<br>
        - taskId: 1234567890
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

    if get_user_by_token(token) is None:
        return bad_request("Bad User Token")

    arr = []
    query = TaskComponent.all()

    try:
        query.filter("taskId = ", int(taskId))
    except Exception as e:
        return bad_request("Bad id format")

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

@task_routes.route('/api/tasks/getAllUserTasks/<string:token>', methods=["GET"])
@auto.doc()
def getAllUserTasks(token):
    """
    <span class="card-title">>This Call will return an array of all of the User's Tasks</span>
    <br>
    <b>Route Parameters</b><br>
        - SeToken: token<br>
    <br>
    <br>
    <b>Payload</b><br>
     - NONE
    <br>
    <br>
    <b>Response</b>
    <br>
    200 - JSON Example:<br>
    <code>[<br>
              {<br>
                "courseName": "Advance Math",<br>
                "courseId": 4762397176758272,<br>
                "PersonalTasks": [<br>
                  {<br>
                    "grade": 12,<br>
                    "isPersonal": true,<br>
                    "dueDate": {<br>
                      "year": 2010,<br>
                      "day": 4,<br>
                      "month": 2<br>
                    },<br>
                    "courseId": 4762397176758272,<br>
                    "title": "task1",<br>
                    "description": "pls fddfsdfdsk",<br>
                    "id": 5888297083600896<br>
                  }<br>
                ],<br>
                "projectTasks": []<br>
              },<br>
              {<br>
                "courseName": "Bad Math",<br>
                "courseId": 5659598665023488,<br>
                "PersonalTasks": [<br>
                  {<br>
                    "grade": 12,<br>
                    "isPersonal": true,<br>
                    "dueDate": {<br>
                      "year": 2010,<br>
                      "day": 4,<br>
                      "month": 2<br>
                    },<br>
                    "courseId": 5659598665023488,<br>
                    "title": "new task1",<br>
                    "description": "pls fddfsdfdsk",<br>
                    "id": 5096648711602176<br>
                  },<br>
                  {<br>
                    "grade": 12,<br>
                    "isPersonal": true,<br>
                    "dueDate": {<br>
                      "year": 2010,<br>
                      "day": 4,<br>
                      "month": 2<br>
                    },<br>
                    "courseId": 5659598665023488,<br>
                    "title": "new task4",<br>
                    "description": "pls fddfsdfdsk",<br>
                    "id": 5167017455779840<br>
                  }<br>
                ],<br>
                "projectTasks": [<br>
                  {<br>
                    "grade": 12,<br>
                    "isPersonal": false,<br>
                    "dueDate": {<br>
                      "year": 2010,<br>
                      "day": 4,<br>
                      "month": 2<br>
                    },<br>
                    "courseId": 5659598665023488,<br>
                    "title": "new task3",<br>
                    "description": "pls fddfsdfdsk",<br>
                    "id": 5237386199957504<br>
                  }<br>
                ]<br>
              }<br>
    ]<br>
    </code>
    <br>
    """
    user = get_user_by_token(token)
    if user is None:
        return bad_request("Bad User Token")

    arr = []
    for c in user.courses_id_list:

        dic = {}
        course = Course.get_by_id(int(c))
        dic['courseName'] = course.courseName
        dic['courseId'] = course.key().id()
        courseTasks = Task.all().filter("courseId = ", course.key().id())
        taskArr = []
        for t in courseTasks.run():
            taskDic =dict(json.loads(t.to_JSON()))
            #add a key 'forSortDate' for sorting dates
            taskTime = datetime.datetime(taskDic['dueDate']['year'], taskDic['dueDate']['month'], taskDic['dueDate']['day'])
            taskDic['forSortDate'] = taskTime
            grade = TaskGrade.all().filter("taskId = ", t.key().id()).filter("userId = ", user.key().id())
            for g in grade.run():
                taskDic['grade'] = g.grade
            if grade.count() == 0:
                taskDic['grade'] = 0
            taskArr.append(taskDic)

        taskArr = sorted(taskArr, key=itemgetter('forSortDate'), reverse=False)
        for i in taskArr:
            del i['forSortDate']

        userTaskArr = []
        projectTaskArr = []
        for t in taskArr:
            if t['isPersonal']:
                userTaskArr.append(t)
            else:
                projectTaskArr.append(t)


        dic['PersonalTasks'] = userTaskArr
        dic['projectTasks'] = projectTaskArr
        arr.append(dic)

    #sort array by date, and remove added key


    return Response(response=json.dumps(arr),
                        status=200,
                        mimetype="application/json")



@task_routes.route('/api/tasks/getUserTaskById/<string:token>/<string:taskId>', methods=["GET"])
@auto.doc()
def getUserTaskById(token, taskId):
    """
    <span class="card-title">>This Call will return an array of all components for a given task</span>
    <br>
    <b>Route Parameters</b><br>
         - SeToken: token<br>
        - taskId: 1234567890
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
    user = get_user_by_token(token)
    if user is None:
        return bad_request("Bad User Token")

    task = Task.get_by_id(int(taskId))
    if task is None:
        return bad_request("Bad Task id")


    taskCompQuery = TaskComponent.all()
    taskCompQuery.filter("taskId = ", task.key().id())

    if task.isPersonal:
        taskCompQuery.filter("userId = ", user.key().id())
    else:
        taskCompQuery.filter("userId = ", user.key().id())#TODO: fix to project

    #check if never created a personalized task and if so, create it
    if taskCompQuery.count() == 0:
        taskCompQuery = TaskComponent.all().filter("taskId = ", task.key().id()).filter("userId = ", -1)
        for tc in taskCompQuery.run():
            tcNew = TaskComponent(taskId=tc.taskId, userId=user.key().id(), type=tc.type, label=tc.label, isMandatory=tc.isMandatory, order=tc.order)
            db.put(tcNew)

        grade = TaskGrade(grade=0, taskId=task.key().id(), userId=user.key().id())
        db.put(grade)







    db.save
    return no_content()



#----------------------------------------------------------
#                     DELETE
#----------------------------------------------------------



@task_routes.route('/api/tasks/deleteTask/<string:token>/<string:taskId>', methods=['DELETE'])
@auto.doc()
def deleteTask(token, taskId):
    """
    <span class="card-title">This Call will delete a specific Task</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
        - taskId: 'taskid'
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

    if not is_lecturer(token):
        return forbidden("Invalid token or not a lecturer!")

    #todo: check if lecturer is owner of course
    #return forbidden("lecturer is not owner of course")

    user = get_user_by_token(token)

    try:
        c = Task.get_by_id(int(taskId))
    except Exception as e:
        return bad_request("Bad id format")

    if c is None:
        return bad_request("no such Task")


    db.delete(c)
    db.save
    return accepted("Task deleted")


@task_routes.route('/api/tasks/deleteTaskComponents/<string:token>/<string:taskId>', methods=['DELETE'])
@auto.doc()
def deleteTaskComponents(token,taskId):
    """
    <span class="card-title">This Call will delete a specific Task's components</span>
    <br>
    <b>Route Parameters</b><br>
        - seToken: 'seToken'
        - taskId: 'taskid'
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
    400 - no such Task
    <br>
    403 - Invalid token or not a lecturer or lecturer is not owner of Task!<br>
    """

    if not is_lecturer(token):
        return forbidden("Invalid token or not a lecturer!")

    #todo: check if lecturer is owner of course
    #return forbidden("lecturer is not owner of course")

    user = get_user_by_token(token)


    try:
        t = Task.get_by_id(int(taskId))
    except Exception as e:
        return bad_request("Bad id format")

    if t is None:
        return bad_request("no such Task")

    query = TaskComponent.all()
    query.filter('taskId = ', t.key().id())

    for tc in query.run():
        db.delete(tc)

    db.save
    return accepted("Task deleted")




#----------------------------------------------------------
#                     DOCUMENTATION
#----------------------------------------------------------

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
