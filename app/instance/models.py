'''Module to create and drop database
'''
from app import CONNECTION

class DatabaseDriver(object):
    '''Class to define methods to drop and create tables
    '''


    def create_all(self):
        '''create db
        '''
        users = 'CREATE TABLE IF NOT EXISTS users(\
        id SERIAL PRIMARY KEY, \
        username varchar (32) NOT NULL, \
        email varchar (32) UNIQUE NOT NULL, \
        password VARCHAR (256) NOT NULL,\
        created_on DATE NOT NULL\
        );'

        questions = 'CREATE TABLE IF NOT EXISTS questions(\
        id SERIAL PRIMARY KEY,\
        content TEXT NOT NULL,\
        question_owner INT NOT NULL REFERENCES users(id),\
        posted_on DATE NOT NULL\
        );'

        answers = 'CREATE TABLE IF NOT EXISTS answers(\
        id SERIAL PRIMARY KEY, \
        content TEXT NOT NULL, \
        answer_owner INT NOT NULL REFERENCES users(id), \
        upvotes INT DEFAULT 0, \
        downvotes INT DEFAULT 0, \
        accepted BOOLEAN DEFAULT FALSE, \
        question_id INT NOT NULL REFERENCES questions(id),\
        posted_on DATE NOT NULL\
        );'

        votes = 'CREATE TABLE IF NOT EXISTS votes(\
        id SERIAL,\
        voter INT NOT NULL REFERENCES users(id), \
        upvote BOOLEAN DEFAULT FALSE,\
        downvote BOOLEAN DEFAULT FALSE\
        );'
        cursor = CONNECTION.cursor()
        cursor.execute(users)
        cursor.execute(questions)
        cursor.execute(answers)
        cursor.execute(votes)
        CONNECTION.commit()
        cursor.close()

    def drop_all(self):
        '''Drop tables
        '''
        cursor = CONNECTION.cursor()
        cursor.execute('DROP TABLE votes, answers, questions, users;')
        CONNECTION.commit()
        cursor.close()
