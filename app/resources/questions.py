#!/usr/bin/python

'''define question as:

 question = {
    id: Integer {URI},
    owner: String {User who asked question},
    content: String {Actual question},
    answers: List of Dictionaries[
    {
        upvotes: Integer {number of upvotes},
        downvotes: Integer {number of downvotes},
        accepted: Boolean{True if marked correct by the question owner},
        answer_content: String {Actual answer},
        answer_owner: String {User who posted answer},
        date_answered: DateTime {Date answered}
    }
    ],
    date_asked: DateTime {Date asked},
    answered: Boolean {True if any of the answers has been accepted}
 }

QUESTIONS is a constant list of dictionaries

'''

from datetime import datetime as dt

QUESTIONS = [
    {
        'id': 1,
        'owner': '__user__1',
        'content': 'This is the very first question',
        'answers': [
            {
                'upvotes': 10,
                'downvotes': 2,
                'accepted': False,
                'answer_content': 'This is the first answer',
                'answer_owner': '__user__2',
                'date_answered': dt.utcnow()
            },
            {
                'upvotes': 10,
                'downvotes': 22,
                'accepted': True,
                'answer_content': 'This is the second answer',
                'answer_owner': '__user__2',
                'date_answered': dt.utcnow()
            },
            {
                'upvotes': 100,
                'downvotes': 2,
                'accepted': False,
                'answer_content': 'This is the third answer',
                'answer_owner': '__user__2',
                'date_answered': dt.utcnow()
            },
        ],
        'date_asked': dt.utcnow(),
        'answered': True  # [answer for answer in question['answers'] if answer['accepted'] is True]
    },
    {
        'id': 2,
        'owner': '__user__1',
        'content': 'This is the second question',
        'answers': [
            {
                'upvotes': 10,
                'downvotes': 2,
                'accepted': False,
                'answer_content': 'This is the first answer',
                'answer_owner': '__user__2',
                'date_answered': dt.utcnow()
            },
            {
                'upvotes': 10,
                'downvotes': 22,
                'accepted': True,
                'answer_content': 'This is the second answer',
                'answer_owner': '__user__2',
                'date_answered': dt.utcnow()
            },
            {
                'upvotes': 100,
                'downvotes': 2,
                'accepted': False,
                'answer_content': 'This is the third answer',
                'answer_owner': '__user__2',
                'date_answered': dt.utcnow()
            },
        ],
        'date_asked': dt.utcnow(),
        'answered': False
    },
    {
        'id': 3,
        'owner': '__user__1',
        'content': 'This is the very first question',
        'answers': [
            {
                'upvotes': 10,
                'downvotes': 2,
                'accepted': False,
                'answer_content': 'This is the first answer',
                'answer_owner': '__user__2',
                'date_answered': dt.utcnow()
            },
            {
                'upvotes': 10,
                'downvotes': 22,
                'accepted': True,
                'answer_content': 'This is the second answer',
                'answer_owner': '__user__2',
                'date_answered': dt.utcnow()
            },
            {
                'upvotes': 100,
                'downvotes': 2,
                'accepted': False,
                'answer_content': 'This is the third answer',
                'answer_owner': '__user__2',
                'date_answered': dt.utcnow()
            },
        ],
        'date_asked': dt.utcnow(),
        'answered': True
    }
]
