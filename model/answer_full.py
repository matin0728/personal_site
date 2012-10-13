# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from account import Account

class AnswerFull(ndb.Model):
  content = ndb.TextProperty(default = '')
  source = ndb.TextProperty(default = '')
  up_voted_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  down_voted_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  no_help_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  #who stared this answer.
  #stared_users = ndb.StringListProperty()
  #lists = ndb.KeyProperty()
  #NOTE: We fillin parent attribute with question object for answer_full, so it's no need to create
  #extra index as following.
  #question = ndb.KeyProperty(kind = Question)