'''api endpoints:
    /api/v1/get_all
        methods=['GET']
        returns json data of all the questions
        status_code 200
    /api/v1/get_question/<int:question_id>
        methods=['GET']
        returns json data on the question specified
        status_code 200
    /api/v1/post_question
        methods=['POST']
        returns json data on the added question
        status_code 201
    /api/v1/post_answer/<int:question_id>
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

# from app.resources.questions import QUESTIONS

QUESTIONS = []

BP = Blueprint('api', __name__, url_prefix='/api/v1')


@BP.route('/questions', methods=['GET'])
def get_all():
    ''' get all questions
    '''
    return jsonify({'QUESTIONS': QUESTIONS}), 200


@BP.route('/questions/<int:question_id>')
def get_question(question_id):
    ''' get specific question
    '''
    question = [question for question in QUESTIONS if question['id'] == question_id]
    if not question:
        abort(404)
    return jsonify({'question': question[0]}), 200


@BP.route('/post_question', methods=['POST'])
def add_question():
    ''' add a question
    '''
    if request.json and request.json['owner'] and request.json['content']:
        try:
            question = {
                'id': QUESTIONS[-1]['id']+1,
                'owner': request.json['owner'],
                'content': request.json['content'],
                'answers': [
                    {
                        'upvotes': 0,
                        'downvotes': 0,
                        'accepted': False,
                        'answer_content': '',
                        'answer_owner': '',
                        'date_answered': dt.utcnow()
                    }
                ],
                'date_asked': dt.utcnow(),
                'answered': False
            }
        except IndexError:
            question = {
                'id': 1,
                'owner': request.json['owner'],
                'content': request.json['content'],
                'answers': [
                    {
                        'upvotes': 0,
                        'downvotes': 0,
                        'accepted': False,
                        'answer_content': '',
                        'answer_owner': '',
                        'date_answered': dt.utcnow()
                    }
                ],
                'date_asked': dt.utcnow(),
                'answered': False
            }
        QUESTIONS.append(question)
        return jsonify({'question': question}), 201

    abort(400)


@BP.route('/questions/<int:question_id>/answers', methods=['POST'])
def answer_question(question_id):
    '''answer a question
    '''
    question = [question for question in QUESTIONS if question['id'] == question_id]
    if not question:
        abort(404)
    else:
        if request.json and request.json['answer_content'] and request.json['answer_owner']:
            answer = {
                "answer_owner": request.json['answer_owner'],
                "answer_content": request.json['answer_content'],
                "accepted": False,
                "upvotes": 0,
                "downvotes": 0,
                "date_answered": dt.utcnow()
            }
            question[0]['answers'].append(answer)
            return jsonify({"question": question}), 201
        else:
            abort(400)
