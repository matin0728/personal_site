# import webapp2
# import jinja2
import os
import json
from module.shared import *

# from google.appengine.api import users
# from model.account import Account
# from service.entity import EntityService

class AjaxResponse(object):
  # this.isError = (result["r"] == 1);
  # this.message = result["msg"];
  # this.redirectUrl = result["redirect"];
  # this.refreshFlag = result["refresh"];
  error_flag = 0
  message = ''
  redirect_url = ''
  refresh_flag = 0
  pagelets = []
  
  def set_refresh(self, is_refresh):
    if is_refresh:
      self.refresh_flag = 1
    else:
      self.refresh_flag = 0
  
  def set_redirect(self, redirect_url):
    self.redirect_url = redirect_url
  
  def set_error_flag(self, is_error):
    if is_error:
      self.error_flag = 1
    else:
      self.error_flag = 0
      
      
  def set_message(self, message):
    self.message = message
  
  def get_json(self):
    pagelet_json_objects = [ p.get_json_object() for p in self.pagelets]
    result = {
      'r': self.error_flag,
      'msg': self.message,
      'redirect': self.redirect_url,
      'refresh': self.refresh_flag,
      'pagelets': pagelet_json_objects
    }
    return json.dumps(result)
  
  def get_pagelet_by_type(self, type_string):
    for p in self.pagelets:
      if p.type_string == type_string:
        return p
        
  def get_pagelets_by_type(self, type_string):
    found = []
    for p in self.pagelets:
      if p.type_string == type_string:
        found.append(p)
    
    return found
    
  def add_pagelet(self, pagelet):
    self.pagelets.append(pagelet)

class Pagelet(object):
  type_string = ''
  instance_identity = ''
  muckup = ''
  construct_args = ''  #Should be a key-value based json object, not used at this moment.
  ref_element = ''
  render_type = 'updating' # default set to updating, case most case is in the live query.
  render_position = 'append'
  event_type = ''
  event_args = '' #Should be json object.
  
  def __init__(self, type_string, instance_identity = '', muckup = ''):
    self.type_string = type_string
    self.instance_identity = instance_identity
    self.muckup = muckup
    
  def set_instance_identity(self, instance_identity):
    self.instance_identity = instance_identity
    return self
    
  def set_construct_arg_string(self, construct_arg_string):
    self.construct_args = construct_arg_string
    return self
    
  def set_ref_element(self, ref_element):
    self.ref_element = ref_element
    return self
  
  def set_render_type(self, render_type):
    self.render_type = render_type
    return self
    
  def set_render_position(self, render_position):
    self.render_position = render_position
    return self
    
  def add_event(self, event_type_string, event_arg_string):
    #NOTE: Currently we don't support multi events.
    self.event_type = event_type_string
    self.event_args = event_arg_string
    return self
  
  def get_json_object(self):
    return [
      self.type_string,
      self.instance_identity,
      self.muckup,
      self.construct_args,
      self.ref_element,
      self.render_type,
      self.render_position,
      self.event_type,
      self.event_args
    ]

class LiveQueryProcessor(object):
  queries_ = []
  result_ = None
  
  @classmethod 
  def deserialize_meta(cls, meta_data):
    meta = {}
    data = string.split(meta_data, "&")
    for item in data:
      item = string.split(item, '=')
      meta[item[0]] = item[1]
    
    return meta
  
  @classmethod 
  def create_node_muckup(cls, node_name, meta_data, handler, config_data = {}): 
    nodes = {
      'demo':DemoNode
    }
    
    if not isinstance(meta_data, basestring):
      meta_data = cls.deserialize_meta(meta_data)
  
    if node_name in nodes.keys():
      node_ = nodes[node_name]
      instance = node_(handler, meta = meta_data, config = config_data)
      return instance.render()
    
             
  def __init__(self, live_queries):
    self.queries_ = json.loads(live_queries)
        
  def get_response(self, handler):      
    if not self.result_:
      pagelets = []
      for q in self.queries_:
        pl = Pagelet(
          q['type_string'], 
          instance_identity = q['instance_id'], 
          muckup = LiveQueryProcessor.create_node_muckup(q['type_string'], q["component_meta"], handler))
        pagelets.append(pl)
        
      result = AjaxResponse()
      result.pagelets = pagelets
      self.result_ = result
        
    return self.result_  
      
      
      
      