__author__ = 'Aran'

from flask import Response
import json

def bad_request():
    return Response(response=json.dumps({'message': 'Bad Request'}),
                        status=400,
                        mimetype="application/json")


def forbidden(message={'message': 'Forbidden'}):
    return Response(response=json.dumps(message),
                        status=403,
                        mimetype="application/json")