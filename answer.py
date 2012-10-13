# coding=utf-8

import webapp2
from google.appengine.api import users
from shared import *
from model.answer import Answer
from model.question import Question
from service.question import QuestionService
from service.entity import EntityService

# from service import answer as AnswerService

# class AnswerHandler(BaseHandler):
#   def get(self, answer_id):
#     answer = Answer.get_by_id(int(answer_id))
#     context = {
#       'current_answer': answer,
#       'answers': AnswerService.get_answers_by_answer(answer.key)
#     }
#     
#     self.response.out.write(context['current_answer'])
#     self.response.out.write(context['answers'])
#     
#     self.render('answer.html', context)
    
class AnswerEditHandler(BaseHandler):
  def get(self, question_id, answer_id):
    current_question = Question.get_by_id(int(question_id))
    if not current_question:
      self.response.out.write('Not found question.')
      return
      
    answer = Answer.get_by_id(int(answer_id), parent = current_question.key)
    #TODO: raise 404 error.
    if not answer:
      self.response.out.write('Not found answer.')
      return

    answer_full = answer.get_extra()
    context = {
      'form_label': u'编辑问题',
      'action_uri': self.uri_for('answer.edit', question_id = answer.question.id(), answer_id = answer.key.id()),
      'current_answer': answer,
      'current_question': current_question
    }
    self.render('answer_edit.html', context)
  
  def post(self, question_id, answer_id):
    source = self.request.get('source')
    QuestionService().update_answer(question_id, answer_id, source)
    self.redirect(self.uri_for('question', question_id = question_id))
      
class AnswerDeleteHandler(BaseHandler):
  def get(self, question_id, answer_id):
    #TODO: Should be a post action.
    question = QuestionService().remove_answer_from_question(question_id, answer_id)
    if question:
      self.redirect(self.uri_for('question', question_id = question.key.id()))
    else:
      self.response.out.write('Answer to be deleted not found!')
      pass

  def post(self, question_id):
    pass      
      
      
      
      
      