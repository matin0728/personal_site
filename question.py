# coding=utf-8

import webapp2
from google.appengine.api import users
from shared import *
from model.question import *
from model.answer import *
# from service.answer import answer as AnswerService
from service import answer as AnswerService
from service import question as QuestionService

class QuestionHandler(BaseHandler):
  def get(self, question_id):
    question = Question.get_by_id(int(question_id))
    answers = AnswerService.get_answers_by_question(question.key)
    
    can_create_answer = True
    me = users.get_current_user()
    for a in answers:
      if a.author == me:
        can_create_answer = False
    
    context = {
      'current_question': question,
      'answers': answers,
      'can_create_answer': can_create_answer
    }
    
    # self.response.out.write(users.get_current_user())
    self.render('question.html', context)
    
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
    question = Question.get_by_id(int(question_id))
    content = self.request.get('content').replace("\n", "<br />")
    if question and content:
      new_answer = Answer()
      new_answer.content = content
      new_answer.question = question.key
      new_answer.author = users.get_current_user()
      new_answer.put()
      QuestionService.update_answer_num(question.key)

    
    self.redirect(self.uri_for('question', question_id = question.key.id()))
    

class QuestionDeleteHandler(BaseHandler):
  def get(self, question_id):
    #TODO: Should be a post action.
    question = Question.get_by_id(int(question_id))
    if not question:
      return
      
    question.key.delete()
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
      question.put()
      self.redirect(self.uri_for('question', question_id = question.key.id()))
    else:
      self.redirect(self.uri_for('question.add'))
        


# app = webapp2.WSGIApplication([
#     # webapp2.Route(r'/', handler=HomeHandler, name='home'),
# 
#     webapp2.Route(r'/question/<question_id:\d+>', handler=QuestionHandler, name="question"),
#     webapp2.Route(r'/question/<question_id:\d+>/edit', handler=QuestionEditHandler, name="question.edit"),
#     webapp2.Route(r'/question/add', handler=AddQuestionHandler, name="question.add"),
# ], debug = SITE_CONFIG['is_debug'], config=SITE_CONFIG)





