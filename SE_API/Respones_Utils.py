__author__ = 'Aran'

from flask import Response
import json

def bad_request(message='Bad Request'):
    return Response(response=json.dumps({'message': message}),
                        status=400,
                        mimetype="application/json")


def forbidden(message='Forbidden'):
    return Response(response=json.dumps({'message': message}),
                        status=403,
                        mimetype="application/json")