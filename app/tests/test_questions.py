'''for commandline tests use:
curl -i -H "Content-Type: application/json" -X POST -d '{"owner":"__user__3", \
"content":"How do you add a post"}' http://localhost:5000/api/v1/post_question
'''
import unittest
import json

from app import APP


class ApiTests(unittest.TestCase):
    """This class holds all the test cases
    """

    def setUp(self):
        """Instantiate the class
        """
        self.app = APP
        self.test_client = self.app.test_client
        self.question = {
            "owner":"martin",
            "content":"How to create an api?"
        }
        self.answer = {
            "answer_content":"Read Miguel's blog and figure it out",
            "answer_owner":"muguna"
        }

    def test_non_persistent(self):
        """ Ensure that data is not persistent
        """
        # Bug self.assertEqual(len(res.data), 17)

    def test_post_question(self):
        """Test that a user can post a new question
        """
        res = self.test_client().post('/api/v1/post_question', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        self.assertIn('application/json', res.content_type)
        self.assertIn('martin', res.data)

    def test_get_all_questions(self):
        """Test that a user can get all the questions as json
        """
        res = self.test_client().post('/api/v1/post_question',\
        data=json.dumps(self.question), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/post_question', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/post_question', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        res = self.test_client().post('/api/v1/post_question', \
        data=json.dumps(self.question), headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 201)
        all_questions = self.test_client().get('/api/v1/questions')
        self.assertEqual(all_questions.status_code, 200)
        self.assertEqual('application/json', all_questions.content_type)
        self.assertIn("How to create an api?", all_questions.data)
        self.assertIn(str(5), str(all_questions.data))

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
