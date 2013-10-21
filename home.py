import webapp2
from google.appengine.api import users
from shared import *
import nodes
import model
import service
from vendor.znode import *
# from module.shared.feed import ZNodeFeedList

class HomeMyQuestionHandler(BaseHandler):
  def get(self):
    # context = {
    #   'question_list': question_list,
    #   'feed_list':feed_list.render()
    # }
    context = {
      'render_home_page': self.render_home_page()
    }
    
    self.render('home.html', context)
    
  def render_home_page(self):
    home_page = nodes.ZNodeHomeMyQuestion(self)
    home_page.set_root_node()
    return home_page.render()
    
  def pagelet(self):
    home_page = nodes.ZNodeHomeMyQuestion(self)
    self.pagelet_(home_page)

class HomeHandler(BaseHandler):
  def get(self):
    # context = {
    #   'question_list': question_list,
    #   'feed_list':feed_list.render()
    # }
    context = {
      'render_home_page': self.render_home_page()
    }
    
    self.render('home.html', context)
    
  def pagelet(self):
    home_page = nodes.ZNodeHomePageFeed(self)
    self.pagelet_(home_page)
    
  def render_home_page(self):
    # home_page = nodes.ZNodeHomePageFeed(self)
    # home_page.set_root_node()
    # return home_page.render()
    pass

    
  def load_more(self):
    start = int(self.request.get('start', 0))
    feed_list_wrap = self.request.get('feed_list_wrap')
    
    feed_data, has_more, limit = service.FeedService().get_feed(start = start)
    
    question_ids = []
    answer_ids = []
    for f in feed_data:
      question_ids.append(f['question'])
      for a in f['answers']:
        answer_ids.append(a)
    
    #pre fetch data:
    service.EntityService().get_multi(question_ids)
    service.EntityService().get_multi(answer_ids)
    
    response = self.get_ajax_response()
    for feed_item_data in feed_data:
      meta = {
        'feed_id': 'abc', # for demo, ignored.
        'question_id': feed_item_data['question'].id(),
        'answer_ids':'', # for demo, ignored.
      }
      feed_node = nodes.ZNodeFeedItem(self, meta = meta)
      feed_node.set_view_data_item('feed_data', feed_item_data)
      
      pagelet = Pagelet(feed_node)
      pagelet.set_ref_element(feed_list_wrap) \
        .set_render_position(PAGELET_RENDER_POSITION.APPEND) 

      response.add_pagelet(pagelet)
      
    #Check feed num, if load more is not availabel, disable the button.
    more_button_pagelet = response.get_pagelet_by_type('ZH.ui.MoreButton')
    
    if not has_more:
      more_button_pagelet.set_render_type(PAGELET_RENDER_TYPE.UN_RENDER)
    else:
      more_button_node = more_button_pagelet.get_node_instance()
      more_button_node.set_meta('request_url', self.uri_for('home', method_name = 'load_more', start = str(start + limit)))
      
    self.output_ajax_response(response)


class SignupHandler(BaseHandler):
  def get(self):
    account = model.Account()
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
    exists = model.Account.query(model.Account.user == current_user).get()
    if exists:
      self.redirect(self.uri_for('home'))  

    error_messages = {
      'nickname_error': 'Nickname can not be empty.',
      'nickname_duplicated': "This name has already been used."
    }

    account = model.Account()
    account.nickname = self.request.get('nickname')
    account.bio = self.request.get('bio')
    account.avator = self.request.get('avator')
    account.user = current_user

    #TODO: Shall we move the validate method to model class?
    messages = []
    if not account.nickname:
      messages.append(error_messages['nickname_error'])

    duplicated = model.Account.query(model.Account.nickname == account.nickname).get()
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
    
class TestHandler(BaseHandler):
  def get(self):
    test_name = self.request.get('test_name')
    if not test_name:
      test_name = 'test_index.html'

    self.render('tests/' + test_name)

class ModalUpdateHandler(BaseHandler):
  def get(self):
    self.render('test_pagelets.html')
    # questions = Question.query().fetch()
    #     for q in questions:
    #       answers = service.AnswerService().get_answers_by_question(q.key)
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
    pass
    
  def post(self):
    self.process_live_query()

# app = webapp2.WSGIApplication([
#     webapp2.Route(r'/', handler=HomeHandler, name='home'),
# 
#     # webapp2.Route(r'/question/<question_id:\d+>', handler=QuestionHandler, name="question"),
#     # webapp2.Route(r'/question/<question_id:\d+>/edit', handler=QuestionEditHandler, name="question.edit")
#     # webapp2.Route(r'/question/add', handler=AddQuestionHandler, name="question.add"),
# ], debug = SITE_CONFIG['is_debug'], config=SITE_CONFIG)
    
