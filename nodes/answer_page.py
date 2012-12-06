import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import service
from answer import *
from comment_list import *

from shared.znode import *

class ZNodeAnswerPage(ZNode):
  # meta = {
  #   'question_id',
  #   'answer_id'
  # }
  
  # view_data = {
  #  'question' : None
  #  'answer' : None
  # }
  # 
  template_ = 'answer_page.html'
  client_type = 'ZH.page.AnswerPage'
  
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    show_comments = self.get_handler().request.get('show_comments')
    
    question = model.Question.get_by_id(int(self.get_meta('question_id')))
    answer = model.Answer.get_by_id(parent = question.key, id = int(self.get_meta('answer_id')))
    relation = service.AccountQuestionRelationService().get_relationship(self.get_handler().get_current_account().key, question.key)
    
    #Inite answer node.
    meta = {
      'answer_id': answer.key.id(),
      'hide_answer_meta': 0
    }
    answer_node = ZNodeAnswer(self.get_handler(), meta = meta)
    answer_node.set_view_data_item('answer', answer)
    answer_node.set_view_data_item('relation', relation)
    self.add_child(answer_node)
      
    self.set_view_data_item('question', question)
    self.set_view_data_item('answer', answer)
    self.set_view_data_item('relation', relation)
    
    if show_comments:
      comments_meta = {
        'entity_key_string': answer.key.urlsafe()
      }
      comments_node = ZNodeCommentList(self.get_handler(), meta = comments_meta)
      answer_node.set_comments_list(comments_node)
      
    self.set_view_data_item('render_answer', answer_node.render())
    
    
    
    
    
    