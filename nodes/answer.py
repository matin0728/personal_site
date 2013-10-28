# coding=utf-8

import os
from google.appengine.ext import ndb
import model
import shared.znode as znode
import service
import datetime



# class ZNodeVote(ZNode):
#   template_ = 'vote.html'
#   client_type = 'ZH.ui.VoteBar'
#   # meta = {
#   #   'question_id',
#   #   'answer_id'
#   # }
  
#   # view_data = {
#   #   'answer',
#   #   'relation'
#   # }
  
#   def fetch_data_internal(self):
#     question = Question.get_by_id(int(self.get_meta('question_id')))
#     answer = Answer.get_by_id(parent = question.key, id = int(self.get_meta('answer_id')))
#     self.set_view_data_item('answer', answer)
    
#     relation = AccountQuestionRelationService().get_relationship(self.get_handler().get_current_account().key, question.key)
#     self.set_view_data_item('relation', relation)
    
#   def fetch_data(self):
#     #NOTE: Is it nessary to check all data exists? check one instead.
#     answer = self.get_view_data_item('answer')
#     if not answer:
#       self.fetch_data_internal()
      
# class ZNodeAnswerMeta(ZNode):
#   template_ = 'answer_meta.html'
#   client_type = 'ZH.ui.AnswerMeta'
    
#   # client_type = 'ZH.ui.AnswerMeta'
#   # template = 'answer_meta.html'
#   # meta = {
#   #   'question_id',
#   #   'answer_id'
#   # }

#   # view_data = {
#   #   'answer',
#   #   'relation'
#   # }

#   def fetch_data_internal(self):
#     # NOTE: We need update this component on action, we MUST IMP this method.
#     #get data from question_id, answer_id
#     question = Question.get_by_id(int(self.get_meta('question_id')))
#     answer = Answer.get_by_id(parent = question.key, id = int(self.get_meta('answer_id')))
#     self.set_view_data_item('answer', answer)
    
#     relation = AccountQuestionRelationService().get_relationship(self.get_handler().get_current_account().key, question.key)
#     self.set_view_data_item('relation', relation)
    

#   def fetch_data(self):
#     #NOTE: It's not nessary to check all data exists, check one instead.
#     answer = self.get_view_data_item('answer')
#     if not answer:
#       self.fetch_data_internal()
    
      

class Answer(znode.ZNode):
  # Default option.
  # meta_ = {
  #   'hide_answer_meta': 1 # Hide answer meta by default.
  # }
  def __init__(self, meta = {}, parent_node = None):
    super(Answer, self).__init__(meta = meta, parent_node = parent_node)
    self.template = 'answer.html'
    self.js_path = 'answer'
    if not 'hide_answer_meta' in meta.keys():
      meta['hide_answer_meta'] = 1

  # def set_comments_list(self, comments_list_node):
  #   self.add_child(comments_list_node)
  #   self.set_meta('comments_list_id', comments_list_node.get_client_id())
  #   self.set_view_data_item('opt_render_comments', comments_list_node.render())
  
  # meta = {
  #   'question_id',
  #   'answer_id'
  # }
  # view_data = {
  #   'answer': AnswerObject,
  #   'relation': accountxquestion
  # }
  def fetch_data_internal(self):
    question = model.Question.get_by_id(int(self.get_meta('question_id')))
    answer = model.Answer.get_by_id(parent = question.key, id = int(self.get_meta('answer_id')))
    self.set_view_data_item('answer', answer)
    
    # relation = AccountQuestionRelationService().get_relationship(self.get_handler().get_current_account().key, question.key)
    # self.set_view_data_item('relation', relation)
    
  def fetch_data(self):
    #NOTE: It's not nessary to check all data exists, check one instead.
    question = self.get_view_data_item('answer')
    if not question:
      self.fetch_data_internal()
      
    # self.set_view_data_item('render_vote', self.render_vote)
    # self.set_view_data_item('render_meta', self.render_meta)
      
  # def render_vote(self, answer, relation):
  #   v = ZNodeVote(self.current_handler)
  #   v.set_view_data_item('answer', answer)
  #   v.set_view_data_item('relation', relation)
  #   self.add_child(v)
  #   return v.render()
    
  # def render_meta(self, answer, relation):
  #   hide_meta = self.get_meta('hide_answer_meta')
  #   if hide_meta:
  #     return ''
    
  #   m = ZNodeAnswerMeta(self.current_handler)
  #   m.set_view_data_item('answer', answer)
  #   m.set_view_data_item('relation', relation)
  #   self.add_child(m)
  #   return m.render()
    
    
    
    
    
    
    
    
    
    
    
    
    
    