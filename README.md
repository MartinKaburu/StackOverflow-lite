# StackOverflow-lite

[![Build Status](https://travis-ci.com/MartinKaburu/StackOverflow-lite.png)](https://travis-ci.org/MartinKaburu/StackOverflow-lite)   [![codecov](https://codecov.io/gh/MartinKaburu/StackOverflow-lite/branch/development/graph/badge.svg)](https://codecov.io/gh/MartinKaburu/StackOverflow-lite)
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/6a89cd9ab95f70bbddda)

# github pages

        https://martinkaburu.github.io/StackOverflow-lite/index.html

# heroku hosting

        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/auth/signup

# USAGE:

        To get started visit:
        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/auth/signup
        methods['POST']
        headers['Content_Type':'application/json']
        body = {
                "username":"username",
                "email":"email",
                "password":"password"
                }
        
    
        login::
        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/auth/login
        methods['POST']
        headers['Content_Type':'application/json']
        body = {
                "email":"someone@gmail.com",
                "password":"password"
                }

# api endpoints::

        Get all questions::  
        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/questions
        methods=['GET']
        headers["Authorization":"JWT {access_token}"]
        returns json data of all the questions
        status_code 200

        Get specific question::
        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/questions/{int:question_id}
        methods=['GET']
        headers["Authorization":"JWT {access_token}"]
        returns json data on the question specified
        status_code 200

        Add a question::
        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/questions
        methods=['POST']
        headers['Content_Type':'application/json', "Authorization":"JWT {access_token}"]
        body['content':'the question']
        returns json data on the added question status_code 201
        or
        returns 400 incase 'content' or 'owner' keys were not specified in the json or the data is not in json format

        Answer a question::
        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/questions/{int:question_id}/answers
        methods=['POST']
        headers['Content_Type':'application/json', "Authorization":"JWT {access_token}"]
        body['answer_content':'the answer']
        returns json data on the answered question status_code 201
        or
        returns 400 incase 'answer_content' key is not specified in the json or the data type is not json
        
        Delete a question::
        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/questions/{int:question_id}
        methods=['DELETE']
        headers['Content_Type':'application/json', "Authorization":"JWT {access_token}"]
        returns 200 : "Question deleted", or 404, or 400 if the user is unauthorized
        
        Update answer::
        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/update/{question_id}/{answer_id}
        methods=['POST']
        headers["Authorization":"JWT {access_token}", "Content-Type":"application/json"]
        body = {
                "content":"answer update"
               }
        returns 201 if successfull, 404 if invaid answer, 401 in unauthorized
        
        upvote answer::
        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/upvote/1
        methods=['POST']
        headers["Authorization":"JWT {access_token}"]
        returns 200 if successfull, 404 if invalid answer, 401 if unauthorized access
        
        downvote answer::
        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/downvote/1
        methods=['POST']
        headers["Authorization":"JWT {access_token}"]
        returns 200 if successfull, 404 if invalid answer, 401 if unauthorized access
        
        Accept answer::
        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/accept/{answer_id}
        methods=['POST']
        headers["Authorization":"JWT {access_token}"]
        returns 201 when accepted, 404 invalid answer, 400 already voted, 401 unauthorized
# errors:
    400 bad request
    404 resource not found
    201 created
    200 Ok
