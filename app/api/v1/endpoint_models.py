'''Create models for the endpoints
'''
from flask import abort, jsonify
from werkzeug.security import generate_password_hash

from app import CONNECTION

class Users():
    '''create objects for users
    '''
    def __init__(self):
        '''instantiate user
        '''
        self.cursor = CONNECTION.cursor()

    def get_all(self, email):
        '''get all users from the db with their emails
        '''
        sql = 'SELECT * FROM users WHERE email=%s;'
        self.cursor.execute(sql, ([email]))
        return self.cursor.fetchall()


    def create_user(self, username, email, password):
        sql = 'INSERT INTO users(username, email, password) VALUES(%s, %s, %s);'
        password = generate_password_hash(password)
        self.cursor.execute(sql, (username, email, password))
        CONNECTION.commit()

class Questions():
    '''create objects for questions
    '''


    def __init__(self):
        '''instantiate question
        '''
        self.cursor = CONNECTION.cursor()


    def save(self, content, question_owner):
        '''post question to database
        '''
        sql = 'INSERT INTO questions(content, question_owner) VALUES (%s, %s);'
        self.cursor.execute(sql, (content, question_owner))
        CONNECTION.commit()


    def get_all(self):
        '''get all questions
        '''
        self.cursor.execute('SELECT * FROM questions;')
        questions = self.cursor.fetchall()
        return questions


    def get_one(self, question_id):
        '''get specific question
        '''
        sql = 'SELECT * FROM questions WHERE id=%s;'
        self.cursor.execute(sql, ([question_id]))
        question = self.cursor.fetchall()
        return question


    def delete_question(self, question_id):
        '''Delete a question
        '''
        sql = 'DELETE FROM answers WHERE question_id=%s;'
        self.cursor.execute(sql, ([question_id]))
        sql = 'DELETE FROM questions WHERE id=%s;'
        self.cursor.execute(sql, ([question_id]))
        CONNECTION.commit()


    def search(self, content):
        '''search for a question by content
        '''
        sql = 'SELECT * FROM questions WHERE content LIKE %s;'
        self.cursor.execute(sql, ([content]))
        res = self.cursor.fetchall()
        return res


class Answers():
    '''create object for answers
    '''


    def __init__(self):
        '''instantiate answer
        '''
        self.cursor = CONNECTION.cursor()


    def get_by_question_id(self, question_id):
        '''get answers by a spcific id
        '''
        sql = 'SELECT * FROM answers WHERE question_id=%s;'
        self.cursor.execute(sql, [question_id])
        answers = self.cursor.fetchall()
        return answers


    def get_by_answer_id(self, answer_id):
        '''get answers by a spcific answer_id
        '''
        sql = 'SELECT * FROM answers WHERE id=%s'
        self.cursor.execute(sql, [answer_id])
        answers = self.cursor.fetchall()
        return answers


    def add_answer(self, answer_owner, content, question_id):
        '''add an answer to the db
        '''
        sql = 'INSERT INTO answers(answer_owner, content, question_id) \
        VALUES (%s, %s, %s);'
        self.cursor.execute(sql, (answer_owner, content, question_id))
        CONNECTION.commit()


    def accepted(self, question_id):
        '''check of the question has been accepted
        '''
        sql = 'SELECT * FROM answers WHERE question_id=%s AND accepted=TRUE'
        self.cursor.execute(sql, ([question_id]))
        accepted = self.cursor.fetchall()
        return accepted


    def accept(self, answer_id):
        '''accept answer
        '''
        sql = 'UPDATE answers SET accepted = TRUE WHERE id=%s;'
        self.cursor.execute(sql, ([answer_id]))
        CONNECTION.commit()


    def voted(self, answer_id, voter):
        '''find out if user has voted before
        '''
        sql = 'SELECT * FROM votes WHERE id=%s AND voter=%s;'
        self.cursor.execute(sql, (answer_id, voter))
        voted = self.cursor.fetchall()
        return voted


    def upvote(self, answer_id):
        '''cast an upvote
        '''
        sql = 'UPDATE answers SET upvotes = upvotes + 1 WHERE id=%s;'
        self.cursor.execute(sql, ([answer_id]))
        CONNECTION.commit()


    def downvote(self, answer_id):
        '''cast a downvote
        '''
        sql = 'UPDATE answers SET upvotes = downvotes + 1 WHERE id=%s;'
        self.cursor.execute(sql, ([answer_id]))
        CONNECTION.commit()


    def update_answer(self, answer_id, question_id, update, current_identity):
        '''update answers with answer_id
        '''
        sql = 'SELECT * FROM answers WHERE id=%s AND question_id=%s;'
        self.cursor.execute(sql, (answer_id, question_id))
        answer = self.cursor.fetchall()
        if answer:
            if answer[0][2] == int(current_identity):
                sql = 'UPDATE answers SET content = %s WHERE id=%s AND question_id=%s;'
                self.cursor.execute(sql, (update, answer_id, question_id))
                CONNECTION.commit()
                return jsonify({"201":"answer updated successfully"})
            return jsonify({"401":"Unauthorized, Ony answer ower can update answer"})
        return abort(404)
