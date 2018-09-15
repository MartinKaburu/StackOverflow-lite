'''JWT and user authentication module
'''
import re
from datetime import datetime as dt

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
        date = dt.now()
        if re.match(email_format, email):
            username_format = r"(^[a-zA-z0-9_.]*$)"
            if re.match(username_format, username):
                cursor = CONNECTION.cursor()
                sql = 'SELECT * FROM users WHERE email=%s;'
                cursor.execute(sql, ([email]))
                existing = cursor.fetchall()
                if not existing:
                    sql = 'INSERT INTO users(username, email, password, created_on) VALUES(%s, %s, %s, %s);'
                    password = generate_password_hash(password)
                    cursor.execute(sql, (username, email, password, date))
                    CONNECTION.commit()
                    return jsonify({"message":"user created successfully"}), 201
                return make_response(jsonify({"message":"Email address has an account"})), 400
            return jsonify({"message":"Username should contain only alphanumeical values"}), 400
        return jsonify({"message":"Invalid email format"}), 400
    return abort(400), 400



@jwt.authentication_handler
def api_login(email, password):
    '''Login user
    '''
    users = Users(email)
    user = users.get_all()
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
    users = Users(email)
    user = users.get_all()
    return user[0][0]


jwt = JWT(APP, api_login, identity)
