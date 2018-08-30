'''Module to test tokens
'''
import json

from app.tests.setup_tests import BaseTest


class TestTokens(BaseTest):
    '''Test tokens validity
    '''


    def test_login_returns_jwt(self):
        '''Test login returns json web token
        '''
        head = {'Content-Type': 'application/json'}

        self.test_client().post('/api/v1/auth/signup',\
        data=json.dumps(self.reg_user), headers = head)

        jwt = self.test_client().post('/api/v1/auth/login',\
        data=json.dumps(self.login_user), headers = head)

        self.assertIn("access_token", jwt.data)


    def test_jwt_validity(self):
        '''test returned jwt is valid
        '''
        head = {'Content-Type': 'application/json'}

        self.test_client().post('/api/v1/auth/signup',\
        data=json.dumps(self.reg_user), headers = head)

        user = self.test_client().post('/api/v1/auth/login', \
        data=json.dumps(self.login_user), headers = head)

        jwt = self.split_jwt(user.json)
        questions = self.test_client().get('/api/v1/questions', \
        headers={'Authorization': 'JWT {}'.format(jwt)})

        self.assertIn('"QUESTIONS"', questions.data)
