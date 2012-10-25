# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from question import Question
from account import Account

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
  content = ndb.TextProperty(default = '')
  source = ndb.TextProperty(default = '')
  up_voted_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  down_voted_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  no_help_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  vote_up_num = ndb.ComputedProperty(lambda self: len(self.up_voted_users))
  vote_down_num = ndb.ComputedProperty(lambda self: len(self.down_voted_users))
  comment_num = ndb.IntegerProperty(default = 0, indexed = False)
  
  def is_author(self, author):
    #can we compare like this?
    return author.key.id() == self.real_author.id()
  