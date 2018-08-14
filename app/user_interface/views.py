''' Render UI views
'''

from flask import render_template

from app import APP

@APP.route('/')
def login():
    ''' route to render login page on '/'
    '''
    return render_template('login.html')


@APP.route('/home')
def home():
    ''' route to render hom page
    '''
    return render_template('index.html')
