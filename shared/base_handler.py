import webapp2
import jinja2
import os
from google.appengine.api import users
from model.account import Account
from service.entity import EntityService
from pagelet_processor import *

class BaseHandler(webapp2.RequestHandler):
  pagelet_processor_ = None
  current_account = None
  def get_current_account(self):
    return self.current_account
    
  def dispatch(self):
    user = users.get_current_user()
    account = Account.query(Account.user == user).get()
    if not account and self.request.route.name != 'signup':
      self.redirect(self.uri_for('signup'))
      return
    
    if account:  
      self.current_account =  account 
      
    return webapp2.RequestHandler.dispatch(self)
  # @webapp2.cached_property
  def get_template_environment(self):
    jinja_environment = jinja2.Environment(
      loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__) + '/../templates')))
    return jinja_environment
    
  def process_live_query(self):
    response = self.get_ajax_response()
    # For test only:
    # response.set_message("Hello world!")
    self.output_ajax_response(response)
    
  def get_ajax_response(self):
    if not self.pagelet_processor_:
      queries = self.request.get('live_components')
      #self.response.out.write(queries)
      #return
      self.pagelet_processor_ = LiveQueryProcessor(queries)
      
    return self.pagelet_processor_.get_response(self)
    
  def output_ajax_response(self, response):
    #strs = [ p.get_json_string() for p in pagelets]
    self.response.out.write(response.get_json())
        
  def set_error(self, error):
    #TODO: Complete this method
    # in_ajax = 'inajax' in self.request.headers.keys()
    # if in_ajax:
    #   pass
      
    self.response.out.write('{"r":1, "msg":"Server error."}')
    
  def render(self, template, context=None):
    context = context or {}
    extra_context = {
      'request': self.request,
      'uri_for': self.uri_for,
      'get': EntityService().get #Shorthand for get entity.
    }

    for key, value in extra_context.items():
      if key not in context:
        context[key] = value
    
    env = self.get_template_environment()
    template = env.get_template(template)
    self.response.out.write(template.render(context))
    