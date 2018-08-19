'''api endpoints:
    /api/v1/questions
        methods=['GET']
        returns json data of all the questions
        status_code 200
    /api/v1/get_questions/<int:question_id>
        methods=['GET']
        returns json data on the question specified
        status_code 200
    /api/v1/post_question
        methods=['POST']
        returns json data on the added question
        status_code 201
    /api/v1/questions/<int:question_id>/answers
        methods=['POST']
        returns json data on the question answered
        status_code 201

errors:
    404 resource not found
    201 created
    200 OK
'''

from datetime import datetime as dt

from flask import jsonify, Blueprint, abort, request

from app import CONNECTION


BP = Blueprint('api', __name__, url_prefix='/api/v1')


@BP.route('/questions', methods=['GET'])
def get_all():
    ''' get all questions
    '''
    cursor = CONNECTION.cursor()
    cursor.execute('SELECT * FROM questions;')
    questions = cursor.fetchall()
    cursor.close()
    return jsonify({'QUESTIONS': questions}), 200


@BP.route('/questions/<int:question_id>')
def get_question(question_id):
    ''' get specific question
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM questions WHERE id=%s;'
    cursor.execute(sql, ([question_id]))
    question = cursor.fetchall()
    cursor.close()
    if not question:
        return abort(404), 404
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM answers WHERE question_id=%s'
    cursor.execute(sql, [question_id])
    answers = cursor.fetchall()
    return jsonify({'question': question}, {'answers':answers}), 200


@BP.route('/post_question', methods=['POST'])
def add_question():
    ''' add a question
    '''
    if request.json and request.json['owner'] and request.json['content']:
        cursor = CONNECTION.cursor()
        sql = 'INSERT INTO questions(content, question_owner) VALUES (%s, %s);'
        cursor.execute(sql, (request.json['content'], request.json['owner']))
        CONNECTION.commit()
        cursor.close()
        return jsonify({'201': 'Question added'}), 201

    return abort(400), 400


@BP.route('/questions/<int:question_id>/answers', methods=['POST'])
def answer_question(question_id):
    '''answer a question
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM questions WHERE id=%s;'
    cursor.execute(sql, ([question_id]))
    question = cursor.fetchall()
    if not question:
        return abort(404), 404
    if request.json and request.json['answer_content'] and request.json['answer_owner']:
        sql = 'INSERT INTO answers(answer_owner, content, question_id) VALUES (%s, %s, %s);'
        cursor.execute(sql,(request.json['answer_owner'], request.json['answer_content'], question_id))
        CONNECTION.commit()
        cursor.close()
        return jsonify({"201": "question answered"}), 201
    return abort(400), 400

@BP.route('/delete/<int:question_id>', methods=['DELETE'])
def remove_question(question_id):
    ''' get specific question
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM questions WHERE id=%s;'
    cursor.execute(sql, ([question_id]))
    question = cursor.fetchall()
    if not question:
        return abort(404), 404
    sql = 'DELETE FROM questions WHERE id=%s;'
    cursor.execute(sql, ([question_id]))
    sql = 'DELETE FROM answers WHERE question_id=%s;'
    cursor.execute(sql, ([question_id]))
    cursor.close()
    CONNECTION.commit()
    return jsonify({'Question deleted':'200'}), 200
