import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
from shared.znode import ZNode
import service

from shared.znode import *

# TODO: This is some piece of un-complete code.

# class ZNodeQuestionListBase(ZNode):
#   #NOTE: Why we call this "ListBase"? This collapsed answerlist is another type of answer list
#   # and it will only need to override the fetch data method and has another client name.
#   
#   # meta should contains following data.
#   # meta = {
#   #   'question_id',
#   # }
#   
#   # view_data should contains(at least) following field.
#   # view_data = {
#   #  'answers' : []
#   #  'relation' : None
#   #  'question': None, question entity.
#   # }
#   # 
#   template_ = 'question_list.html'
#   client_type = 'ZH.ui.QuestionList'
#   
#   def render_question(self, question_key, relation):
#     meta = {
#       'question_id': question_key.id(),
#       'account_id': 0
#     }
#     a = ZNodeQuestion(self.get_handler(), meta = meta)
#     a.set_view_data_item('question', service.EntityService().get(question_key))
#     a.set_view_data_item('relation', relation)
#     self.add_child(a)
#     return a.render()
#   
#   def fetch_data_internal(self):
#     pass
#     
#   def fetch_data(self):
#     questions = self.get_view_data_item('questions')
#     if not questions:
#       self.fetch_data_internal()
#      
#     question_ids = self.get_view_data_item('questions')
#     # Batch fetch entity
#     service.EntityService().get_multi(question_ids)
#     self.set_view_data_item('render_question', self.render_question)
#     
# class ZNodeQuestionListOfMember(ZNodeQuestionListBase):
#   # meta = {
#   #   'account_id',
#   # }
#   def fetch_data_internal(self):
#     questions = models.Question.get_by_id(question.key, keys_only = True)
#     self.set_view_data_item('questions', questions)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
