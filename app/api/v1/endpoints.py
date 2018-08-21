'''api endpoints
'''

from datetime import datetime as dt

from flask import jsonify, Blueprint, abort, request
from flask_jwt import jwt_required, current_identity

<<<<<<< HEAD
from app import CONNECTION
=======
>>>>>>> 3beadc8e238cad2fd9ece65512a14f5c3254acfc


BP = Blueprint('api', __name__, url_prefix='/api/v1')


<<<<<<< HEAD
@BP.route('/questions', methods=['GET'])
@jwt_required()
def get_all():
=======
@BP.route('/questions', methods=['GET', 'POST'])
def get_and_add():
>>>>>>> 3beadc8e238cad2fd9ece65512a14f5c3254acfc
    ''' get all questions
    Post a new question
    '''
<<<<<<< HEAD
    cursor = CONNECTION.cursor()
    cursor.execute('SELECT * FROM questions;')
    questions = cursor.fetchall()
    cursor.close()
    return jsonify({'QUESTIONS': questions}), 200
=======
    if request.method == 'POST':
        if request.json and request.json['owner'] and request.json['content']:
            try:
                question = {
                    'id': QUESTIONS[-1]['id']+1,
                    'owner': request.json['owner'],
                    'content': request.json['content'],
                    'answers': [],
                    'date_asked': dt.utcnow(),
                    'answered': False
                }
            except IndexError:
                question = {
                    'id': 1,
                    'owner': request.json['owner'],
                    'content': request.json['content'],
                    'answers': [],
                    'date_asked': dt.utcnow(),
                    'answered': False
                }
            QUESTIONS.append(question)
            return jsonify({'question': question}), 201
        return abort(400), 400

    return jsonify({'QUESTIONS': QUESTIONS}), 200
>>>>>>> 3beadc8e238cad2fd9ece65512a14f5c3254acfc


@BP.route('/questions/<int:question_id>')
@jwt_required()
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
    cursor.close()
    return jsonify({'question': question}, {'answers':answers}), 200


<<<<<<< HEAD
@BP.route('/post_question', methods=['POST'])
@jwt_required()
def add_question():
    ''' add a question
    '''
    if request.json and request.json['content']:
        cursor = CONNECTION.cursor()
        sql = 'INSERT INTO questions(content, question_owner) VALUES (%s, %s);'
        cursor.execute(sql, (request.json['content'], int(current_identity)))
        CONNECTION.commit()
        cursor.close()
        return jsonify({'201': 'Question added'}), 201

    return abort(400), 400


=======
>>>>>>> 3beadc8e238cad2fd9ece65512a14f5c3254acfc
@BP.route('/questions/<int:question_id>/answers', methods=['POST'])
@jwt_required()
def answer_question(question_id):
    '''answer a question
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM questions WHERE id=%s;'
    cursor.execute(sql, ([question_id]))
    question = cursor.fetchall()
    if not question:
        return abort(404), 404
    if request.json and request.json['answer_content']:
        sql = 'INSERT INTO answers(answer_owner, content, question_id) VALUES (%s, %s, %s);'
        cursor.execute(sql,(int(current_identity), request.json['answer_content'], question_id))
        CONNECTION.commit()
        cursor.close()
        return jsonify({"201": "question answered"}), 201
    return abort(400), 400

@BP.route('/delete/<int:question_id>', methods=['DELETE'])
@jwt_required()
def remove_question(question_id):
    ''' get specific question
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM questions WHERE id=%s;'
    cursor.execute(sql, ([question_id]))
    question = cursor.fetchall()
    if not question:
        return abort(404), 404
    if int(current_identity) is question[0][2]:
        sql = 'DELETE FROM questions WHERE id=%s;'
        cursor.execute(sql, ([question_id]))
        sql = 'DELETE FROM answers WHERE question_id=%s;'
        cursor.execute(sql, ([question_id]))
        cursor.close()
        CONNECTION.commit()
        return jsonify({'Question deleted':'200'}), 200
    return jsonify({"401":"Unauthorized: Only question owner can remove question"})

@BP.route('/upvote/<int:answer_id>', methods=['POST'])
@jwt_required()
def upvote_answer(answer_id):
    '''Upvote answers
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM answers WHERE id=%s;'
    cursor.execute(sql, ([answer_id]))
    answer = cursor.fetchall()
    if answer:
        try:
            if str(current_identity) in answer[0][7]:
                return jsonify({"400":"You can only vote once"})
        except TypeError:
            pass
        answer[0] = list(answer[0])
        answer[0][3] +=1
        sql = 'SELECT array_append(voters[], %s);'
        cursor.execute(sql, ([str(current_identity)]))
        answer[0] = tuple(answer[0])
        CONNECTION.commit()
        cursor.close()
    return abort(404)

@BP.route('/downvote/<int:answer_id>', methods=['POST'])
@jwt_required()
def downvote_answer(answer_id):
    '''Downvote answers
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM answers WHERE id=%s;'
    cursor.execute(sql, ([answer_id]))
    answer = cursor.fetchall()
    if answer:
        try:
            if str(current_identity) in answer[0][7]:
                return jsonify({"400":"You can only vote once"})
        except TypeError:
            pass
        answer[0][3] -= 1;
        sql = 'SELECT array_append(%s, %s);'
        cursor.execute(sql, (answer[0][7], str(current_identity)))
        CONNECTION.commit()
        cursor.close()
    return abort(404)
