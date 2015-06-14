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
    '''
    <span class="card-title">This Function is will Activate a user and add tha campus to it</span>
    <br>
    <b>Route Parameters</b><br>
        - validation_token: 'seToken|email_suffix'
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
        'username' : 'github_username',<br>
        'name' : 'Bob Dylan',<br>
        'email' : 'email@domain.com',<br>
        'isLecturer' : true,<br>
        'seToken' : 'dds2d-sfvvsf-qqq-fdf33-sfaa',<br>
        'avatar_url' : 'http://location.domain.com/image.jpg',<br>
        'isFirstLogin' : false,<br>
        'campuses_id_list': ['22314','243512',...,'356'],<br>
        'classes_id_list': ['22314','243512',...,'356']<br>
        }
    </code>
    <br>
    403 - Invalid Token
    '''
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