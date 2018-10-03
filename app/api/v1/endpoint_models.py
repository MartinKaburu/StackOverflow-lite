'''Create models for the endpoints
'''
from datetime import datetime as dt

from flask import abort, jsonify
from werkzeug.security import generate_password_hash

from app import CONNECTION

class Users():
    '''create objects for users
    '''
    def __init__(self, email, username=None, password=None):
        '''instantiate user
        '''
        self.cursor = CONNECTION.cursor()
        self.email = email
        self.username = username
        self.password = password

    def get_all(self):
        '''get all users from the db with their emails
        '''
        sql = 'SELECT * FROM users WHERE email=%s;'
        self.cursor.execute(sql, ([self.email]))
        return self.cursor.fetchall()


    def create_user(self):
        date = dt.now()
        sql = 'INSERT INTO users(username, email, password, created_on) VALUES(%s, %s, %s, %s);'
        self.password = generate_password_hash(self.password)
        self.cursor.execute(sql, (self.username, self.email, self.password, date))
        CONNECTION.commit()

class Questions():
    '''create objects for questions
    '''


    def __init__(self, question_owner=None, content=None):
        '''instantiate question
        '''
        self.date = dt.now()
        self.cursor = CONNECTION.cursor()
        self.content = content
        self.question_owner = question_owner


    def save(self):
        '''post question to database
        '''
        sql = 'INSERT INTO questions(question_owner, content, posted_on) VALUES (%s, %s, %s);'
        self.cursor.execute(sql, (self.question_owner, self.content, self.date))
        CONNECTION.commit()


    def get_all(self):
        '''get all questions
        '''
        self.cursor.execute('SELECT * FROM questions ORDER BY posted_on DESC;')
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

    def get_by_owner(self):
        sql = 'SELECT * FROM questions WHERE question_owner=%s ORDER BY posted_on DESC;'
        self.cursor.execute(sql, ([self.question_owner]))
        ans = self.cursor.fetchall()
        return ans

    def search(self):
        '''search for a question by content
        '''
        content = '%'+self.content+'%'
        sql = 'SELECT * FROM questions WHERE content LIKE LOWER(%s);'
        self.cursor.execute(sql, ([content]))
        res = self.cursor.fetchall()
        return res

    def get_by_both(self, question_id):
        sql = 'SELECT * FROM questions WHERE question_owner=%s AND id=%s;'
        self.cursor.execute(sql, (self.question_owner, question_id))
        ans = self.cursor.fetchall()
        return ans

    def get_username(self, id):
        sql = 'SELECT * FROM users WHERE id=%s;'
        self.cursor.execute(sql, ([id]))
        user = self.cursor.fetchone()
        return user[1]

    def edit_question(self, question_id, content):
        sql = 'UPDATE questions SET content=%s WHERE id=%s;'
        self.cursor.execute(sql, (content, question_id))




