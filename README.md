# StackOverflow-lite

[![Build Status](https://travis-ci.org/MartinKaburu/StackOverflow-lite.svg?branch=development)](https://travis-ci.org/MartinKaburu/StackOverflow-lite)
[![codecov](https://codecov.io/gh/MartinKaburu/StackOverflow-lite/branch/master/graph/badge.svg)](https://codecov.io/gh/MartinKaburu/StackOverflow-lite)
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
        | Method | Endpoint | Public Access | Summary |
        | --- | --- | --- | --- |

        | **GET** | /api/v1/questions | FALSE | Get all questions |
        | **POST** | /api/v1/questions/{question_id} | FALSE | Post a question |
        | **POST** | /api/v1/questions | FALSE | Post a question |
        | **POST** | /api/v1/questions/{question_id}/answers | FALSE | Answer a question |
        | **DELETE** | /api/v1/questions/{question_id} | FALSE | Delete a specific question |
        | **POST** | /api/v1/update/{question_id}/{answer_id} | FALSE | Update an answer |
        | **POST** | /api/v1/upvote/{answer_id} | FALSE | Upvote an answer |
        | **POST** | /api/v1/downvote/{answer_id} | FALSE | downvote an answer |
        | **POST** | /api/v1/accept/{answer_id} | FALSE | accept an answer |
        | **POST** | /api/v1/search | FALSE | search for a question |

# status codes:
    400 bad request
    404 resource not found
    201 created
    200 Ok
