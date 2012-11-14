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
  def __init__(self, *args, **kwargs):
    super(QuestionHandler, self).__init__(*args, **kwargs)
    self.answer_form_client_id = ''
    
  def get(self, question_id):      
    question = Question.get_by_id(int(question_id))
    relation = QuestionService().get_question_relationship(self.get_current_account().key, question.key)
    
    view_data = {
      'question': question,
      'relation': relation,
      'render_answer_list': self.render_answer_list(question, relation),
      'render_answer_edit_form': self.render_answer_edit_form(question, relation)
    }
    
    # TEST
    # Add a extra live node append to specified element.
    demo_node = DemoNode(self)
    extra_pagelet = Pagelet(demo_node)
    extra_pagelet.set_ref_element(self.answer_form_client_id)
    # This is default option, we can dismiss them.
    # extra_pagelet.set_render_type(PAGELET_RENDER_TYPE.DECORATION)
    # extra_pagelet.set_render_position(PAGELET_RENDER_POSITION.BEFORE)
    
    ajax_response = self.get_ajax_response()
    ajax_response.add_pagelet(extra_pagelet)

    self.render('question.html', view_data)
    
  def render_answer_list(self, question, relation):
    meta = {
      'question_id': question.key.id()
    }
    answer_list = ZNodeAnswerList(self, meta = meta)
    answer_list.set_view_data_item('question', question)
    answer_list.set_view_data_item('relation', relation)
    
    answer_list.set_root_node()
    
    return answer_list.render()
    
  def render_answer_edit_form(self, question, relation):
    if not relation.my_answer:    
      edit_form = ZNodeAnswerEditForm(self)
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
    answer = QuestionService().add_answer(question_id, source, self.get_current_account())
    if answer:
      self.redirect(self.uri_for('question', question_id = answer.question.id()))
    else:
      error = QuestionService().get_last_error()
      self.set_error(error)

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





