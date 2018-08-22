'''Module to create and drop database
'''
from app import CONNECTION

class DatabaseDriver(object):
    '''Class to define methods to drop and create tables
    '''
    def __init__(self):
        '''Create a cursor
        '''
        self.cursor = CONNECTION.cursor()

    def create_all(self):
        '''create db
        '''
        users = 'CREATE TABLE IF NOT EXISTS users(\
        id SERIAL PRIMARY KEY, \
        username varchar (32) NOT NULL, \
        email varchar (32) UNIQUE NOT NULL, \
        password VARCHAR (256) NOT NULL\
        );'

        questions = 'CREATE TABLE IF NOT EXISTS questions(\
        id SERIAL PRIMARY KEY,\
        content TEXT NOT NULL,\
        question_owner INT NOT NULL REFERENCES users(id)\
        );'

        answers = 'CREATE TABLE IF NOT EXISTS answers(\
        id SERIAL PRIMARY KEY, \
        content TEXT NOT NULL, \
        answer_owner INT NOT NULL REFERENCES users(id), \
        upvotes INT DEFAULT 0, \
        downvotes INT DEFAULT 0, \
        accepted BOOLEAN DEFAULT FALSE, \
        question_id INT NOT NULL REFERENCES questions(id)\
        );'

        votes = 'CREATE TABLE IF NOT EXISTS votes(\
        id SERIAL REFERENCES answers(id),\
        voter INT NOT NULL REFERENCES users(id) \
        );'

        self.cursor.execute(users)
        self.cursor.execute(questions)
        self.cursor.execute(answers)
        self.cursor.execute(votes)
        CONNECTION.commit()

    def drop_all(self):
        '''Drop database
        '''
        self.cursor = CONNECTION.cursor()
        self.cursor.execute('DROP TABLE votes, answers, questions, users;')
        CONNECTION.commit()
