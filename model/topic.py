# coding=utf-8
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
# from question import Question
# from account import Account

class Topic(ndb.Model):
  display_name = ndb.TextProperty(default = '')
  url_token = ndb.TextProperty(default = '')
  avatar = ndb.TextProperty(default = '')
  
  def get_json_object(self):
    obj = {
      'id': self.key.id(),
      'display_name': self.display_name,
      'url_token': self.url_token,
      'avatar': self.avatar
    }

    return obj
  
  

