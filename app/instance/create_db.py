'''Module to create database
Should only be run once
'''
import psycopg2 as psycopg

from app import CONNECTION, APP
cursor = CONNECTION.cursor()

users = 'CREATE TABLE users(\
    id SERIAL PRIMARY KEY, \
    username varchar (32) NOT NULL, \
    email varchar (32) UNIQUE NOT NULL, \
    password VARCHAR (256) NOT NULL\
    );'

questions = 'CREATE TABLE questions(\
        id SERIAL PRIMARY KEY,\
        content TEXT NOT NULL,\
        question_owner INT NOT NULL REFERENCES users(id)\
        );'

answers = 'CREATE TABLE answers(\
    id SERIAL PRIMARY KEY, \
    content TEXT NOT NULL, \
    answer_owner INT NOT NULL REFERENCES users(id), \
    upvotes INT DEFAULT 0, \
    downvotes INT DEFAULT 0, \
    accepted BOOLEAN DEFAULT FALSE, \
    question_id INT NOT NULL REFERENCES questions(id),\
    voters VARCHAR[] \
    );'

votes = 'CREATE TABLE votes(\
id SERIAL REFERENCES answers(id)
voter INT NOT NULL REFERENCES users(id), \

);'

try:
    sql = 'CREATE DATABASE %s;'
    cursor.execute(sql, APP.config['DATABASE_NAME'])
    CONNECTION.commit()
except:
    pass

cursor.execute(users)
cursor.execute(questions)
cursor.execute(answers)
CONNECTION.commit()
cursor.close()
