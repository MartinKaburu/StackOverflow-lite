'''api endpoints
'''
from flask import jsonify, Blueprint, abort, request
from flask_jwt import jwt_required, current_identity
from flask_cors import CORS

from app import CONNECTION
from app.api.v1.endpoint_models import Users, Questions, Answers


BP = Blueprint('api', __name__, url_prefix='/api/v1')
CORS(BP)


@BP.route('/questions', methods=['GET', 'POST'])
@jwt_required()
def get_and_post():
    ''' get all questions
    Post a new question
    '''
    if request.method == 'GET':
        questions = Questions()
        questions = questions.get_all()
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
            content = request.json['content']
            question_owner = int(current_identity)
            question = Questions(question_owner, content)
            question.save()
            return jsonify({'201': 'Question added'}), 201
        return abort(400), 400


@BP.route('/questions/<int:question_id>', methods=['GET', 'DELETE'])
@jwt_required()
def get_delete_question(question_id):
    ''' get specific question
    '''
    question = Questions()
    if request.method == 'GET':
        display = []
        question = question.get_one(question_id)
        if question:
            answers = Answers(question_id)
            answers = answers.get_by_question_id()
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
            return jsonify(display), 200
        return abort(404), 404
    que = question.get_one(question_id)
    if que:
        if int(current_identity) is que[0][2]:
            question.delete_question(question_id)
            return jsonify({'Question deleted':'200'}), 200
        return jsonify({"401":"Unauthorized: Only question owner can remove question"})
    return abort(404), 404


@BP.route('/questions/<int:question_id>/answers', methods=['POST'])
@jwt_required()
def answer_question(question_id):
    '''answer a question
    '''
    question = Questions()
    question = question.get_one(question_id)
    if question:
        if request.json and request.json['answer_content']:
            content = request.json['answer_content']
            answer_owner = int(current_identity)
            answer = Answers(question_id, answer_owner, content)
            answer.add_answer()
            return jsonify({"201": "question answered"}), 201
        return abort(400), 400
    return abort(404), 404


@BP.route('/update/<int:question_id>/<int:answer_id>', methods=['PUT'])
@jwt_required()
def update(question_id, answer_id):
    ''' update an answer
    '''
    if request.json and request.json['content']:
        content = request.json['content']
        answer = Answers(question_id, int(current_identity), content)
        return answer.update_answer(answer_id)
    return abort(400)


@BP.route('/upvote/<int:answer_id>', methods=['POST'])
@jwt_required()
def upvote_answer(answer_id):
    '''Upvote answers
    '''
    answer = Answers(None, int(current_identity))
    ans = answer.get_by_answer_id(answer_id)
    if ans:
        voted = answer.voted(answer_id)
        if not voted:
            answer.upvote(answer_id)
            return jsonify({"200":"Voted successfully"})
        return jsonify({'400':'You can only vote once'}), 400
    return abort(404)


@BP.route('/downvote/<int:answer_id>', methods=['POST'])
@jwt_required()
def downvote_answer(answer_id):
    '''downvote answers
    '''
    answer = Answers(None, int(current_identity))
    ans = answer.get_by_answer_id(answer_id)
    if ans:
        if not answer.voted(answer_id):
            answer.downvote(answer_id)
            return jsonify({"200":"Voted successfully"})
        return jsonify({'400':'You can only vote once'}), 400
    return abort(404)


@BP.route('/accept/<int:answer_id>', methods=['POST'])
@jwt_required()
def accept_answer(answer_id):
    '''Mark answer as accepted
    '''
    answer = Answers()
    ans = answer.get_by_answer_id(answer_id)
    if ans:
        answer = Answers(int(ans[0][6]))
        question = Questions()
        que = question.get_one(int(ans[0][6]))
        if que:
            accepted = answer.accepted()
            if not accepted:
                answer.accept(ans[0][0])
                return jsonify({"200":"Answer Accepted"})
            return jsonify({"400":"You can only accept one answer per question"})
        return jsonify({"401":"Ony the question owner can accept answer"})
    return abort(404)


@BP.route('/search', methods=['POST'])
@jwt_required()
def search():
    '''search the db
    '''
    if request.json and request.json['search']:
        search = request.json['search']
        questions = Questions(0,search)
        results = questions.search()
        if results:
            res = []
            for question in results:
                answer = Answers()
                question = list(question)
                question[0] = str(question[0])
                answers = answer.get_by_question_id(question[0])
                display_ans = []
                for answer in answers:
                    answer = list(answer)
                    retans = {
                        "answer_id":answer[0],
                        "answer_content":answer[1],
                        "answer_owner":answer[2],
                        "upvotes":answer[3],
                        "downvotes":answer[4],
                        "accepted":answer[5],
                        "question_id":answer[6]
                    }
                    display_ans.append(retans)
                retformat = {
                    "id":question[0],
                    "content":question[1],
                    "owner_id":question[2],
                    "answers":display_ans
                }
                res.append(retformat)
            return jsonify({"RESULTS":res})
        return jsonify({"404":"No matching results"})
    return jsonify({"400":"Missing parameters"})
