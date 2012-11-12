import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from model.question import *
from model.answer import *
from shared.znode import ZNode
from service import *

class ZNodeVote(ZNode):
  template_ = 'vote.html'
  client_type = 'ZH.ui.VoteBar'
    
  # client_type = 'ZH.ui.VoteBar'
  # template = 'vote.html'
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
  template_ = 'answer_meta.html'
  client_type = 'ZH.ui.AnswerMeta'
    
  # client_type = 'ZH.ui.AnswerMeta'
  # template = 'answer_meta.html'
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
    if not answer:
      self.fetch_data_internal()

class ZNodeAnswer(ZNode):
  client_type = 'ZH.ui.Answer'
  template_ = 'answer.html'
  
  # Default option.
  # meta_ = {
  #   'hide_answer_meta': 1 # Hide answer meta by default.
  # }
  
  def __init__(self, current_handler, meta = {}):
    #TODO: merge options.
    if not 'hide_answer_meta' in meta.keys():
      meta['hide_answer_meta'] = 1
      
    super(ZNodeAnswer, self).__init__(current_handler, meta = meta)
  # meta = {
  #   'question_id',
  #   'answer_id'
  # }
  # view_data = {
  #   'answer': AnswerObject,
  #   'relation': accountxquestion
  # }
  def fetch_data_internal(self):
    #get feed data from question_id, answer_id
    # We don't IMP this, case if we don't use this component seperately, it's not
    # nessary IMP this.
    pass
    
  def fetch_data(self):
    #NOTE: It's not nessary to check all data exists, check one instead.
    question = self.get_view_data_item('answer')
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
    hide_meta = self.get_meta('hide_answer_meta')
    if hide_meta:
      return ''
    
    m = ZNodeAnswerMeta(self.current_handler)
    m.set_view_data_item('answer', answer)
    m.set_view_data_item('relation', relation)
    self.add_child(m)
    return m.render()
    
    
    
    
    
    
    
    
    
    
    
    
    
    