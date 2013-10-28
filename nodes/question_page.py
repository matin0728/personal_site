# coding=utf-8

import os
from google.appengine.ext import ndb

import model
import service
import nodes

# from answer import *
# from topic_editor import *
# from answer_list_base import *
# from answer_edit_form import *

import vendor.znode as znode

class QuestionPage(znode.ZNode):
  # meta = {
  #   'question_id',
  # }
  
  # view_data = {
  #  'question' : None
  #  'relation' : None
  # }
  # 
  
  
  def __init__(self, meta = {}):
    self.template = 'question_page.html'
    self.js_path = 'question_page'
    #TODO: merge options.
    # meta['page_url'] = '/question/' + meta['question_id']
    super(QuestionPage, self).__init__(meta = meta)
  
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    question = model.Question.get_by_id(int(self.get_meta('question_id')))
    # relation = service.AccountQuestionRelationService().get_relationship(self.get_handler().get_current_account().key, question.key)
    
    self.set_view_data_item('question', question)
    # self.set_view_data_item('relation', relation)
    # self.set_view_data_item('render_topic_editor', self.render_topic_editor(question))
    self.set_view_data_item('render_answer_list', self.render_answer_list(question, relation))
    # self.set_view_data_item('render_answer_list_header', self.render_answer_list_header(question))
    self.set_view_data_item('render_answer_edit_form', self.render_answer_edit_form(question, relation))
    
  # def render_answer_list_header(self, question):
  #   meta = {
  #     'question_id': question.key.id()
  #   }
  #   answer_list_header = ZNodeAnswerListHeader(self.get_handler(), meta = meta)
  #   self.add_child(answer_list_header)
  #   answer_list_header.set_view_data_item('question', question)
  #   return answer_list_header.render()
  
  def render_answer_list(self, question, relation):
    meta = {
      'question_id': question.key.id()
    }
    answer_list = nodes.AnswerList(meta = meta, parent_node = self)
    self.add_child(answer_list)
    answer_list.set_view_data_item('question', question)
    answer_list.set_view_data_item('relation', relation)
    
    return answer_list.render()
    
  def render_answer_edit_form(self, question, relation):
    edit_form = nodes.AnswerEditForm(parent_node = self)
    return edit_form.render()

    # if not relation.my_answer:    
    #   edit_form = nodes.AnswerEditForm(parent_node = self)
    #   edit_form.set_view_data_item('question', question)
    #   edit_form.set_view_data_item('relation', relation)
      
    #   # self.answer_form_client_id = edit_form.get_client_id()
      
    #   self.add_child(edit_form)
    #   return edit_form.render()
    # else:
    #   disabled_info = ZNodeAnswerEditFormDisabledInfo(self.get_handler())
    #   self.add_child(disabled_info)
    #   return disabled_info.render()
      
  # def render_topic_editor(self, question):
  #   meta = {
  #     'question_id': question.key.id() 
  #   }
  #   editor = ZNodeTopicEditor(self.get_handler(), meta = meta)
  #   editor.set_view_data_item('question', question)
  #   self.add_child(editor)
  #   return editor.render()
    
  def render_question_head_block(self):
    #TODO.
    pass
    
  