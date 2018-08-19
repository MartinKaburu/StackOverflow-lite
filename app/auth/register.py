'''Module to register users into the database
'''
from flask import request, jsonify, make_response, abort
from werkzeug.security import  generate_password_hash

from app import CONNECTION, APP
from app.api.v1.endpoints import BP

@BP.route('/register', methods=['POST'])
def register():
    '''Register new User
    '''
    if request.json and request.json['username'] and request.json['email'] and request.json['password']:
        cursor = CONNECTION.cursor()
        sql = 'SELECT * FROM users WHERE email=%s;'
        email = request.json['email']
        cursor.execute(sql, ([email]))
        existing = cursor.fetchall()
        if existing:
            return make_response(jsonify({"400":"Email address has an account"})), 400

        sql = 'INSERT INTO users(username, email, password) VALUES(%s, %s, %s);'
        password = generate_password_hash(request.json['password'])
        cursor.execute(sql, (request.json['username'], request.json['email'], password))
        CONNECTION.commit()
        return jsonify({"201":"user created successfully"}), 201
    return abort(400), 400
