'''stackoverflow-lite api
'''

from flask import Flask, make_response, jsonify
import psycopg2 as psycopg

from config import Development

APP = Flask(__name__)
APP.config.from_object(Development)
CONNECTION = psycopg.connect(\
    dbname=APP.config['DATABASE_NAME'], \
    user=APP.config['DATABASE_USER'], \
    host=APP.config['DATABASE_HOST'], \
    password=APP.config['DATABASE_PASSWORD']\
    )


from .api.v1 import endpoints
from .auth import api_login, register_user, identity

APP.register_blueprint(endpoints.BP)



@APP.errorhandler(404)
def not_found(error):
    '''jsonify 404
    '''
    return make_response(jsonify({'error': 'Not found'}), 404)


@APP.errorhandler(400)
def bad_request(error):
    ''' jsonify 400
    '''
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@APP.errorhandler(405)
def method_not_allowed(error):
    '''error handler for Bad request
    '''
    return make_response(jsonify({'error':'Method Not Allowed'}), 405)
