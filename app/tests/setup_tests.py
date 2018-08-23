from unittest import TestCase
import json

from app import APP
from app.instance.models import DatabaseDriver
from config import Test


class BaseTest(TestCase):
    def setUp(self):
        """Instantiate the class
        """
        self.test = DatabaseDriver()
        APP.config.from_object(Test)
        self.test.create_all()
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
        '''Create a new jwt for every test
        '''
        user = self.test_client().post('/api/v1/auth/signup',\
        data=json.dumps(self.reg_user), headers={'Content-Type': 'application/json'})
        user = self.test_client().post('/api/v1/auth/login',\
        data=json.dumps(self.login_user), headers={'Content-Type': 'application/json'})
        self.token = self.split_jwt(user.json)
        return self.token

    def split_jwt(self, jwt):
        jwt = json.dumps(jwt)
        null, jwt = jwt.split(' "')
        jwt, null = jwt.split('"}')
        return jwt


    def tearDown(self):
        '''Drop db after test
        '''
        self.test.drop_all()
