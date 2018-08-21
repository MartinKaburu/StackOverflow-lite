'''Test postgresql data
'''
import unittest
import json

from app import APP, CONNECTION
from config import Test

def split_jwt(jwt):
    jwt = json.dumps(jwt)
    null, jwt = jwt.split(' "')
    jwt, null = jwt.split('"}')
    return jwt

class ApiTests(unittest.TestCase):
    """This class holds all the test cases
    """

    def setUp(self):
        """Instantiate the class
        """
        self.app = APP
        self.app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
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

    def test_register_user(self):
        '''Test user registration in persistent database
        '''
        user = self.test_client().post('/api/v1/register',\
        data=json.dumps(self.reg_user), headers={'Content-Type': 'application/json'})
        self.assertEqual(user.status_code, 201)
        self.assertIn("User created successfully", user.data)

    def test_login_user(self):
        '''Test user was successfully created
        '''
        user = self.test_client().post('/api/v1/login',\
        data=json.dumps(self.login_user), headers={'Content-Type': 'application/json'})
        self.assertEqual(user.status_code, 200)

    def test_login_returns_jwt(self):
        '''Test login returns json web token
        '''
        jwt = self.test_client().post('/api/v1/login',\
        data=json.dumps(self.login_user), headers={'Content-Type': 'application/json'})
        self.assertIn("access_token", jwt.data)

    def test_jwt_validity(self):
        user = self.test_client().post('/api/v1/login', data=json.dumps(self.login_user), headers={'Content_Type':'application/json'})
        print(user.data)
        jwt = split_jwt(user.json)
        question = self.test_client().get('/api/v1/questions', headers={'Authentication': 'JWT '+jwt})


    def test_post_question(self):
        """Test that a user can post a new question
        """
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        self.assertIn('application/json', res.content_type)
        self.assertIn('Posted', res.data)

    def test_get_all_questions(self):
        """Test that a user can get all the questions as json
        """
        res = self.test_client().post('/api/v1/questions',\
        data=json.dumps(self.question), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        all_questions = self.test_client().get('/api/v1/questions')
        self.assertEqual(all_questions.status_code, 200)
        self.assertEqual('application/json', all_questions.content_type)
        self.assertIn("How to create an api?", all_questions.data)
        self.assertIn(str(4), str(all_questions.data))

    def test_get_specific_question(self):
        """Test the api to return specific question as per the question id"""
        # get the first question
        question = self.test_client().get('/api/v1/questions/1')
        self.assertEqual(question.status_code, 200)
        self.assertIn("How to create an api?", str(question.data))

    def test_post_answer(self):
        """Test to post an answer to a specific question
        """
        post_answer = self.test_client().post('/api/v1/questions/1/answers', \
        data=json.dumps(self.answer), headers={'Content-Type': 'application/json'})
        self.assertEqual('application/json', post_answer.content_type)
        self.assertIn(self.answer['answer_content'], str(post_answer.data))


if __name__ == '__main__':
    unittest.main()
