import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from model.question import *
from model.answer import *
from shared.znode import ZNode
from service import *
import datetime

class ZNodeTopicEditor(ZNode):
  template_ = 'topic_editor.html'
  client_type = 'ZH.ui.TagEditorRemote'
  # meta = {
  #   'question_id', 
  # }
  
  # view_data = {
  #   'question'
  # }
  
  def fetch_data_internal(self):
    question = Question.get_by_id(int(self.get_meta('question_id')))
    self.set_view_data_item('question', question)
    
  def fetch_data(self):
    question = self.get_view_data_item('question')
    if not question:
      self.fetch_data_internal()
      
    question = self.get_view_data_item('question')
    topics = [ t.get() for t in question.topics]
    self.set_view_data_item('topics', topics)
    
    self.set_meta('model', [ t.get_json_object() for t in topics ])
    
    
    
    
    
    