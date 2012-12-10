# coding=utf-8

#TODO: Move account creation logic here.

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from model import *
from singleton import Singleton
from base_service import BaseService

class AccountService(Singleton, BaseService):
  def update_nick_name(self, nick_name, account):
    error_message = []
    if not nick_name:
      error_message.append(u'昵称不能为空')
      return (False, error_message)
        
    account.nickname = nick_name
    account.put()
    return (True, None)