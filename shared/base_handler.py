import webapp2
import jinja2
import os
from google.appengine.api import users
from model.account import Account
from service.entity import EntityService
from pagelet_processor import *
from app_config import *

class BaseHandler(webapp2.RequestHandler):
  def __init__(self,application, request, **kwargs):  
    super(BaseHandler, self).__init__(application, request, **kwargs)
    self.pagelet_processor_ = None
    self.parents_map_ = None
    self.current_account = None
    
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
      
    # return webapp2.RequestHandler.dispatch(self)
    """Dispatches the request.

    This will first check if there's a 'method_name' param, if present, 
    call the method related.
    """
    request = self.request
    method_name = request.get('method_name')
    
    if not method_name:
      return super(BaseHandler, self).dispatch()

    method = getattr(self, method_name, None)
    if method:
      args, kwargs = request.route_args, request.route_kwargs
      if kwargs:
          args = ()
          
      try:
          return method(*args, **kwargs)
      except Exception, e:
          return self.handle_exception(e, self.app.debug)
          
    else:
      valid = 'Methos not exists.'
      self.abort(405, headers=[('Allow', valid)])
    
  # @webapp2.cached_property
  def get_template_environment(self):
    jinja_environment = jinja2.Environment(
      loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__) + '/../templates')))
    return jinja_environment
    
  def process_live_query(self):
    response = self.get_ajax_response()
    # For test only:
    # response.set_message("Hello world!")
    # response.set_redirect('baidu.com')
    # response.set_refresh(False)
    # p = Pagelet('test_type', instance_identity = 'abc', markup = 'kkkk')
    #  p.set_instance_identity('new_identity')
    #  p.set_render_type('some_type')
    #  p.set_render_position('positon')
    #  p.set_construct_arg_string('aaa')
    #  p.set_ref_element('some ele')
    #  p.add_event('some event', 'some args')
    #  response.add_pagelet(p)
    #  pp = response.get_pagelet_by_type('test_type')
    #  pp.set_instance_identity('qqqqq')
    
    self.output_ajax_response(response)
  
  def get_parents_map(self):
    if not self.parents_map_:
      self.parents_map_ = ParentsMap()
      
    return self.parents_map_
    
  def get_ajax_response(self):
    if not self.pagelet_processor_:
      queries = self.request.get('live_components')
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
    # TODO: Add user role info for authentication purpose.
    extra_context = {
      'request': self.request,
      'uri_for': self.uri_for,
      'config': SITE_CONFIG,
      'parents_map': self.get_parents_map().get_json(),
      'root_nodes': self.get_parents_map().get_root_nodes_json()
    }
    #'get': EntityService().get #Shorthand for get entity, NOTE: 2012-11-01, disable this feature,
    # don't get entity on template.

    for key, value in extra_context.items():
      if key not in context:
        context[key] = value
    
    env = self.get_template_environment()
    template = env.get_template(template)
    self.response.out.write(template.render(context))
    
  

    # method_name = request.route.handler_method
    # if not method_name:
    #     method_name = _normalize_handler_method(request.method)
    # 
    # method = getattr(self, method_name, None)
    # if method is None:
    #     # 405 Method Not Allowed.
    #     # The response MUST include an Allow header containing a
    #     # list of valid methods for the requested resource.
    #     # http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.6
    #     valid = ', '.join(_get_handler_methods(self))
    #     self.abort(405, headers=[('Allow', valid)])
    # 
    # # The handler only receives *args if no named variables are set.
    # args, kwargs = request.route_args, request.route_kwargs
    # if kwargs:
    #     args = ()
    # 
    # try:
    #     return method(*args, **kwargs)
    # except Exception, e:
    #     return self.handle_exception(e, self.app.debug)
    