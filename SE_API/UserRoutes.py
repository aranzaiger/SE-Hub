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

#Validation Utils Libs
from SE_API.Validation_Utils import *
from SE_API.Respones_Utils import *


user_routes = Blueprint("user_routes", __name__)
auto = Autodoc()


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
        'campuses_id_list': ['JCA','JCB','JCC'],<br>
        'classes_id_list': ['a','b','c']<br>
        }
    </code>
    <br>
    403 - No User Found
    """
    query = User.all()
    query.filter("seToken = ", token)

    for u in query.run(limit=5):
        return Response(response=u.to_JSON(),
                        status=200,
                        mimetype="application/json")  # Real response!

    return bad_request("No User Found")


@user_routes.route('/api/users/help')
def documentation():
    return auto.html()