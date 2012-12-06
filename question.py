# coding=utf-8

import webapp2
from google.appengine.api import users
from shared import *
from model.question import *
from model.answer import *
# from service.answer import answer as AnswerService
from service.answer import AnswerService
from service.question import QuestionService
from service.entity import EntityService
from module.question import *
from nodes import *

class QuestionHandler(BaseHandler):
  def get(self, question_id):      
    context = {
      'render_question_page': self.render_question_page(question_id)
    }
    
    self.render('question.html', context)
  
  def render_question_page(self, question_id = 0):
    meta = {
      'question_id': question_id
    }
    question_page = ZNodeQuestionPage(self, meta)
    question_page.set_root_node()
    return question_page.render()
    
  def pagelet(self, question_id):
    ref_element = self.request.get('ref_element')
    meta = {
      'question_id': question_id
    }
    question_page = ZNodeQuestionPage(self, meta)
    
    response = self.get_ajax_response();
    pagelet = Pagelet(question_page)
    
    pagelet.set_ref_element(ref_element)
    pagelet.set_render_position(PAGELET_RENDER_POSITION.BEFORE)
    pagelet.set_render_type(PAGELET_RENDER_TYPE.DECORATION)

    response.add_pagelet(pagelet)
    self.output_ajax_response(response)
    
class QuestionEditHandler(BaseHandler):
  def get(self, question_id):
    question = Question.get_by_id(int(question_id))
    context = {
      'form_label': u'编辑问题',
      'action_uri': self.uri_for('question.edit', question_id = question.key.id()),
      'current_question': question
    }
    self.render('question_add.html', context)
  
  def post(self, question_id):
    question = Question.get_by_id(int(question_id))
    if not question:
      return
    
    #TODO: Parse question object in helper method.
    title = self.request.get('title')
    #TODO: file desc content using hlper method.
    description = self.request.get('description').replace("\n", "<br />")
    if title:
      question.title = title
      question.description = description
      question.put()
      self.redirect(self.uri_for('question', question_id = question.key.id()))
      
class QuestionAddAnswerHandler(BaseHandler):
  def get(self):
    pass
    
  def post(self, question_id):
    source = self.request.get('source')
    answer_list_wrap = self.request.get('answer_list_wrap_id')
    
    answer = QuestionService().add_answer(question_id, source, self.get_current_account())
    
    meta = {
      'question_id': question_id,
      'answer_id': answer.key.id(),
      'hide_answer_meta': 0
    }
    
    # Update edit form pagelet.
    edit_form_id = self.request.get('edit_form_id')
    edit_form_disabled_info = ZNodeAnswerEditFormDisabledInfo(self)
    pagelet = Pagelet(edit_form_disabled_info)
    pagelet.set_ref_element(edit_form_id) \
      .set_render_position(PAGELET_RENDER_POSITION.BEFORE) 
      
    response = self.get_ajax_response()
    response.add_pagelet(pagelet)
    
    # New answer pagelet.
    answer_node = ZNodeAnswer(self, meta)
    pagelet = Pagelet(answer_node)
    pagelet.set_ref_element(answer_list_wrap) \
      .set_render_position(PAGELET_RENDER_POSITION.APPEND) 
    
    response = self.get_ajax_response()
    response.add_pagelet(pagelet)
    self.output_ajax_response(response)
    
    # if answer:
    #   self.redirect(self.uri_for('question', question_id = answer.question.id()))
    # else:
    #   error = QuestionService().get_last_error()
    #   self.set_error(error)

class QuestionDeleteHandler(BaseHandler):
  def get(self, question_id):
    #TODO: Should be a post action.
    QuestionService().delete_question(question_id)
    self.redirect(self.uri_for('home'))
    
  def post(self, question_id):
    pass
      
class QuestionAddHandler(BaseHandler):
  def get(self):
    q = Question()
    q.title = ''
    context = {
      'form_label': u'添加问题',
      'action_uri': self.uri_for('question.add'),
      'current_question': q
    }
    self.render('question_add.html', context)
    
  def post(self):
    title = self.request.get('title')
    if title:
      question = Question()
      question.title = title
      question.description = self.request.get('description').replace("\n", "<br />")
      question.creator = self.get_current_account().key
      question.put()
      self.redirect(self.uri_for('question', question_id = question.key.id()))
    else:
      self.redirect(self.uri_for('question.add'))
        
class QuestionFocusHandler(BaseHandler):
  def get(self, question_id):
    return self.post(question_id)
  
  def post(self, question_id):
    account = self.get_current_account().key
    QuestionService().focus_question(account, question_id)
    self.process_live_query()
    
class QuestionUnFocusHandler(BaseHandler):
  def get(self, question_id):
    return self.post(question_id)
  
  def post(self, question_id):
    account = self.get_current_account().key
    QuestionService().unfocus_question(account, question_id)
    self.process_live_query()
    

# app = webapp2.WSGIApplication([
#     # webapp2.Route(r'/', handler=HomeHandler, name='home'),
# 
#     webapp2.Route(r'/question/<question_id:\d+>', handler=QuestionHandler, name="question"),
#     webapp2.Route(r'/question/<question_id:\d+>/edit', handler=QuestionEditHandler, name="question.edit"),
#     webapp2.Route(r'/question/add', handler=AddQuestionHandler, name="question.add"),
# ], debug = SITE_CONFIG['is_debug'], config=SITE_CONFIG)





