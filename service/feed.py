# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

def get_feed(start):
  #feed_id, last_updated, action_type ,actor_ids, question_id, answer_ids
  return [
    {
      'feed_id':1,
      'last_updated':1348553241882,
      'action_type':'vote',
      'actor_ids':[],
      'question_id':1,
      'answer_ids':[10]
    },
    {
      'feed_id':2,
      'last_updated':1348553241882,
      'action_type':'focus',
      'actor_ids':[],
      'question_id':3,
      'answer_ids':[11]
    },
    {
      'feed_id':3,
      'last_updated':1348553241882,
      'action_type':'vote',
      'actor_ids':[],
      'question_id':4,
      'answer_ids':[12]
    }
  ]

