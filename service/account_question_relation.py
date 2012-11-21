# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
import model
from entity import EntityService
from singleton import Singleton
from base_service import BaseService

class AccountQuestionRelationService(Singleton, BaseService):
  def get_relationship(self, account_key, question_key):
    relationship = model.AccountXQuestion.query(ancestor=question_key).filter(model.AccountXQuestion.account == account_key).get()
    if not relationship:
      relationship = model.AccountXQuestion(
        parent = question_key, 
        account = account_key, 
        question = question_key)
    
    return relationship