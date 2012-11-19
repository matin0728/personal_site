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
from answer_list_base import *
from answer_edit_form import *

from shared.znode import *

class ZNodeQuestionPage(ZNode):
  # meta = {
  #   'question_id',
  # }
  
  # view_data = {
  #  'question' : None
  #  'relation' : None
  # }
  # 
  template_ = 'question_page.html'
  client_type = 'ZH.page.QuestionPage'
  
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    question = Question.get_by_id(int(self.get_meta('question_id')))
    relation = QuestionService().get_question_relationship(self.get_handler().get_current_account().key, question.key)
    
    self.set_view_data_item('question', question)
    self.set_view_data_item('relation', relation)
    self.set_view_data_item('render_answer_list', self.render_answer_list(question, relation))
    self.set_view_data_item('render_answer_edit_form', self.render_answer_edit_form(question, relation))

  
  def render_answer_list(self, question, relation):
    meta = {
      'question_id': question.key.id()
    }
    answer_list = ZNodeAnswerList(self.get_handler(), meta = meta)
    answer_list.set_view_data_item('question', question)
    answer_list.set_view_data_item('relation', relation)
    
    return answer_list.render()
    
  def render_answer_edit_form(self, question, relation):
    if not relation.my_answer:    
      edit_form = ZNodeAnswerEditForm(self.get_handler())
      edit_form.set_view_data_item('question', question)
      edit_form.set_view_data_item('relation', relation)
      
      self.answer_form_client_id = edit_form.get_client_id()
      
      edit_form.set_root_node()
      return edit_form.render()
    else:
      return 'You has answered this question.'
    
  def render_question_head_block(self):
    #TODO.
    pass
    
  