# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from account import Account

class Comment(ndb.Model):
  content = ndb.TextProperty(default = '')
  author = ndb.KeyProperty(kind = Account)
  real_author = ndb.KeyProperty(kind = Account)
  created_date = ndb.DateTimeProperty(auto_now_add = True)
  # We dont need save the comment type field.
  # entity_type = ndb.StringProperty(choices = ['question', 'answer', 'list'], indexded = False)
  #NOTE: Do we really need this index? question is the 'parent' for current answer.
  # question = ndb.KeyProperty(kind = Question)
  #   content = ndb.TextProperty(default = '')
  #   source = ndb.TextProperty(default = '')
  #   up_voted_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  #   down_voted_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  #   no_help_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  #   vote_up_num = ndb.ComputedProperty(lambda self: len(self.up_voted_users))
  #   vote_down_num = ndb.ComputedProperty(lambda self: len(self.down_voted_users))
  #   comment_num = ndb.IntegerProperty(indexed = False)

