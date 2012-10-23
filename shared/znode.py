import webapp2
import jinja2
import os
from google.appengine.api import users
from service.entity import EntityService

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__) + '/../templates')))

# class ZContext(object):
#   questions = {}
#   answers = {}
#   def get_question(self, qeustion_id):
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
  

class ZNode(object):
  meta = {}
  template = None
  config = {}
  view_data = {}
  current_handler = None
  def __init__(self, current_handler, meta = {}, config = {}):
    self.config = config
    self.meta = meta
    self.current_handler = current_handler
    
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
      
  def render(self):
    self.fetch_data()
    template = jinja_environment.get_template(self.template)
    self.set_view_data_item('uri_for', self.current_handler.uri_for)
    self.set_view_data_item('get', EntityService().get)
    return template.render(self.view_data)
    
    
    
    
    