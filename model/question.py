# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from account import Account
from topic import Topic

# from google.appengine.ext.ndb import polymodel

# class QuestionDAO:
#   @classmethod
#   def delete(cls, key):
#     ndb.delete(key)
#polymodel.PolyModel
class Question(ndb.Model):
  title = ndb.StringProperty(required = True, indexed=False)
  description = ndb.TextProperty(default = '')
  answers_num = ndb.IntegerProperty(default = 0)
  creator = ndb.KeyProperty(kind = Account)
  created_date = ndb.DateTimeProperty(auto_now_add=True)
  # Shall we disable the index on topics column?
  topics = ndb.KeyProperty(kind = Topic, repeated = True)
