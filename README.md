# StackOverflow-lite

[![Build Status](https://travis-ci.com/MartinKaburu/StackOverflow-lite.png)](https://travis-ci.com/MartinKaburu/StackOverflow-lite)   [![codecov](https://codecov.io/gh/MartinKaburu/StackOverflow-lite/branch/master/graph/badge.svg)](https://codecov.io/gh/MartinKaburu/StackOverflow-lite)

# github pages

https://martinkaburu.github.io/StackOverflow-lite/index.html

# heroku hosting

https://stacksverflow-lite.herokuapp.com

# USAGE:

To get started visit:
        https://stacksverflow-lite.herokuapp.com

# api endpoints:

->Get all questions  
https://stacksverflow-lite.herokuapp.com/api/v1/questions

methods=['GET']

returns json data of all the questions

status_code 200

->Get specific question
https://stacksverflow-lite.herokuapp.com/api/v1/questions/<int:question_id>
methods=['GET']
returns json data on the question specified
status_code 200

->Add a question \n
https://stacksverflow-lite.herokuapp.com/api/v1/post_question
methods=['POST']
headers['Content_Type':'application/json']
body['owner':'username','content':'the question']

returns json data on the added question status_code 201
or 
returns 400 incase 'content' or 'owner' keys were not specified

Answer a question
https://stacksverflow-lite.herokuapp.com/api/v1/questions/<int:question_id>/answers
methods=['POST']
headers['Content_Type':'application/json']
body['answer_owner':'username','answer_content':'the answer']

returns json data on the answered question status_code 201
or 
returns 400 incase 'answer_content' or 'answer_owner' keys were not specified

# errors:
    400 bad request
    404 resource not found
    201 created
    200 Ok
