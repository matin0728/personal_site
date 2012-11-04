import webapp2
import jinja2
import os
from google.appengine.api import users
from service.entity import EntityService
import time, datetime
import json

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
  seed = None
  def get_next_id(self):
    if not self.seed:
      start = time.mktime(datetime.datetime(2000,1,1,0,0,0).timetuple())
      self.seed = int(time.time()) - int(start)
    else:
      self.seed = self.seed + 1
      
    return 'z' + str(self.seed)
  
  def set_parent(self, parent_id, child_id):
    if not parent_id in self.parents_map.keys():
      self.parents_map[parent_id] = [child_id]
    else:
      self.parents_map[parent_id].append(child_id)
      
  def get_json(self):
    return json.dumps(self.parents_map)

class ZNode(object):
  client_type = ''
  client_id = ''
  meta = {}
  template = ''
  config = {}
  view_data = {}
  current_handler = None
  
  def __init__(self, current_handler, meta = {}, config = {}):
    self.client_id = ParentsMap().get_next_id()
    self.client_id = 'ab'
    self.config = config
    self.meta = meta
    self.current_handler = current_handler
  
  def get_client_id(self):
    return self.client_id
  
  def add_child(self, child_node):
    ParentsMap().set_parent(self.get_client_id(), child_node.get_client_id())
    
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
    
    
  def get_config(self, key):
    return self.config[key]
  
  def node_attribute(self):
    return ' id="{0}" data-nodetype="{1}"'.format(self.client_id, self.client_type)
      
  def render(self):
    self.fetch_data()
    template = jinja_environment.get_template(self.template)
    self.set_view_data_item('uri_for', self.current_handler.uri_for)
    self.set_view_data_item('client_id', self.get_client_id())
    self.set_view_data_item('node_attribute', self.node_attribute)
    self.set_view_data_item('get', EntityService().get)
    return template.render(self.view_data)
    
    
    
    
    