# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from account import Account
from question import Question
from answer import Answer

class AccountXQuestion(ndb.Model):
  account = ndb.KeyProperty(kind = Account)
  question = ndb.KeyProperty(kind = Question)
  focused = ndb.BooleanProperty(default = False)
  # equals not intresting.
  muted = ndb.BooleanProperty(default = False)
  thanksed_answers = ndb.KeyProperty(kind = Answer, repeated = True, indexed = False)
  up_voted_answers = ndb.KeyProperty(kind = Answer, repeated = True, indexed = False)
  down_voted_answers = ndb.KeyProperty(kind = Answer, repeated = True, indexed = False)
  no_help_answers = ndb.KeyProperty(kind = Answer, repeated = True, indexed = False)
  #equals collection or list
  stared = ndb.KeyProperty(kind = Answer, repeated = True, indexed = False)
  is_anonymouse = ndb.BooleanProperty(default = False)