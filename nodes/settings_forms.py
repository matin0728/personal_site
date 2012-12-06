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
  
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    
    pass
    
    
    
    
    
    
