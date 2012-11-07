import webapp2
import jinja2
import os
from google.appengine.api import users
from service.entity import EntityService
import time, datetime
import json
from client_type_map import CLIENT_TYPE_MAP

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__) + '/../templates')))

# class ZContext(object):
#   questions = {}
#   answers = {}
#   def get_question(self, question_id):
#     pass
#     
#   def get_answer(self, answer_id):
#     pass
#   
#   #Each entity type needs a method like this.  
#   def batch_fetch_question(self, question_id_set = []):
#     keys = question.keys()
#     keys_to_fetch = []
#     for k in question_id_set:
#       if not k in keys:
#         keys_to_fetch.append(k)
#     get_multi


class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
        
class ParentsMap(Singleton):
  parents_map = {}
  root_nodes = []
  seed = None
  def get_next_id(self):
    if not self.seed:
      # start = time.mktime(datetime.datetime(2008,1,1,0,0,0).timetuple())
      # self.seed = int(time.time()) - int(start)
      self.seed = 100
    else:
      self.seed = self.seed + 1
      
    return str(hex(self.seed))[1:]
  
  def set_parent(self, parent_id, child_node_info):
    if not parent_id in self.parents_map.keys():
      self.parents_map[parent_id] = [child_node_info]
    else:
      self.parents_map[parent_id].append(child_node_info)
  
  def get_parents_map(self):
    return self.parents_map
      
  def get_json(self):
    return json.dumps(self.parents_map)
    
  def add_root_node(self, node_client_id):
    self.root_nodes.append(node_client_id)
  
  def get_root_nodes(self):
    return self.root_nodes
    
  def get_root_nodes_json(self):
    return json.dumps(self.root_nodes)

class ZNode(object):
  #Subclall will overide this from clienttype map(May be create by script).
  client_type = ''
  #Auto generate.
  client_id = ''
  meta = {}
  template = ''
  config = {}
  view_data = {}
  current_handler = None
  
  def set_root_node(self):
    ParentsMap().add_root_node([self.get_client_id(), self.get_type()])
  
  def __init__(self, current_handler, meta = {}, config = {}):
    self.client_id = ParentsMap().get_next_id()
    #Not used at this moment.
    self.config = config 
    self.meta = meta
    self.current_handler = current_handler
    self.child_nodes = []
  
  def get_client_id(self):
    return self.client_id
    
  #NOTE: used for update existing component  
  def set_client_id(self, client_id):
    self.client_id = client_id
  
  def add_child(self, child_node):
    self.child_nodes.append(child_node)
    ParentsMap().set_parent(self.get_client_id(), [child_node.get_type(), child_node.get_client_id()])
    
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
    #NOTE: Subclass will override this method.
    pass
    
  def get_meta(self, key):
    if key in self.meta:
      return self.meta[key]
      
    return None
  
  def get_type(self):
    return CLIENT_TYPE_MAP[self.client_type]
    
  def get_raw_type(self):
    return self.client_type
    
  def get_config(self, key):
    return self.config[key]
  
  def node_attribute(self):
    return ' id="{0}" '.format(self.get_client_id())
      
  def get_pagelet_meta(self):
    # self.type_string,
    # self.instance_identity,
    # self.markup,
    # self.child_nodes,
    return [
      self.get_type(),
      self.get_client_id(),
      self.render(),
      self.child_nodes
    ]    
      
  def render(self):
    self.fetch_data()
    # #Add parents map.
    # ParentsMap().set_parent(self.get_client_id(), self.child_nodes)
    
    template = jinja_environment.get_template(self.template)
    self.set_view_data_item('uri_for', self.current_handler.uri_for)
    self.set_view_data_item('client_id', self.get_client_id())
    self.set_view_data_item('node_attribute', self.node_attribute)
    self.set_view_data_item('get', EntityService().get)
    return template.render(self.view_data)
    
    
    
    
    