import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import service

from shared.znode import *

class ZNodeSettingsFormEditName(ZNode):
  # meta = {
  # }
  
  # view_data = {
  # }
  # 
  template_ = 'settings_form_edit_name.html'
  client_type = 'ZH.ui.SettingsFormEditName'
  
  def __init__(self, current_handler, meta = {}):
    super(ZNodeSettingsFormEditName, self).__init__(current_handler, meta = meta)
    self.error_messages_ = []
    self.expanded_ = False
    if 'expanded' in meta.keys():
      self.expanded_ = True if int(meta['expanded']) == 1 else False
  
  def fetch_data_internal(self):
    pass
    
  def set_expanded(self, is_expanded):
    self.expanded_ = is_expanded
    
  def fetch_data(self):
    self.set_view_data_item('expanded', self.expanded_)
    self.set_view_data_item('error_messages', self.error_messages_)
    
  def append_error_message(self, error_message):
    self.error_messages_.append(error_message)
    
    
    
    
    
    
