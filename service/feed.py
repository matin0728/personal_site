# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from singleton import Singleton
from base_service import BaseService
from model.question import Question
from model.answer import Answer

class FeedService(Singleton, BaseService):
  def get_feed(self, start):
    feeds = []
    questions = Question.query().fetch(20)
        
    for q in questions:
      a = Answer.query(ancestor = q.key).get(keys_only = True)
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
      
    return feeds
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

