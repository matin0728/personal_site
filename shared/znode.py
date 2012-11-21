# coding=utf-8

import webapp2
import jinja2
import os
from google.appengine.api import users
from service.entity import EntityService
import time, datetime
import json
from client_type_map import *

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__) + '/../templates')))

        
class ParentsMap(object):
  str_list = 'qwertyuiopasdfghjklzxcvbnm1234567890'
  def __init__(self):
    self.parents_map_ = {}
    self.root_nodes_ = []
    self.seed_ = None
    super(ParentsMap, self).__init__()
    
    
  def map_name_(self, str_index):
    s = []
    t = str_index
    while t > 0:
        p = (t % 36)
        s.append(self.str_list[p])
        t /= 36
        
    return ''.join(s)
    
  def get_next_id(self, str_type):
    if not self.seed_:
      self.seed_ = int(time.time()*10) - int(time.mktime(datetime.datetime(2012,1,1,0,0,0).timetuple())*10)
    else:
      self.seed_ = self.seed_ + 1
        
    return str_type + self.map_name_(self.seed_)
  
  def set_parent(self, parent_id, child_node_info):
    if not parent_id in self.parents_map_.keys():
      self.parents_map_[parent_id] = [child_node_info]
    else:
      self.parents_map_[parent_id].append(child_node_info)
  
  def get_parents_map(self):
    return self.parents_map_
      
  def get_json(self):
    return json.dumps(self.parents_map_)
    
  def add_root_node(self, node_info):
    self.root_nodes_.append(node_info)
  
  def get_root_nodes(self):
    return self.root_nodes_
    
  def get_root_nodes_json(self):
    return json.dumps(self.root_nodes_)

#NOTE: Do we need provide a method to set template name at runtime?
class ZNode(object):
  template_ = ''
  client_type = 'ZH.common.LiveComponent'
  def set_root_node(self):
    self.get_handler().get_parents_map().add_root_node([self.get_type(), self.get_client_id()])
  
  """A creation filter.
  handler can add node near the new node or return false to prevent new node to be 
  created.
  """
  def on_create_node(self, new_node):
    handler = self. get_handler()
    if handler.on_create_node(new_node):
      return new_node
    else:
      return None
  
  def __init__(self, current_handler, meta = {}):
    self.view_data = {}
    self.template = self.template_
    # self.config = config 
    self.meta = meta
    self.current_handler = current_handler
    self.child_nodes = []
    self.parents_map = self.current_handler.get_parents_map()
    #Auto generate.
    self.client_id = self.parents_map.get_next_id(CLIENT_TYPE_MAP[self.client_type])
    self.parent_ = None
  
  def get_client_id(self):
    return self.client_id
    
  def get_handler(self):
    return self.current_handler
    
  #NOTE: used for update existing component  
  def set_client_id(self, client_id):
    self.client_id = client_id
    
  def get_client_id(self):
    return self.client_id
    
  def get_parent(self):
    return self.parent_
    
  def set_parent(self, parent_node):
    self.parent_ = parent_node
  
  def add_child(self, child_node):
    child_node.set_parent(self)
    self.child_nodes.append(child_node)
    self.get_handler().get_parents_map().set_parent(self.get_client_id(), [child_node.get_type(), child_node.get_client_id()])
    
  def get_view_data_item(self, key):
    if key in self.view_data.keys():
      return self.view_data[key]

  def set_view_data_item(self, key, data_item):
    self.view_data[key] = data_item

  def set_view_data(self, data):
    self.view_data = data

  def set_template(self, template):
    self.template = template
      
  def fetch_data(self):
    #NOTE: Subclass will override self method.
    pass
    
  def set_meta(self, key, value):
    self.meta[key] = value
    
  def get_meta(self, key):
    if key in self.meta:
      return self.meta[key]
    elif self.get_parent():
      return self.get_parent().get_meta(key)
      
    return None
  
  def get_type(self):
    return CLIENT_TYPE_MAP[self.client_type]
    
  def get_raw_type(self):
    return self.client_type
    
  # def get_config(self, key):
  #   return self.config[key]
  
  def node_attribute(self):
    meta_data = self.meta
    # m = '&'.join(['{0}={1}'.format(k, str(meta_data[k]).replace('=', '○').replace('&', '⊕')) for k in meta_data ])
    # m = '&'.join(['{0}={1}'.format(k, str(meta_data[k]).replace('=', u'○').replace('&', u'⊕')) for k in meta_data ])
    m = json.dumps(meta_data)
    
    return ' id="{0}" data-meta=\'{1}\''.format(self.get_client_id(), m)
      
  def get_pagelet_meta(self):
    # self.type_string,
    # self.instance_identity,
    # self.markup,
    # self.child_nodes,
    return [
      self.get_type(),
      self.get_client_id(),
      self.render()
    ]
    # TODO: WHY child nodes here ? Do we need this method?
    return [
      self.get_type(),
      self.get_client_id(),
      self.render(),
      self.child_nodes
    ]    
      
  def render(self):
    self.fetch_data()
    
    template = jinja_environment.get_template(self.template)
    # Global data, is accessable for all template, 
    # Future, we need user roles data to control admin func display.
    self.set_view_data_item('uri_for', self.current_handler.uri_for)
    self.set_view_data_item('node_attribute', self.node_attribute)
    self.set_view_data_item('current_account', self.current_handler.get_current_account())
    return template.render(self.view_data)
    
    
    
    
    