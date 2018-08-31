# StackOverflow-lite

[![Build Status](https://travis-ci.org/MartinKaburu/StackOverflow-lite.svg?branch=development)](https://travis-ci.org/MartinKaburu/StackOverflow-lite)
[![codecov](https://codecov.io/gh/MartinKaburu/StackOverflow-lite/branch/development/graph/badge.svg)](https://codecov.io/gh/MartinKaburu/StackOverflow-lite)
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/6a89cd9ab95f70bbddda)

# github pages

        https://martinkaburu.github.io/StackOverflow-lite/index.html

# heroku hosting

        https://kaburu-stackoverflowlite-cp3.herokuapp.com

# Documentation

        https://stackdoc.docs.apiary.io/

# clone repository

    git clone https://github.com/MartinKaburu/stackoverflow-lite.git

# setup runtime environment for the app:

    $> pip install virtualenv
    $> virtualenv venv
    $> source venv/bin/activate
    $> pip install -r requirements.txt

# setup configurations for tests:

      $>  export CONTEXT= TEST
      $>  export DATABASE_NAME= {YOUR_TEST_DB_NAME}
      $>  export DATABASE_HOST= localhost
      $>  export DATABASE_PASSWORD= {YOUR_TEST_DB_PASSWORD}
      $>  export DATABASE_USER= {YOUR_DB_USER}

# run tests:

    $> pip install pytest
    $> pytest app

# setup configurations for running the app:

    $> export CONTEXT= DEV
    $> export DATABASE_NAME= {YOUR_OTHER_DB_NAME}
    $> export DATABASE_HOST= localhost
    $> export DATABASE_PASSWORD= {YOUR_OTHER_DB_PASSWORD}
    $> export DATABASE_USER= {YOUR_DB_USER}
    $> export FLASK_APP=app
    $> export FLASK_ENV=development

# run the app with flask:

    $> flask run

# run the app with gunicorn:

    $> gunicorn app:APP

# Endpoints

  | Method | Endpoint | Public Access | Summary |
  | --- | --- | --- | --- |
  | **POST** | /api/v1/auth/login | TRUE | login a user |
  | **POST** | /api/v1/auth/signup | TRUE | signup a user |
  | **GET** | /api/v1/questions | FALSE | Get all questions |
  | **POST** | /api/v1/questions | FALSE | Post a question |
  | **POST** | /api/v1/questions/{question_id}/answers | FALSE | Answer a question |
  | **DELETE** | /api/v1/questions/{question_id} | FALSE | Delete a specific question |
  | **PUT** | /api/v1/questions/{question_id}/answers/{answer_id} | FALSE | Update an answer |
  | **POST** | /api/v1/upvote/{answer_id} | FALSE | Upvote an answer |
  | **POST** | /api/v1/downvote/{answer_id} | FALSE | downvote an answer |
  | **POST** | /api/v1/questions/{question_id}/answers/{answer_id} | FALSE | accept an answer |
  | **POST** | /api/v1/search | FALSE | search for a question |
  | **DELETE** | /api/v1/questions/{question_id}/answers/{answer_id} | FALSE | Delete an answer |
  | **GET** | /api/v1/questions/user | FALSE | get the current users questions |
