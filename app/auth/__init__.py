'''JWT and user authentication module
'''
import re

from flask import request, jsonify, make_response, abort
from werkzeug.security import  generate_password_hash, check_password_hash
from flask_jwt import JWT

from app import CONNECTION, APP

jwt = JWT()

class User(object):
    def __init__(self, id):
        self.id = id


@APP.route('/api/v1/auth/signup', methods=['POST'])
def register_user():
    '''Register new User
    '''
    if request.json and request.json['username'] and request.json['email'] and request.json['password']:
        email = request.json['email']
        password = request.json['password']
        username = request.json['username']
        email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"
        if re.match(email_format, email):
            cursor = CONNECTION.cursor()
            sql = 'SELECT * FROM users WHERE email=%s;'
            cursor.execute(sql, ([email]))
            existing = cursor.fetchall()
            if existing:
                return make_response(jsonify({"400":"Email address has an account"})), 400

            sql = 'INSERT INTO users(username, email, password) VALUES(%s, %s, %s);'
            password = generate_password_hash(password)
            cursor.execute(sql, (username, email, password))
            CONNECTION.commit()
            return jsonify({"201":"user created successfully"}), 201
        return jsonify({"400":"Invalid email format"})
    return abort(400), 400


@jwt.authentication_handler
def api_login(email, password):
    '''Login user
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM users WHERE email=%s;'
    cursor.execute(sql, ([email]))
    user = cursor.fetchall()
    try:
        if check_password_hash(user[0][3], password):
            return User(id=user[0][1])
        return False
    except IndexError:
        return False


@jwt.identity_handler
def identity(payload):
    '''Define current user
    '''
    username = payload['identity']
    sql = 'SELECT * FROM users WHERE username=%s;'
    cursor = CONNECTION.cursor()
    cursor.execute(sql, ([username]))
    user = cursor.fetchall()
    cursor.close()
    return user[0][0]

jwt = JWT(APP, api_login, identity)
