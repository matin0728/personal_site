# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from model.answer import Answer

def get_answers_by_question(question_key):
  return Answer.query(Answer.question == question_key).fetch()

  