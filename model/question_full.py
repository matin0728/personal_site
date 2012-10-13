# coding=utf-8

import datetime
from google.appengine.ext import ndb
from account import Account

class Question(ndb.Model):
  focused_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  # do we need this?
  #muted_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  invited_users = ndb.KeyProperty(kind = Account, repeated = True, indexed = False)
  summary = ndb.TextProperty(default = '')
  view_times = ndb.IntegerProperty()
  