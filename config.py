import os

class Development(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Th3Y_5@1D.t#3_H3@vEn5_4R3_0nLY_4_t#3_V1013Nt' 
    JWT_AUTH_URL_RULE = '/api/v1/login'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_AUTH_ENDPOINT = 'api_login'
    JWT_VERIFY_EXPIRATION = True
    DATABASE_NAME = 'stackoverflow'
    DATABASE_HOST = 'localhost'
    DATABASE_PASSWORD = 'kaburu@andela'
    DATABASE_USER = 'postgres'
