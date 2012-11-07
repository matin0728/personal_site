import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from model.question import *
from model.answer import *
from shared.znode import ZNode
from service.feed import FeedService
from service.entity import EntityService
from service.question import QuestionService
from answer import *

class ZNodeFeedItem(ZNode):
  # meta should contains following data.
  # meta = {
  #   'feed_id',
  #   'question_id',
  #   'answer_ids'
  #   'answer_num'
  # }
  
  # view_data should contains(at least) following field.
  # view_data = {
  #  'question' : None
  #  'answers' : []
  #  'relation' : None
  #  'actors' : []
  #  'action_type' : 'vote'
  # }
  # 
  template = 'feed_item.html'
  client_type = 'ZH.ui.FeedItem'
  def fetch_data_internal(self):
    #get feed data from feed ID
    #self.feed_data = FeedService().get_by_id(self.get_meta('feed_id'))
    pass
  
  def render_answer(self, answer, relation):
    meta = {
      # NOTE: we needn't to set the question_id, case it is set on it's parent or ancestor.
      # 'question_id':self.get_meta('question_id'),
      'answer_id': answer.key.id()
    }
    a = ZNodeAnswer(self.current_handler, meta = meta)
    a.set_view_data_item('answer', answer)
    a.set_view_data_item('relation', relation)
    self.add_child(a)
    return a.render()
  
    
  def fetch_data(self):
    feed_data = self.get_view_data_item('feed_data')
    if not feed_data:
      self.fetch_data_internal()
      feed_data = self.get_view_data_item('feed_data')

    action_type = {'vote': " vote up the answer", 'focus': " focus the question"}
    #NOTE: Add extra data just for test only.
    
    feed_data['relation'] = QuestionService().get_question_relationship(self.current_handler.get_current_account().key, feed_data['question'])
    feed_data['question'] = EntityService().get(feed_data['question'])
    feed_data['answers'] = [EntityService().get(a) for a in feed_data['answers']]
    feed_data['actors'] = []
    feed_data['info'] = action_type[feed_data['action_type']]
    feed_data['render_answer'] = self.render_answer

    self.set_view_data(feed_data)
    
    # self.set_view_data_item('question', EntityService().get(question))
    # self.set_view_data_item('answers', [EntityService().get(a) for a in answers])
    # self.set_view_data_item('relation', QuestionService().get_question_relationship(self.current_handler.get_current_account().key, question))
    # self.set_view_data_item('actors', [])
    # self.set_view_data_item('info', action_type[self.view_data['action_type']])

class ZNodeFeedList(ZNode):
  client_type = 'ZH.ui.FeedList'
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
      question_ids.append(f['question'])
      for a in f['answers']:
        answer_ids.append(a)
    
    #pre fetch data:
    EntityService().get_multi(question_ids)
    #NOTE: Multi get is apply for entity with different parent?
    EntityService().get_multi(answer_ids)
    
    # self.current_handler.response.out.write(feed_data)
    # for f in feed_data:
    #   self.render_feed_item(f)

  def render_feed_item(self, feed_item_data):
    #NOTE: Each feed should has a ID.
    meta = {
      'feed_id': 'abc',
      'question_id': feed_item_data['question'].id(),
      'answer_ids':'', # for demo, ignored.
      'answer_num': len(feed_item_data['answers']) #pass this for caculate live feed replacement.
    }
    f = ZNodeFeedItem(self.current_handler, meta = meta)
    self.add_child(f)
    f.set_view_data_item('feed_data', feed_item_data)
    return f.render()
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    