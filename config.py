from datetime import timedelta
import os

class Development(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Th3Y_5@1D.t#3_H3@vEn5_4R3_0nLY_4_t#3_V1013Nt'
    JWT_AUTH_URL_RULE = '/api/v1/auth/login'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_AUTH_ENDPOINT = 'api_login'
    JWT_VERIFY_EXPIRATION = True
    DATABASE_NAME = 'd5gcv7646io26h'
    DATABASE_HOST = 'ec2-107-22-221-60.compute-1.amazonaws.com'
    DATABASE_PASSWORD = '245e9cfaaa8251df376234a231ebe0205ed5fb6264a8e9c9b689eee128dda3a9'
    DATABASE_USER = 'ogsfvuckhnbkgu'
    JWT_EXPIRATION_DELTA = timedelta(seconds=1800)
    TRACK_MODIFICATIONS = True
    debug = True

class Test(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Th3Y_5@1D.t#3_H3@vEn5_4R3_0nLY_4_t#3_V1013Nt'
    JWT_AUTH_URL_RULE = '/api/v1/auth/login'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_AUTH_ENDPOINT = 'api_login'
    JWT_VERIFY_EXPIRATION = True
    DATABASE_NAME = 'stackoverflow_test'
    DATABASE_HOST = 'localhost'
    DATABASE_PASSWORD = 'kaburu@andela'
    DATABASE_USER = 'postgres'
    TRACK_MODIFICATIONS = True
    debug = True
    JWT_EXPIRATION_DELTA = timedelta(seconds=1800)
