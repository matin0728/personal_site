import webapp2
import jinja2
import os
from google.appengine.api import users
from model.account import Account
from service.entity import EntityService

class BaseHandler(webapp2.RequestHandler):
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
    