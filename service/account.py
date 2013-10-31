# coding=utf-8

#TODO: Move account creation logic here.

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from model import *
from singleton import Singleton
from base_service import BaseService
from model.account import Account


class AccountService(Singleton, BaseService):
  def __init__(self):
    super(AccountService, self).__init__()
    self.current_account = None

  def update_nick_name(self, nick_name, account):
    error_message = []
    if not nick_name:
      error_message.append(u'昵称不能为空')
      return (False, error_message)
        
    account.nickname = nick_name
    account.put()
    return (True, None)

  def get_logged_user_account(self):
    if self.current_account:
      return self.current_account

    user = users.get_current_user()
    if not user:
      return

    account = Account.query(Account.user == user).get()
    
    if account:  
      self.current_account =  account

    return account





    

