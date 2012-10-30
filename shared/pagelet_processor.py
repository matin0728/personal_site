# import webapp2
# import jinja2
import os
import json
from module.shared import *

# from google.appengine.api import users
# from model.account import Account
# from service.entity import EntityService

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
  
  def get_json_string(self):
    return json.dumps([
      self.type_string,
      self.instance_identity,
      self.muckup,
      self.construct_args,
      self.ref_element,
      self.render_type,
      self.render_position,
      self.event_type,
      self.event_args
    ])

class LiveQueryProcessor(object):
  queries_ = []
  pagelets = None
  
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
        
  def get_pagelets(self, handler):      
    if not self.pagelets:
      self.pagelets = []
      for q in self.queries_:
        pl = Pagelet(
          q['type_string'], 
          instance_identity = q['instance_id'], 
          muckup = LiveQueryProcessor.create_node_muckup(q['type_string'], q["component_meta"], handler))
        self.pagelets.append(pl)
        
    return self.pagelets  
      
      
      
      