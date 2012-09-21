# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from question import Question

class Answer(ndb.Model):
  content = ndb.TextProperty(default = '')
  #auditing = in processing review
  status = ndb.StringProperty(default = 'normal', choices = ('normal', 'draft', 'collapsed', 'deleted', 'auditing'))
  author = ndb.UserProperty(auto_current_user_add = True)
  updated_date = ndb.DateTimeProperty(auto_now = True)
  created_date = ndb.DateTimeProperty(auto_now_add = True)
  question = ndb.KeyProperty(kind = Question)
