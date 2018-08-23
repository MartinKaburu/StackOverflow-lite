import json

from app.tests.setup_tests import BaseTest

class TestTokens(BaseTest):
    def test_login_returns_jwt(self):
        '''Test login returns json web token
        '''
        user = self.test_client().post('/api/v1/auth/signup',\
        data=json.dumps(self.reg_user), headers={'Content-Type': 'application/json'})
        jwt = self.test_client().post('/api/v1/auth/login',\
        data=json.dumps(self.login_user), headers={'Content-Type': 'application/json'})
        self.assertIn("access_token", jwt.data)

    def test_jwt_validity(self):
        user = self.test_client().post('/api/v1/auth/signup',\
        data=json.dumps(self.reg_user), headers={'Content-Type': 'application/json'})
        user = self.test_client().post('/api/v1/auth/login', data=json.dumps(self.login_user), \
        headers={'Content-Type':'application/json'})
        jwt = self.split_jwt(user.json)
        questions = self.test_client().get('/api/v1/questions', \
        headers={'Authorization': 'JWT {}'.format(jwt)})
        self.assertIn('"QUESTIONS"', questions.data)
