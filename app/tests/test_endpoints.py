'''Test endpoints functionality
'''
import json

from app import CONNECTION
from app.tests.setup_tests import BaseTest


class TestEndpoints(BaseTest):
    '''Test all endpoints
    '''
    def test_post_question(self):
        """Test that a user can post a new question
        """
        self.token = self.get_token()
        self.token = self.get_token()
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), \
        headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)
        self.assertIn('application/json', res.content_type)
        self.assertIn('Question added', res.data)
        self.assertEqual(res.status_code, 201)

    def test_get_all_questions(self):
        """Test that a user can get all the questions as json
        """
        self.token = self.get_token()
        res = self.test_client().post('/api/v1/questions',\
        data=json.dumps(self.question), \
        headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), \
        headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), \
        headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), \
        headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)
        all_questions = self.test_client().get('/api/v1/questions', \
        headers={'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(all_questions.status_code, 200)
        self.assertEqual('application/json', all_questions.content_type)
        self.assertIn("How to create an api?", all_questions.data)
        cursor = CONNECTION.cursor()
        cursor.execute('SELECT * FROM questions;')
        questions = cursor.fetchall()
        cursor.close()
        self.assertIn(questions[0][1], all_questions.data)

    def test_get_specific_question(self):
        """Test the api to return specific question as per the question id"""
        self.token = self.get_token()
        self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), \
        headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        question = self.test_client().get('/api/v1/questions/1', \
        headers={'Authorization': 'JWT {}'.format(self.token)})
        self.assertEqual(question.status_code, 200)
        self.assertIn("How to create an api?", str(question.data))

    def test_post_answer(self):
        """Test to post an answer to a specific question
        """
        self.token = self.get_token()
        self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), \
        headers={'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)})
        post_answer = self.test_client().post('/api/v1/questions/1/answers', \
        data=json.dumps(self.answer), \
        headers={'Content-Type': 'application/json', "Authorization": 'JWT {}'.format(self.token)})
        self.assertEqual('application/json', post_answer.content_type)
        self.assertIn("question answered", str(post_answer.data))
