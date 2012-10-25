# coding=utf-8

import webapp2
from google.appengine.api import users
from shared import *
from model.answer import Answer
from model.question import Question
from service.question import QuestionService
from service.answer import AnswerService
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

  def post(self, question_id, answer_id):
    pass      
      
class AnswerThanksHandler(BaseHandler):
  def post(self, question_id, answer_id):
    AnswerService().thanks_for_answer(self.get_current_account(), question_id, answer_id)
    # TODO: Create response pagelet.

  def get(self, question_id, answer_id):
    self.post(question_id, answer_id)      
  
class AnswerNoHelpHandler(BaseHandler):
  def post(self, question_id, answer_id):
    AnswerService().set_no_help(self.get_current_account(), question_id, answer_id)
    # TODO: Create response pagelet.

  def get(self, question_id, answer_id):
    self.post(question_id, answer_id)
        
        
class AnswerCancelNoHelpHandler(BaseHandler):
  def post(self, question_id, answer_id):
    AnswerService().cancel_no_help(self.get_current_account(), question_id, answer_id)
    # TODO: Create response pagelet.

  def get(self, question_id, answer_id):
    self.post(question_id, answer_id)  
    
class AnswerVoteUpHandler(BaseHandler):
  def post(self, question_id, answer_id):
    AnswerService().voteup_answer(self.get_current_account(), question_id, answer_id)
    # TODO: Create response pagelet.

  def get(self, question_id, answer_id):
    self.post(question_id, answer_id)    
      
class AnswerVoteDownHandler(BaseHandler):
  def post(self, question_id, answer_id):
    AnswerService().votedown_answer(self.get_current_account(), question_id, answer_id)
    # TODO: Create response pagelet.

  def get(self, question_id, answer_id):
    self.post(question_id, answer_id)

class AnswerCommentDeleteHandler(BaseHandler):
  def post(self, question_id, answer_id, comment_id):
    pass
  
  def get(self, question_id, answer_id, comment_id):
    self.post(question_id, answer_id, comment_id)
    
class AnswerAddCommentHandler(BaseHandler):
  def get(self, question_id, answer_id):
    content = self.request.get('content')
    if not content:
      #TODO: Handle error report.
      return
      
      
    pass

class AnswerCommentListHandler(BaseHandler):
  def get(self, question_id, answer_id):
    pass
    
class AnswerCommentDeleteHandler(BaseHandler):
  def post(self, question_id, answer_id, comment_id):
    pass

  def get(self, question_id, answer_id, comment_id):
    self.post(question_id, answer_id, comment_id)


