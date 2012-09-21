# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from model.question import Question
import answer as AnswerService

def update_answer_num(question_key):
  question = Question.get_by_id(question_key.id())
  if question:
    answers = AnswerService.get_answers_by_question(question_key)
    question.answers_num = len(answers)
    question.put()

