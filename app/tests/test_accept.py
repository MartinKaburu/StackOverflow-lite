'''Module to test mark answer as preferred functionality
'''
import json

from app.tests.setup_tests import BaseTest


class TestAccept(BaseTest):
    '''Test mark preferred functionality
    '''


    def test_accept_answer(self):
        """Test the user can accept specific answers
        """
        self.token = self.get_token()
        head = {'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)}

        self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers= head)

        self.test_client().post('/api/v1/questions/1/answers', \
        data=json.dumps(self.answer), headers = head)

        accept_answer = self.test_client().post('/api/v1/questions/1/answers/1', headers = head)
        self.assertEqual(accept_answer.status_code, 200)
        self.assertIn("Answer Accepted", accept_answer.data)



    def test_accept_answer_twice(self):
        """Test the user can accept specific answers
        """
        self.token = self.get_token()
        head = {'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)}

        self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers = head)

        self.test_client().post('/api/v1/questions/1/answers', \
        data=json.dumps(self.answer), headers = head)

        accept_answer = self.test_client().post('/api/v1/questions/1/answers/1', headers = head)
        self.assertEqual(accept_answer.status_code, 200)
        self.assertIn("Answer Accepted", accept_answer.data)
        accept_answer_twice = self.test_client().post('/api/v1/questions/1/answers/1', headers =  head)
        self.assertEqual(accept_answer_twice.status_code, 400)
