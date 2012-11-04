import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from model.question import *
from model.answer import *
from shared.znode import ZNode
from service import *

class ZNodeVote(ZNode):
  client_type = 'Vote'
  template = 'vote.html'
  # meta = {
  #   'question_id',
  #   'answer_id'
  # }
  
  # view_data = {
  #   'answer',
  #   'relation'
  # }
  
  def fetch_data_internal(self):
    # NOTE: It's not likely to use this compoent standalone, ignore this IMP
    #get data from question_id, answer_id
    pass
    
  def fetch_data(self):
    #NOTE: It's not nessary to check all data exists, check one instead.
    answer = self.get_view_data_item('answer')
    if not question:
      self.fetch_data_internal()
      
class ZNodeAnswerMeta(ZNode):
  client_type = 'AnswerMeta'
  template = 'answer_meta.html'
  # meta = {
  #   'question_id',
  #   'answer_id'
  # }

  # view_data = {
  #   'answer',
  #   'relation'
  # }

  def fetch_data_internal(self):
    # NOTE: It's not likely to use this compoent standalone, ignore this IMP
    #get data from question_id, answer_id
    pass

  def fetch_data(self):
    #NOTE: It's not nessary to check all data exists, check one instead.
    answer = self.get_view_data_item('answer')
    if not question:
      self.fetch_data_internal()

class ZNodeAnswer(ZNode):
  template = 'answer.html'
  # meta = {
  #   'question_id',
  #   'answer_id'
  # }
  def fetch_data_internal(self):
    #get feed data from question_id, answer_id
    pass
    
  def fetch_data(self):
    #NOTE: It's not nessary to check all data exists, check one instead.
    question = self.get_view_data_item('question')
    if not question:
      self.fetch_data_internal()
      
    self.set_view_data_item('render_vote', self.render_vote)
    self.set_view_data_item('render_meta', self.render_meta)
      
  def render_vote(self, answer, relation):
    v = ZNodeVote(self.current_handler)
    v.set_view_data_item('answer', answer)
    v.set_view_data_item('relation', relation)
    self.add_child(v)
    return v.render()
    
  def render_meta(self, answer, relation):
    m = ZNodeAnswerMeta(self.current_handler)
    m.set_view_data_item('answer', answer)
    m.set_view_data_item('relation', relation)
    self.add_child(m)
    return m.render()
    
    
    
    
    
    
    
    
    
    
    
    
    
    