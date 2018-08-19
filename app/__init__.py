'''stackoverflow-lite api
'''

from flask import Flask, make_response, jsonify
import psycopg2 as psycopg

from config import Config

APP = Flask(__name__, template_folder='./user_interface/templates', static_folder='./user_interface/static')
APP.config.from_object(Config)
CONNECTION = psycopg.connect(dbname='stackoverflow', user='postgres', host='localhost', password='kaburu@andela')


from .api.v1 import endpoints
from .auth import login, register_user, identity
from .user_interface import views

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
