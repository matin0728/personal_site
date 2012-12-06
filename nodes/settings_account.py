import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import service

from shared.znode import *
from settings_forms import *

class ZNodeSettingsAccount(ZNode):
  # meta = {
  # }
  
  # view_data = {
  # }
  # 
  template_ = 'settings_account.html'
  client_type = 'ZH.page.SettingsAccount'
  
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    meta = {}
    form_edit_name = ZNodeSettingsFormEditName(self.get_handler(), meta)
    self.add_child(form_edit_name)
    self.set_meta('form_edit_name', form_edit_name.get_client_id())
    self.set_view_data_item('render_form_edit_name', self.render_form_edit_name(form_edit_name))
    
  def render_form_edit_name(self, form_edit_name):
    return form_edit_name.render()
    
    
    
    
