# coding=utf-8

import webapp2
from google.appengine.api import users
from shared import *
from model.answer import *
from service import question as QuestionService

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
  def get(self, answer_id):
    answer = Answer.get_by_id(int(answer_id))
    answer.content = answer.content.replace("<br />", "\n")
    context = {
      'form_label': u'编辑问题',
      'action_uri': self.uri_for('answer.edit', answer_id = answer.key.id()),
      'current_answer': answer,
      'current_question': Question.get_by_id(answer.question.id())
    }
    self.render('answer_edit.html', context)
  
  def post(self, answer_id):
    answer = Answer.get_by_id(int(answer_id))
    
    if not answer:
      #TODO: redirect to 404.
      pass
      
    #TODO: filter desc content using hlper method.
    content = self.request.get('content').replace("\n", "<br />")
    if content:
      answer.content = content
      answer.put()
      question = Question.get_by_id(answer.question.id())
      self.redirect(self.uri_for('question', question_id = question.key.id()))
      
class AnswerDeleteHandler(BaseHandler):
  def get(self, answer_id):
    #TODO: Should be a post action.
    answer = Answer.get_by_id(int(answer_id))
    if not answer:
      #TODO: redirect 404.
      return

    answer.key.delete()
    question = Question.get_by_id(answer.question.id())
    
    QuestionService.update_answer_num(question.key)
    
    self.redirect(self.uri_for('question', question_id = question.key.id()))

  def post(self, question_id):
    pass      
      
      
      
      
      