'''Modulle to test authentication
'''
import json

from app.tests.setup_tests import BaseTest


class TestAuth(BaseTest):
    '''class to test authentication
    '''
    def test_register_user(self):
        '''Test user registration in persistent database
        '''
        head = {'Content-Type': 'application/json'}
        user = self.test_client().post('/api/v1/auth/signup',\
        data=json.dumps(self.reg_user), headers = head)
        self.assertEqual(user.status_code, 201)
        self.assertIn("user created successfully", user.data)

    def test_login_user(self):
        '''Test user was successfully created
        '''
        head = {'Content-Type': 'application/json'}
        self.token = self.get_token()
        user = self.test_client().post('/api/v1/auth/login',\
        data=json.dumps(self.login_user), headers = head)
        self.jwt = self.split_jwt(user.json)
        self.assertEqual(user.status_code, 200)
