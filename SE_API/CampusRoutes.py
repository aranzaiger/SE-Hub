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
from models.Campus import Campus

#Validation Utils Libs
from SE_API.Validation_Utils import *
from SE_API.Respones_Utils import *



campus_routes = Blueprint("campus_routes", __name__)
auto = Autodoc()

@campus_routes.route('/api/campuses/create/<string:token>', methods=['POST'])
@auto.doc()
def create_campus(token):
    """
    <span class="card-title">This call will create a new campus in the DB</span>
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
        campus = Campus(title=payload['title'], email_ending=payload['email_ending'], master_user_id=user.key().id(), avatar_url=payload['avatar_url'])
    except Exception:
        return bad_request()

    db.put(campus)
    db.save
    return Response(response=campus.to_JSON(),
                                status=201,
                                mimetype="application/json")





@campus_routes.route('/api/campuses/<string:token>', methods=['GET'])
@auto.doc()
def get_campuses(token):
    """
    <span class="card-title">This Call will return an array of all Campuses available</span>
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




@campus_routes.route('/api/campuses/help')
def documentation():
    return auto.html()