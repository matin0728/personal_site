# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

from google.appengine.ext.ndb import model


class Account(model.Model):
  nickname = ndb.StringProperty(required = True)
  avator = ndb.StringProperty(default='')
  bio = ndb.StringProperty(default='')
  user = ndb.UserProperty()
  regist_date = ndb.DateTimeProperty(auto_now_add = True)
