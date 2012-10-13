# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from model.answer import Answer
from model.answer_full import AnswerFull
from singleton import Singleton
from base_service import BaseService

class AnswerService(Singleton, BaseService):
  
  def get_answer_full_by_question(self, question_key):
    #return AnswerFull.query(AnswerFull.question == question_key).fetch()
    return 

  def get_answer_by_question(self, question_key, full_version = False):
    answers = Answer.query(ancestor = question_key).fetch()
    if not full_version:
      return answers
      
    answer_fulls = AnswerFull.query(ancestor = question_key).fetch()
    map_ = {}
    for a in answer_fulls:
      map_[a.key.string_id()] = a
    
    for a in answers:
      k = a.answer_full_key.string_id()
      if k in map_.keys():
        a.answer_full = map_[k]
      
    return answers
  