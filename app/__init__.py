'''stackoverflow-lite api
'''

from flask import Flask, make_response, jsonify
from .api.v1 import endpoints


APP = Flask(__name__, template_folder='./user_interface/templates', \
static_folder='./user_interface/static')
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
def bad_request(error):
    '''error handler for Bad request
    '''
    return make_response(jsonify({'error':'Method Not Allowed'}), 405)
