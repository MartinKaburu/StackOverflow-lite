'''JWT and user authentication module
'''
import re

from flask import request, jsonify, make_response, abort
from werkzeug.security import  generate_password_hash, check_password_hash
from flask_jwt import JWT
from flask_cors import cross_origin

from app import CONNECTION, APP
from app.api.v1.endpoint_models import Users

jwt = JWT()

class User(object):
    '''Create object for jwt
    '''
    def __init__(self, id):
        self.id = id


@APP.route('/api/v1/auth/signup', methods=['POST'])
@cross_origin()
def register_user():
    '''Register new User
    '''
    if request.json and \
    request.json['username'] and \
    request.json['email'] and \
    request.json['password']:
        email = request.json['email']
        password = request.json['password']
        username = request.json['username']
        email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"
        if re.match(email_format, email):
            user = Users()
            existing = user.get_all(email)
            if existing:
                return make_response(jsonify({"400":"Email address has an account"})), 400
            user.create_user(username, email,password)
            return jsonify({"201":"user created successfully"}), 201
        return jsonify({"400":"Invalid email format"}), 400
    return abort(400), 400


@jwt.authentication_handler
def api_login(email, password):
    '''Login user
    '''
    users = Users()
    user = users.get_all(email)
    try:
        if check_password_hash(user[0][3], password):
            return User(id=user[0][2])
        return False
    except IndexError:
        return False


@jwt.identity_handler
def identity(payload):
    '''Define current user
    '''
    email = payload['identity']
    users = Users()
    user = users.get_all(email)
    return user[0][0]


jwt = JWT(APP, api_login, identity)
