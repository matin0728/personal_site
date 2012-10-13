import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from model.question import *
from model.answer import *
from shared.znode import ZNode
from service.feed import FeedService
from service.entity import EntityService

class ZNodeFeedItem(ZNode):
  template = 'feed_item.html'
  def fetch_data_internal(self):
    #get data from feed ID
    pass
    
    
  def fetch_data(self):
    if not self.view_data:
      self.fetch_data_internal()
      
    action_type = {'vote': " vote up the answer", 'focus': " focus the question"}
    #NOTE: Add extra data just for text only.
    self.set_view_data_item('actors', [])
    self.set_view_data_item('info', action_type[self.view_data['action_type']])

class ZNodeFeedList(ZNode):
  template = 'feed_list.html'
  def fetch_data(self):
    # print FeedService
    feed_data = FeedService().get_feed(self.get_meta('start'))
    self.set_view_data_item('feeds', feed_data)
    self.set_view_data_item('render_feed_item', self.render_feed_item)
    
    #NOTE: We should IMP a collection class to provide data batch fetching mechanism, 
    #'Feed like' list can reuse this class for data initialization.
    
    question_ids = []
    answer_ids = []      
    # Each feed should contains:
    #feed_id, last_updated, action_type ,actor_ids, question_id, answer_ids
    # for f in feed_data:
    #   question_ids.append(ndb.Key(Question, f['question_id']))
    #   for a in f['answer_ids']:
    #     answer_ids.append(ndb.Key(Answer, a))
    
    #NOTE: For demostration and simplycify, we provide key for feed property.
    for f in feed_data:
      question_ids.append(f['question_id'])
      for a in f['answer_ids']:
        answer_ids.append(a)
    
    #pre fetch data:
    EntityService().get_multi(question_ids)
    #NOTE: Multi get is apply for entity with different parent?
    EntityService().get_multi(answer_ids)

  def render_feed_item(self, feed_item_data):
    
    #NOTE: Each feed should has a ID.
    # here should be feed = ZNodeFeedItem(feed_id)
    f = ZNodeFeedItem(self.current_handler)
    f.set_view_data(feed_item_data)
    #return 'feed item<br />' + str(feed_item_data)
    return f.render()
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    