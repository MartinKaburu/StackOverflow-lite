from datetime import timedelta
import os

class Development(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Th3Y_5@1D.t#3_H3@vEn5_4R3_0nLY_4_t#3_V1013Nt'
    JWT_AUTH_URL_RULE = '/api/v1/auth/login'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_AUTH_ENDPOINT = 'api_login'
    JWT_VERIFY_EXPIRATION = True
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_USER = os.environ.get('DATABASE_USER')
    JWT_EXPIRATION_DELTA = timedelta(seconds=3600)
    TRACK_MODIFICATIONS = True
    debug = True

class Test(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Th3Y_5@1D.t#3_H3@vEn5_4R3_0nLY_4_t#3_V1013Nt'
    JWT_AUTH_URL_RULE = '/api/v1/auth/login'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_AUTH_ENDPOINT = 'api_login'
    JWT_VERIFY_EXPIRATION = True
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_USER = os.environ.get('DATABASE_USER')
    TRACK_MODIFICATIONS = True
    debug = True
    JWT_EXPIRATION_DELTA = timedelta(seconds=3600)
