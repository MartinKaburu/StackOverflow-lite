'''api endpoints
'''
from re import match

from flask import jsonify, Blueprint, abort, request
from flask_jwt import jwt_required, current_identity
from flask_cors import CORS

from app import CONNECTION
from app.api.v1.endpoint_models import Users, Questions, Answers


BP = Blueprint('api', __name__, url_prefix='/api/v1')
CORS(BP)
#BP.url_map.strict_slashes = False
input_format = r"(^[0-9_?!@#$%^&*/|\\]*$)"

@BP.route('/questions', methods=['GET', 'POST'])
@jwt_required()
def get_and_post():
    ''' get all questions
    Post a new question
    '''
    if request.method == 'GET':
        questions = Questions()
        questionz = questions.get_all()
        display = []
        if questionz:
            for question in questionz:
                retformat = {
                    "question_id":question[0],
                    "content":question[1],
                    "owner_id":question[2],
                    "username": questions.get_username(question[2]),
                    "posted_on": question[3].strftime('%B %d, %Y')
                }
                display.append(retformat)
            return jsonify({"QUESTIONS":display}), 200
        return jsonify({"message":"No questions posted yet"}), 404
    elif request.method == 'POST':
        if request.json and request.json['content']:
            content = request.json['content']
            question_owner = int(current_identity)
            question = Questions(question_owner, content)
            question.save()
            return jsonify({'message': 'Question added'}), 201
        return abort(400), 400


@BP.route('/questions/<int:question_id>', methods=['GET', 'DELETE', 'PUT'])
@jwt_required()
def get_delete_question(question_id):
    ''' get specific question
    '''
    question = Questions(int(current_identity))
    if request.method == 'GET':
        question = question.get_one(question_id)
        if question:
            answers = Answers(question_id)
            answerz = answers.get_by_question_id()
            display_ans = []
            for answer in answerz:
                answer = list(answer)
                retformat = {
                    "answer_id":answer[0],
                    "answer_content":answer[1],
                    "answer_owner":answer[2],
                    "upvotes":answer[3],
                    "downvotes":answer[4],
                    "accepted":answer[5],
                    "question_id":answer[6],
                    "username": answers.get_username(answer[2]),
                    "posted_on": answer[7].strftime('%B %d, %Y')
                }
                display_ans.append(retformat)
            display = {
                    "question_id": question[0][0],
                    "content": question[0][1],
                    "question_owner": question[0][2],
                    "answers": display_ans,
                    "username": answers.get_username(question[0][2]),
                    "posted_on": question[0][3].strftime('%B %d, %Y')
                }
            return jsonify(display), 200
        return abort(404), 404
    elif request.method == 'PUT':
        if request.json and request.json['content']:

            exists = question.get_one(question_id)
            if exists:
                authorized = question.get_by_both(question_id)
                if authorized:
                    content = request.json["content"]
                    question.edit_question(question_id, content)
                    return jsonify({"message":"Question updated successfully"}), 201
                return jsonify({"message":"Unauthorized, only question owner can edit question"}), 401
            return abort(404), 404
        return abort(400), 400
    que = question.get_one(question_id)
    if que:
        if int(current_identity) is que[0][2]:
            question.delete_question(question_id)
            return jsonify({'message':'Question deleted'}), 200
        return jsonify({"message":"Unauthorized: Only question owner can remove question"}), 401
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
            return jsonify({"message": "question answered"}), 201
        return abort(400), 400
    return abort(404), 404


@BP.route('/questions/<int:question_id>/answers/<int:answer_id>', methods=['PUT', 'POST', 'DELETE'])
@jwt_required()
def update_delete_accept(question_id, answer_id):
    ''' update an answer
    '''
    if request.method == 'PUT':
        if request.json and request.json['content']:
            content = request.json['content']
            answer = Answers(question_id, int(current_identity), content)
            return answer.update_answer(answer_id)
        return abort(400)
    elif request.method == 'POST':
        answer = Answers()
        ans = answer.get_by_answer_id(answer_id)
        if ans:
            answer = Answers(int(ans[0][6]))
            question = Questions(int(current_identity))
            que = question.get_by_both(question_id)
            if que:
                accepted = answer.accepted()
                if not accepted:
                    answer.accept(ans[0][0])
                    return jsonify({"message":"Answer Accepted"}), 200
                return jsonify({"message":"You can only accept one answer per question"}), 400
            return jsonify({"message":"Ony the question owner can accept answer"}), 401
        return abort(404)
    else:
        answer = Answers()
        exists = answer.exists(question_id, answer_id)
        if exists:
            authorized = answer.get_by_both(int(current_identity), answer_id)
            if authorized:
                answer.delete(answer_id)
                return jsonify({"message":"Answer deleted successfully"}), 200
            return jsonify({"message":"Only answer owner can delete answer"}), 400
        return abort(404)



@BP.route('/upvote/<int:answer_id>', methods=['POST'])
@jwt_required()
def upvote_answer(answer_id):
    '''Upvote answers
    '''
    answer = Answers()
    ans = answer.get_by_answer_id(answer_id)
    if ans:
        upvoted = answer.upvoted(answer_id, int(current_identity))
        if not upvoted:
            answer.upvote(answer_id, int(current_identity))
            return(jsonify({"message":"Voted successfully"})), 200
        return jsonify({"message":"You already voted"}), 400
    return abort(404)



@BP.route('/downvote/<int:answer_id>', methods=['POST'])
@jwt_required()
def downvote_answer(answer_id):
    '''downvote answers
    '''
    answer = Answers(None, int(current_identity))
    ans = answer.get_by_answer_id(answer_id)
    if ans:
        if not answer.downvoted(answer_id, int(current_identity)):
            answer.downvote(answer_id, int(current_identity))
            return jsonify({"message":"Voted successfully"}), 200
        return jsonify({'message':'You can only vote once'}), 400
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
                answers = Answers(question[0])
                question = list(question)
                question[0] = str(question[0])
                answerz = answers.get_by_question_id()
                display_ans = []
                for answer in answerz:
                    answer = list(answer)
                    retans = {
                        "answer_id":answer[0],
                        "answer_content":answer[1],
                        "answer_owner":answer[2],
                        "upvotes":answer[3],
                        "downvotes":answer[4],
                        "accepted":answer[5],
                        "question_id":answer[6],
                        "username": answers.get_username(answer[2]),
                        "posted_on": answer[7].strftime('%B %d, %Y')
                    }
                    display_ans.append(retans)
                retformat = {
                    "id":question[0],
                    "content":question[1],
                    "owner_id":question[2],
                    "answers":display_ans,
                    "username": answers.get_username(question[2]),
                    "posted_on": question[3].strftime('%B %d, %Y')
                }
                res.append(retformat)
            return jsonify({"RESULTS":res})
        return jsonify({"message":"No matching results"}), 404
    return jsonify({"message":"Missing parameters"}), 400


@BP.route('/questions/user', methods=['GET'])
@jwt_required()
def get_mine():
    '''get questions for the current user
    '''
    que = Questions(int(current_identity))
    questions = que.get_by_owner()
    display = []
    if questions:
        for question in questions:
            retformat = {
                "question_id":question[0],
                "content":question[1],
                "owner_id":question[2],
                "username": que.get_username(question[2]),
                "posted_on": question[3].strftime('%B %d, %Y')
            }
            display.append(retformat)
        return jsonify({"QUESTIONS":display}), 200
    return jsonify({"message":"Current user has no questions"}), 404
