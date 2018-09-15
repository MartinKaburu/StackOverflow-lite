'''stackoverflow-lite api
'''
import os

from flask import Flask, make_response, jsonify
import psycopg2 as psycopg
from flask_cors import CORS

from config import Development, Test

APP = Flask(__name__)
if os.getenv('CONTEXT') == 'TEST':
    APP.config.from_object(Test)
elif os.getenv('CONTEXT') == 'DEV':
    APP.config.from_object(Development)
    APP.url_map.strict_slashes = False

CONNECTION = psycopg.connect(\
    dbname=APP.config['DATABASE_NAME'], \
    user=APP.config['DATABASE_USER'], \
    host=APP.config['DATABASE_HOST'], \
    password=APP.config['DATABASE_PASSWORD']\
    )

CORS(APP, resources=r'/api/*')
from .api.v1 import endpoints
from .auth import api_login, register_user, identity

APP.register_blueprint(endpoints.BP)


@APP.errorhandler(404)
def not_found(error):
    '''jsonify 404
    '''
    return make_response(jsonify({'message': 'Not found'}), 404)


@APP.errorhandler(400)
def bad_request(error):
    ''' jsonify 400
    '''
    return make_response(jsonify({'message': 'Bad Request'}), 400)

@APP.errorhandler(405)
def method_not_allowed(error):
    '''error handler for Bad request
    '''
    return make_response(jsonify({'message':'Method Not Allowed'}), 405)


@APP.errorhandler(500)
def method_not_allowed(error):
    '''error handler for Bad request
    '''
    return make_response(jsonify({'message':'Server down'}), 500)
