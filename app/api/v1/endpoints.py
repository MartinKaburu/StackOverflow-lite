'''api endpoints
'''
from flask import jsonify, Blueprint, abort, request
from flask_jwt import jwt_required, current_identity

from app import CONNECTION


BP = Blueprint('api', __name__, url_prefix='/api/v1')


@BP.route('/questions', methods=['GET', 'POST'])
@jwt_required()
def get_and_post():
    ''' get all questions
    Post a new question
    '''
    if request.method == 'GET':
        cursor = CONNECTION.cursor()
        cursor.execute('SELECT * FROM questions;')
        questions = cursor.fetchall()
        cursor.close()
        display = []
        for question in questions:
            retformat = {
                "question_id":question[0],
                "content":question[1],
                "owner_id":question[2]
            }
            display.append(retformat)
        return jsonify({"QUESTIONS":display}), 200
    elif request.method == 'POST':
        if request.json and request.json['content']:
            cursor = CONNECTION.cursor()
            sql = 'INSERT INTO questions(content, question_owner) VALUES (%s, %s);'
            cursor.execute(sql, (request.json['content'], int(current_identity)))
            CONNECTION.commit()
            cursor.close()
            return jsonify({'201': 'Question added'}), 201
        return abort(400), 400


@BP.route('/questions/<int:question_id>', methods=['GET', 'DELETE'])
@jwt_required()
def get_delete_question(question_id):
    ''' get specific question
    '''
    if request.method == 'GET':
        display = []
        cursor = CONNECTION.cursor()
        sql = 'SELECT * FROM questions WHERE id=%s;'
        cursor.execute(sql, ([question_id]))
        question = cursor.fetchall()
        cursor.close()
        if question:
            cursor = CONNECTION.cursor()
            sql = 'SELECT * FROM answers WHERE question_id=%s'
            cursor.execute(sql, [question_id])
            answers = cursor.fetchall()
            display_ans = []
            for answer in answers:
                answer = list(answer)
                retformat = {
                    "answer_id":answer[0],
                    "answer_content":answer[1],
                    "answer_owner":answer[2],
                    "upvotes":answer[3],
                    "downvotes":answer[4],
                    "accepted":answer[5],
                    "question_id":answer[6],
                }
                display_ans.append(retformat)
            display = [
                {
                    "question_id": question[0][0],
                    "content": question[0][1],
                    "question_owner": question[0][2],
                    "answers": display_ans
                }
            ]
            cursor.close()
            return jsonify(display), 200
        return abort(404), 404
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM questions WHERE id=%s;'
    cursor.execute(sql, ([question_id]))
    question = cursor.fetchall()
    if question:
        if int(current_identity) is question[0][2]:
            sql = 'DELETE FROM answers WHERE question_id=%s;'
            cursor.execute(sql, ([question_id]))
            sql = 'DELETE FROM questions WHERE id=%s;'
            cursor.execute(sql, ([question_id]))
            cursor.close()
            CONNECTION.commit()
            return jsonify({'Question deleted':'200'}), 200
        return jsonify({"401":"Unauthorized: Only question owner can remove question"})
    return abort(404), 404


@BP.route('/questions/<int:question_id>/answers', methods=['POST'])
@jwt_required()
def answer_question(question_id):
    '''answer a question
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM questions WHERE id=%s;'
    cursor.execute(sql, ([question_id]))
    question = cursor.fetchall()
    if question:
        if request.json and request.json['answer_content']:
            sql = 'INSERT INTO answers(answer_owner, content, question_id) \
            VALUES (%s, %s, %s);'
            cursor.execute(sql, \
            (int(current_identity), request.json['answer_content'], question_id))
            CONNECTION.commit()
            cursor.close()
            return jsonify({"201": "question answered"}), 201
        return abort(400), 400
    return abort(404), 404


@BP.route('/update/<int:question_id>/<int:answer_id>', methods=['PUT'])
@jwt_required()
def update_answer(question_id, answer_id):
    ''' get specific question
    '''
    if request.json and request.json['content']:
        update = request.json['content']
        cursor = CONNECTION.cursor()
        sql = 'SELECT * FROM answers WHERE id=%s AND question_id=%s;'
        cursor.execute(sql, (answer_id, question_id))
        answer = cursor.fetchall()
        if answer:
            if answer[0][2] == int(current_identity):
                sql = 'UPDATE answers SET content = %s WHERE id=%s AND question_id=%s;'
                cursor.execute(sql, (update, answer_id, question_id))
                CONNECTION.commit()
                cursor.close()
                return jsonify({"201":"answer updated successfully"})
            return jsonify({"401":"Unauthorized, Ony answer ower can update answer"})
        return abort(404)
    return abort(400)


@BP.route('/upvote/<int:answer_id>', methods=['POST'])
@jwt_required()
def upvote_answer(answer_id):
    '''Upvote answers
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM answers WHERE id=%s;'
    cursor.execute(sql, ([int(answer_id)]))
    answer = cursor.fetchall()
    if answer:
        sql = 'SELECT * FROM votes WHERE id=%s AND voter=%s;'
        cursor.execute(sql, (int(answer[0][0]), int(current_identity)))
        voted = cursor.fetchall()
        if not voted:
            sql = 'UPDATE answers SET upvotes = upvotes + 1 WHERE id=%s;'
            cursor.execute(sql, ([answer_id]))
            CONNECTION.commit()
            cursor.close()
            return jsonify({"200":"Voted successfully"})
        return jsonify({'400':'You can only vote once'}), 400
    return abort(404)


@BP.route('/downvote/<int:answer_id>', methods=['POST'])
@jwt_required()
def downvote_answer(answer_id):
    '''downvote answers
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM answers WHERE id=%s;'
    cursor.execute(sql, ([int(answer_id)]))
    answer = cursor.fetchall()
    if answer:
        sql = 'SELECT * FROM votes WHERE id=%s AND voter=%s;'
        cursor.execute(sql, (answer_id, int(current_identity)))
        voted = cursor.fetchall()
        if not voted:
            sql = 'UPDATE answers SET downvotes = downvotes + 1 WHERE id=%s;'
            cursor.execute(sql, ([answer_id]))
            CONNECTION.commit()
            cursor.close()
            return jsonify({"200":"Voted successfully"})
        return jsonify({'400':'You can only vote once'}), 400
    return abort(404)


@BP.route('/accept/<int:answer_id>', methods=['POST'])
@jwt_required()
def accept_answer(answer_id):
    '''Mark answer as accepted
    '''
    cursor = CONNECTION.cursor()
    sql = 'SELECT * FROM answers WHERE id=%s;'
    cursor.execute(sql, ([int(answer_id)]))
    answer = cursor.fetchall()
    if answer:
        sql = 'SELECT * FROM questions WHERE id=%s AND question_owner=%s;'
        cursor.execute(sql, (int(answer[0][6]), int(current_identity)))
        question = cursor.fetchall()
        if question:
            sql = 'SELECT * FROM answers WHERE question_id=%s AND accepted=TRUE'
            cursor.execute(sql, ([int(answer[0][6])]))
            accepted = cursor.fetchall()
            if not accepted:
                sql = 'UPDATE answers SET accepted = TRUE WHERE id=%s;'
                cursor.execute(sql, ([answer[0][0]]))
                CONNECTION.commit()
                return jsonify({"200":"Answer Accepted"})
            return jsonify({"400":"You can only accept one answer per question"})
        return jsonify({"401":"Ony the question owner can accept answer"})
    return abort(404)
