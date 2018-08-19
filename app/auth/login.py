'''Module to login user
'''
from flask import abort, jsonify, request
from werkzeug.security import check_password_hash

from app import CONNECTION
from app.api.v1.endpoints import BP


@BP.route('/login', methods=['POST'])
def login():
    '''Login user
    '''
    if request.json and request.json['email'] and request.json['password']:
        email = request.json['email']
        cursor = CONNECTION.cursor()
        sql = 'SELECT * FROM users WHERE email=%s;'
        cursor.execute(sql, ([email]))
        user = cursor.fetchall()
        if check_password_hash(user[0][3], request.json['password']):
            return jsonify({"200":"User logged in successfully"}), 200
        return jsonify({"404":"Invalid user or credentials"}), 200
    return abort(400), 400
