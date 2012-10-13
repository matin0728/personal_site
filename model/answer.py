# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from question import Question
from account import Account
from answer_full import AnswerFull

class Answer(ndb.Model):
  summary = ndb.TextProperty(default = '')
  #recently voted user.
  # recent_voted_users = ndb.StringListProperty()
  #auditing = in processing review
  status = ndb.StringProperty(default = 'normal', choices = ('normal', 'draft', 'collapsed', 'deleted', 'auditing'))
  author = ndb.KeyProperty(kind = Account)
  real_author = ndb.KeyProperty(kind = Account)
  updated_date = ndb.DateTimeProperty(auto_now = True)
  created_date = ndb.DateTimeProperty(auto_now_add = True)
  #NOTE: Do we really need this index? question is the 'parent' for current answer.
  question = ndb.KeyProperty(kind = Question)
  answer_full_key = ndb.KeyProperty(kind = AnswerFull)
  #NOTE: answer_full is a placeholder, will be fillin at entity query.
  answer_full = None
  
  def get_extra(self):
    if not self.answer_full:
      self.answer_full = self.answer_full_key.get()
      
    return self.answer_full
  
  def is_author(self, author):
    #can we compare like this?
    return author.key.id() == self.real_author.id()
  