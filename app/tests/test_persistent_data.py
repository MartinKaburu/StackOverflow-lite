'''Test postgresql data
'''
import unittest
import json

from flask import jsonify

from app import APP, CONNECTION
from app.instance.models import DatabaseDriver
from config import Test


APP.config.from_object(Test)
test = DatabaseDriver()
print(APP.config['DATABASE_NAME'])

def split_jwt(jwt):
    print(jwt)
    jwt = json.dumps(jwt)
    null, jwt = jwt.split(' "')
    jwt, null = jwt.split('"}')
    jwt[0:1].strip('"')
    print(jwt)
    return jwt


class ApiTests(unittest.TestCase):
    """This class holds all the test cases
    """

    def setUp(self):
        """Instantiate the class
        """
        test.drop_all()
        test.create_all()
        self.app = APP
        self.test_client = self.app.test_client
        self.question = {
            "content":"How to create an api?"
        }
        self.answer = {
            "answer_content":"Read Miguel's blog and figure it out"
        }
        self.reg_user = {
    	   "username":"martinkaburu",
           "email":"martinkaburu.m@gmail.com",
           "password":"kaburu@andela"
        }
        self.login_user = {
            "email":"martinkaburu.m@gmail.com",
            "password":"kaburu@andela"
        }


    def get_token(self):
        '''Test user was successfully created
        '''
        user = self.test_client().post('/api/v1/register',\
        data=json.dumps(self.reg_user), headers={'Content-Type': 'application/json'})
        user = self.test_client().post('/api/v1/login',\
        data=json.dumps(self.login_user), headers={'Content-Type': 'application/json'})
        self.token = split_jwt(user.json)
        return self.token

    def test_register_user(self):
        '''Test user registration in persistent database
        '''
        user = self.test_client().post('/api/v1/register',\
        data=json.dumps(self.reg_user), headers={'Content-Type': 'application/json'})
        self.assertEqual(user.status_code, 201)
        self.assertIn("user created successfully", user.data)

    def test_login_user(self):
        '''Test user was successfully created
        '''
        self.token = self.get_token()
        user = self.test_client().post('/api/v1/login',\
        data=json.dumps(self.login_user), headers={'Content-Type': 'application/json'})
        self.jwt = split_jwt(user.json)
        self.assertEqual(user.status_code, 200)

    def test_login_returns_jwt(self):
        '''Test login returns json web token
        '''
        user = self.test_client().post('/api/v1/register',\
        data=json.dumps(self.reg_user), headers={'Content-Type': 'application/json'})
        jwt = self.test_client().post('/api/v1/login',\
        data=json.dumps(self.login_user), headers={'Content-Type': 'application/json'})
        self.assertIn("access_token", jwt.data)

    def test_jwt_validity(self):
        user = self.test_client().post('/api/v1/register',\
        data=json.dumps(self.reg_user), headers={'Content-Type': 'application/json'})
        user = self.test_client().post('/api/v1/login', data=json.dumps(self.login_user), headers={'Content-Type':'application/json'})
        jwt = split_jwt(user.json)
        questions = self.test_client().get('/api/v1/questions', headers={'Authorization': 'JWT {}'.format(jwt)})
        self.assertIn('"QUESTIONS"', questions.data)


    def test_post_question(self):
        """Test that a user can post a new question
        """
        self.token = self.get_token()
        self.token = self.get_token()
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)
        self.assertIn('application/json', res.content_type)
        self.assertIn('Question added', res.data)
        self.assertEqual(res.status_code, 201)

    def test_get_all_questions(self):
        """Test that a user can get all the questions as json
        """
        self.token = self.get_token()
        res = self.test_client().post('/api/v1/questions',\
        data=json.dumps(self.question), headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)
        all_questions = self.test_client().get('/api/v1/questions', headers={'Authorization': 'JWT {}'.format(self.token)})

        self.assertEqual(all_questions.status_code, 200)
        self.assertEqual('application/json', all_questions.content_type)
        self.assertIn("How to create an api?", all_questions.data)

        cursor = CONNECTION.cursor()
        cursor.execute('SELECT * FROM questions;')
        questions = cursor.fetchall()
        cursor.close()
        all = '"QUESTIONS"'
        self.assertIn(all, json.dumps(all_questions.json))

    def test_get_specific_question(self):
        """Test the api to return specific question as per the question id"""
        self.token = self.get_token()
        post_question = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        question = self.test_client().get('/api/v1/questions/1', headers={'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(question.status_code, 200)
        self.assertIn("How to create an api?", str(question.data))

    def test_post_answer(self):
        """Test to post an answer to a specific question
        """
        self.token = self.get_token()
        post_question = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        post_answer = self.test_client().post('/api/v1/questions/1/answers', \
        data=json.dumps(self.answer), headers={'Content-Type': 'application/json', "Authorization": 'JWT {}'.format(self.token)})
        self.assertEqual('application/json', post_answer.content_type)
        self.assertIn("question answered", str(post_answer.data))


if __name__ == '__main__':
    unittest.main()
