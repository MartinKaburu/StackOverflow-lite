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


    def test_register_user_with_same_email(self):
        '''Test user registration in persistent database
        '''
        head = {'Content-Type': 'application/json'}

        self.test_client().post('/api/v1/auth/signup',\
        data=json.dumps(self.reg_user), headers = head)

        user = self.test_client().post('/api/v1/auth/signup',\
        data=json.dumps(self.reg_user), headers = head)

        self.assertEqual(user.status_code, 400)
        self.assertIn("Email address has an account", user.data)


    def test_login_user_wrong_credentials(self):
        '''Test user with wrong credentials created
        '''
        head = {'Content-Type': 'application/json'}
        self.token = self.get_token()

        user = self.test_client().post('/api/v1/auth/login',\
        data=json.dumps(self.login_user_wrong), headers = head)

        try:
            self.jwt = self.split_jwt(user.json)
        except:
            pass
        self.assertEqual(user.status_code, 401)


    def test_register_user_invalid_email(self):
        '''Test user registration in persistent database
        '''
        head = {'Content-Type': 'application/json'}

        user = self.test_client().post('/api/v1/auth/signup',\
        data=json.dumps(self.reg_user_wrong), headers = head)

        self.assertEqual(user.status_code, 400)
        self.assertIn("Invalid email format", user.data)
