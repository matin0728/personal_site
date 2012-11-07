import webapp2
from google.appengine.api import users
from shared import *
from model.question import Question
from model.account import Account
from service.answer import AnswerService
from service.entity import EntityService
from module.shared.feed import ZNodeFeedList

class HomeHandler(BaseHandler):
  def get(self):
    question_list = Question.query().fetch()
    feed_list = ZNodeFeedList(self)
    feed_list.set_root_node()
    context = {
      'question_list': question_list,
      'feed_list':feed_list.render()
    }
    self.render('home.html', context)


class SignupHandler(BaseHandler):
  def get(self):
    account = Account()
    account.nickname = ''
    account.user = users.get_current_user()
    context = {
      'error_count':0,
      'messages':[],
      'account': account
    }
      
    #NOTE: Is there any uri builder utils in Python?
    #self.response.out.write(account.user)
    self.render('signup.html', context)
  
  def post(self):
    current_user = users.get_current_user()
    exists = Account.query(Account.user == current_user).get()
    if exists:
      self.redirect(self.uri_for('home'))  
    
    error_messages = {
      'nickname_error': 'Nickname can not be empty.',
      'nickname_duplicated': "This name has already been used."
    }
    
    account = Account()
    account.nickname = self.request.get('nickname')
    account.bio = self.request.get('bio')
    account.avator = self.request.get('avator')
    account.user = current_user
    
    #TODO: Shall we move the validate method to model class?
    messages = []
    if not account.nickname:
      messages.append(error_messages['nickname_error'])
    
    duplicated = Account.query(Account.nickname == account.nickname).get()
    if duplicated:
      messages.append(error_messages['nickname_duplicated'])
    
    error_count = len(messages)
    if error_count:
      context = {
        'messages':messages,
        'account': account,
        'error_count':error_count
      }
      self.render('signup.html', context)
      return
      
    account.put()
    self.redirect(self.uri_for('home'))

class ModalUpdateHandler(BaseHandler):
  def get(self):
    self.render('test_pagelets.html')
    # questions = Question.query().fetch()
    #     for q in questions:
    #       answers = AnswerService().get_answers_by_question(q.key)
    #       q.answers_num = len(answers)
    #       q.put()
    #       for a in answers:
    #         a.author = users.get_current_user()
    #         a.put()
    #       
    #     self.response.out.write("Update complete!")
    
  def post(self):
    self.process_live_query()
    
  def pagelet(self):
    self.response.out.write("You call pagelet method!")

#NOTE: response for ObjectLoader interface.
class NodeHandler(BaseHandler):
  def get(self):
    node_type = self.request.get('node_name')
    # TODO:
    # response = self.get_ajax_response()
    # pagelet = Pagelet()
    # response.add_pagelet() LiveQueryProcessor().
    pass

# app = webapp2.WSGIApplication([
#     webapp2.Route(r'/', handler=HomeHandler, name='home'),
# 
#     # webapp2.Route(r'/question/<question_id:\d+>', handler=QuestionHandler, name="question"),
#     # webapp2.Route(r'/question/<question_id:\d+>/edit', handler=QuestionEditHandler, name="question.edit")
#     # webapp2.Route(r'/question/add', handler=AddQuestionHandler, name="question.add"),
# ], debug = SITE_CONFIG['is_debug'], config=SITE_CONFIG)