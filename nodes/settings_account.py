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
  #   account_id:xxx
  # }
  
  # view_data = {
  #   account
  # }
  # 
  template_ = 'settings_account.html'
  client_type = 'ZH.ui.SettingsAccount'
  
  def fetch_data_internal(self):
    account = model.Account.get_by_id(int(self.get_meta('account_id')))
    self.set_view_data_item('account', account)
    
  def fetch_data(self):
    account = self.get_view_data_item('account')
    if not account:
      self.fetch_data_internal()
      
    meta = {}
    form_edit_name = ZNodeSettingsFormEditName(self.get_handler(), meta)
    self.add_child(form_edit_name)
    self.set_meta('form_edit_name', form_edit_name.get_client_id())
    self.set_view_data_item('render_form_edit_name', self.render_form_edit_name(form_edit_name))
    
  def render_form_edit_name(self, form_edit_name):
    return form_edit_name.render()
    
    
    
    
