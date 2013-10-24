import webapp2
import jinja2
import os
from google.appengine.api import users
from model.account import Account
from service.entity import EntityService
from pagelet_processor import *
from app_config import *
from nodes import *
from vendor.znode import zh_client_info_map

class BaseHandler(webapp2.RequestHandler):
  infor_map = None
  def __init__(self,application, request, **kwargs):  
    super(BaseHandler, self).__init__(application, request, **kwargs)
    self.ajax_response_ = None
    self.parents_map_ = None
    self.current_account = None
    
  def get_current_account(self):
    return self.current_account

  def get_client_infor_map(self):
    if not self.infor_map: 
      self.infor_map = zh_client_info_map.ClientInfoMap()

    return self.infor_map
    
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
    self.output_ajax_response(response)
  
  def get_parents_map(self):
    if not self.parents_map_:
      self.parents_map_ = ParentsMap()
      
    return self.parents_map_
    
  def get_ajax_response(self):
    if not self.ajax_response_:
      queries = self.request.get('live_components')
      processor = LiveQueryProcessor(queries)
      response_ = processor.get_response(self)
      self.ajax_response_ = response_
      
    return self.ajax_response_
    
  def output_ajax_response(self, response):
    self.response.headers.add_header("Content-Type", "application/json")
    #strs = [ p.get_json_string() for p in pagelets]
    self.response.out.write(response.get_json())
    
  def on_create_node(self, new_node):
    #OVERRIGHT this method to filter node or append node before/after
    return True
  
  def set_error(self, error):
    #TODO: Complete this method
    # in_ajax = 'inajax' in self.request.headers.keys()
    # if in_ajax:
    #   pass
      
    self.response.out.write('{"r":1, "msg":"Server error."}')
    
  def get_pagelets(self):
    response = self.get_ajax_response()
    return response.get_pagelet_json_objects()
  
  def render(self, template, context=None):
    context = context or {}
    
    page_header = self.render_page_header()
    page_footer = self.render_page_footer()
    # TODO: Add user role info for authentication purpose.
    extra_context = {
      'request': self.request,
      'uri_for': self.uri_for,
      'config': SITE_CONFIG,
      'parents_map': self.get_parents_map().get_json(),
      'root_nodes': self.get_parents_map().get_root_nodes_json(),
      'pagelets': json.dumps(self.get_pagelets()),
      'current_account': self.get_current_account(),
      'render_page_header': page_header,
      'render_page_footer': page_footer,
      'client_infor_map': self.get_client_infor_map().get_infor_map_json(),
      'root_nodes': self.get_client_infor_map().get_root_list_json()
    }
    #'get': EntityService().get #Shorthand for get entity, NOTE: 2012-11-01, disable this feature,
    # don't get entity on template.

    for key, value in extra_context.items():
      if key not in context:
        context[key] = value
    
    env = self.get_template_environment()
    template = env.get_template(template)
    self.response.out.write(template.render(context))
    
  def render_page_header(self):
    return ''
    # page_header = nodes.ZNodePageHeader(self)
    # page_header.set_root_node()
    # return page_header.render()
    
  def render_page_footer(self):
    return ''
    # page_footer = nodes.ZNodePageFooter(self)
    # page_footer.set_root_node()
    # return page_footer.render()
    
  def pagelet_(self, node_instance, render_position = PAGELET_RENDER_POSITION.BEFORE, ref_element_id = 'ref_element'):
    ref_element = self.request.get(ref_element_id)

    response = self.get_ajax_response();
    pagelet = Pagelet(node_instance)

    pagelet.set_ref_element(ref_element)
    pagelet.set_render_position(render_position)
    pagelet.set_render_type(PAGELET_RENDER_TYPE.DECORATION)

    response.add_pagelet(pagelet)
    self.output_ajax_response(response)

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
    