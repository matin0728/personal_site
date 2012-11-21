# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from singleton import Singleton
from base_service import BaseService
import model

class FeedService(Singleton, BaseService):
  def get_feed(self, start = 0, limit = 7):
    feeds = []
    questions = model.Question.query().fetch(limit + 1, offset = start)
        
    index = 0
    for q in questions:
        if index < limit:
          a = model.Answer.query(ancestor = q.key).get(keys_only = True)
          answer_ids = []
          if a:
            answer_ids.append(a)
          f = {
              'feed_id':1,
              'last_updated':1348553241882,
              'action_type':'vote',
              'actors':[],
              'question':q.key,
              'answers':answer_ids
          }
          feeds.append(f)
          index = index + 1
      
    has_more = (len(questions) == limit + 1)
      
    return (feeds, has_more, limit)
      # {
      #   'feed_id':1,
      #   'last_updated':1348553241882,
      #   'action_type':'vote',
      #   'actor_ids':[],
      #   'question_id':1,
      #   'answer_ids':[10]
      # },
      # {
      #   'feed_id':2,
      #   'last_updated':1348553241882,
      #   'action_type':'focus',
      #   'actor_ids':[],
      #   'question_id':3,
      #   'answer_ids':[11]
      # },
      # {
      #   'feed_id':3,
      #   'last_updated':1348553241882,
      #   'action_type':'vote',
      #   'actor_ids':[],
      #   'question_id':4,
      #   'answer_ids':[12]
      # }

