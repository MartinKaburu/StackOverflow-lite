'''Module to test the delete functionality
'''
import json

from app.tests.setup_tests import BaseTest


class TestDelete(BaseTest):
    '''Class to test delete functionality
    '''


    def test_delete_question(self):
        """Test the user can delete questions they posted
        """
        self.token = self.get_token()
        head = {'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)}

        self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers = head)

        delete_question = self.test_client().delete('/api/v1/questions/1', headers = head)
        self.assertEqual(delete_question.status_code, 200)
        self.assertIn("Question deleted", delete_question.data)


    def test_delete_question_twice(self):
        """Test the user can delete questions they posted
        """
        self.token = self.get_token()
        head = {'Content-Type': 'application/json', 'Authorization': 'JWT {}'.format(self.token)}

        self.test_client().post('/api/v1/questions', \
        data=json.dumps(self.question), headers = head)

        self.test_client().delete('/api/v1/questions/1', \
        data=json.dumps(self.question), headers = head)

        delete_non_existing = self.test_client().delete('/api/v1/questions/1', headers = head)

        self.assertEqual(delete_non_existing.status_code, 404)
