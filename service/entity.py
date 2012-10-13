# coding=utf-8
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from model import *
from singleton import Singleton
# import answer as AnswerService

class EntityService(Singleton):
  entity_map = {}
    
  def get(self, key):
    cache_key = key.urlsafe()
    if cache_key in self.entity_map.keys():
      return self.entity_map[cache_key]
    else:
      entity = key.get()
      if entity:
        self.entity_map[cache_key] = entity
        return entity

  #this is for pre-fetch.
  def get_multi(self, entity_keys):
    entities = ndb.get_multi(entity_keys)
    for entity in entities:
      if entity:
        self.entity_map[entity.key.urlsafe()] = entity



