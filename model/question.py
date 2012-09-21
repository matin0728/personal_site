# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

from google.appengine.ext.ndb import polymodel

# class QuestionDAO:
#   @classmethod
#   def delete(cls, key):
#     ndb.delete(key)

class Question(polymodel.PolyModel):
  title = ndb.StringProperty(required = True)
  description = ndb.TextProperty(default = '')
  answers_num = ndb.IntegerProperty(default = 0)
  created_date = ndb.DateTimeProperty(auto_now_add=True)