class Answers():
    '''create object for answers
    '''


    def __init__(self, question_id=None, answer_owner=None, content=None):
        '''instantiate answer
        '''
        self.cursor = CONNECTION.cursor()
        self.question_id = question_id
        self.answer_owner = answer_owner
        self.content = content
        self.date = dt.now()



    def get_by_question_id(self):
        '''get answers by a spcific id
        '''
        sql = 'SELECT * FROM answers WHERE question_id=%s ORDER BY posted_on DESC;'
        self.cursor.execute(sql, [self.question_id])
        answers = self.cursor.fetchall()
        return answers


    def get_by_answer_id(self, answer_id):
        '''get answers by a spcific answer_id
        '''
        sql = 'SELECT * FROM answers WHERE id=%s ORDER BY posted_on DESC'
        self.cursor.execute(sql, [answer_id])
        answers = self.cursor.fetchall()
        return answers


    def add_answer(self):
        '''add an answer to the db
        '''
        sql = 'INSERT INTO answers(answer_owner, content, question_id, posted_on) \
        VALUES (%s, %s, %s, %s);'
        self.cursor.execute(sql, (self.answer_owner, self.content, self.question_id, self.date))
        CONNECTION.commit()


    def accepted(self):
        '''check of the question has been accepted
        '''
        sql = 'SELECT * FROM answers WHERE question_id=%s AND accepted=TRUE'
        self.cursor.execute(sql, ([self.question_id]))
        accepted = self.cursor.fetchall()
        return accepted


    def accept(self, answer_id):
        '''accept answer
        '''
        sql = 'UPDATE answers SET accepted = TRUE WHERE id=%s;'
        self.cursor.execute(sql, ([answer_id]))
        CONNECTION.commit()


    def upvoted(self, answer_id, current_identity):
        '''find out if user has voted before
        '''
        sql = 'SELECT * FROM votes WHERE id=%s AND voter=%s AND upvote=TRUE;'
        self.cursor.execute(sql, (answer_id, current_identity))
        voted = self.cursor.fetchall()
        return voted

    def downvoted(self, answer_id, current_identity):
        '''find out if user has voted before
        '''
        sql = 'SELECT * FROM votes WHERE id=%s AND voter=%s AND downvote=TRUE;'
        self.cursor.execute(sql, (answer_id, current_identity))
        voted = self.cursor.fetchall()
        return voted


    def upvote(self, answer_id, current_identity):
        '''cast an upvote
        '''
        sql = 'SELECT * FROM votes WHERE id=%s AND voter=%s AND downvote=TRUE;'
        self.cursor.execute(sql, (answer_id, current_identity))
        vote = self.cursor.fetchall()
        if vote:
            sql = 'UPDATE answers SET downvotes = downvotes-1 WHERE id=%s;'
            self.cursor.execute(sql, ([answer_id]))
            sql = 'UPDATE votes SET downvote=FALSE WHERE id=%s AND voter=%s;'
            self.cursor.execute(sql, (answer_id, current_identity))
            CONNECTION.commit()
        sql = 'UPDATE answers SET upvotes = upvotes + 1 WHERE id=%s;'
        self.cursor.execute(sql, ([answer_id]))
        sql = 'INSERT INTO votes(upvote, id, voter) VALUES(TRUE, %s, %s);'
        self.cursor.execute(sql, (answer_id, current_identity))
        CONNECTION.commit()


    def downvote(self, answer_id, current_identity):
        '''cast a downvote
        '''
        sql = 'SELECT * FROM votes WHERE id=%s AND voter=%s AND upvote=TRUE;'
        self.cursor.execute(sql, (answer_id, current_identity))
        vote = self.cursor.fetchall()
        if vote:
            sql = 'UPDATE answers SET upvotes = upvotes-1 WHERE id=%s;'
            self.cursor.execute(sql, ([answer_id]))
            sql = 'UPDATE votes SET upvote=FALSE WHERE id=%s AND voter=%s;'
            self.cursor.execute(sql, (answer_id, current_identity))
            CONNECTION.commit()
        sql = 'UPDATE answers SET downvotes = downvotes + 1 WHERE id=%s;'
        self.cursor.execute(sql, ([answer_id]))
        sql = 'INSERT INTO votes(downvote, id, voter) VALUES(TRUE, %s, %s);'
        self.cursor.execute(sql, (answer_id, current_identity))
        CONNECTION.commit()


    def update_answer(self, answer_id):
        '''update answers with answer_id
        '''
        sql = 'SELECT * FROM answers WHERE id=%s AND question_id=%s;'
        self.cursor.execute(sql, (answer_id, self.question_id))
        answer = self.cursor.fetchall()
        if answer:
            if answer[0][2] == int(self.answer_owner):
                sql = 'UPDATE answers SET content = %s WHERE id=%s AND question_id=%s;'
                self.cursor.execute(sql, (self.content, answer_id, self.question_id))
                CONNECTION.commit()
                return jsonify({"message":"answer updated successfully"}), 201
            return jsonify({"message":"Unauthorized, Ony answer ower can update answer"}), 401
        return abort(404)


    def get_by_owner(self, owner):
        sql = 'SELECT * FROM answers WHERE answer_owner=%s ORDER BY posted_on DESC;'
        self.cursor.execute(sql, ([owner]))
        ans = self.cursor.fetchall()
        return ans


    def get_by_both(self, owner, answer_id):
        sql = 'SELECT * FROM answers WHERE answer_owner=%s AND id=%s;'
        self.cursor.execute(sql, (owner, answer_id))
        ans = self.cursor.fetchall()
        return ans


    def delete(self, answer_id):
        sql = 'DELETE FROM answers WHERE id=%s;'
        self.cursor.execute(sql, ([answer_id]))
        CONNECTION.commit()


    def exists(self, question_id, answer_id):
        sql = 'SELECT * FROM answers WHERE question_id=%s AND id=%s;'
        self.cursor.execute(sql, (question_id, answer_id))
        ans = self.cursor.fetchone()
        return ans

    def get_username(self, id):
        sql = 'SELECT * FROM users WHERE id=%s;'
        self.cursor.execute(sql, ([id]))
        user = self.cursor.fetchone()
        return user[1]
