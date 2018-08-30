# StackOverflow-lite

[![Build Status](https://travis-ci.org/MartinKaburu/StackOverflow-lite.svg?branch=development)](https://travis-ci.org/MartinKaburu/StackOverflow-lite)
[![codecov](https://codecov.io/gh/MartinKaburu/StackOverflow-lite/branch/development/graph/badge.svg)](https://codecov.io/gh/MartinKaburu/StackOverflow-lite)
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/6a89cd9ab95f70bbddda)

# github pages

        https://martinkaburu.github.io/StackOverflow-lite/index.html

# heroku hosting

        https://kaburu-stackoverflowlite-cp3.herokuapp.com/api/v1/auth/signup

# USAGE:
  1. Clone the repo
  2. Setup a virtualenvironment for the app
  3. Install all the dependancies from the requirements.txt
  4. Setup all the database configurations as environment variables in a .env file
  5. set the app CONTEXT variable as either TEST or DEV
  6. Run and smile 

  | Method | Endpoint | Public Access | Summary |
  | --- | --- | --- | --- |
  | **POST** | /api/v1/auth/login | TRUE | login a user |
  | **POST** | /api/v1/auth/signup | TRUE | signup a user |
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
