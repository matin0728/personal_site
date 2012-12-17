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
  template_ = 'settings/settings_account.html'
  client_type = 'ZH.page.SettingsAccount'
  
  def __init__(self, current_handler, meta = {}):
    #TODO: merge options.
    meta['page_url'] = '/settings/account'
    meta['page_group'] = 'settings_tab'
    super(ZNodeSettingsAccount, self).__init__(current_handler, meta = meta)
  
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
    self.set_view_data_item('render_form_edit_name', form_edit_name.render())
    
    form_edit_url = ZNodeSettingsFormEditUrl(self.get_handler(), meta)
    self.add_child(form_edit_url)
    self.set_meta('form_edit_url', form_edit_url.get_client_id())
    self.set_view_data_item('render_form_edit_url', form_edit_url.render())
    
    form_edit_email = ZNodeSettingsFormEditEmail(self.get_handler(), meta)
    self.add_child(form_edit_email)
    self.set_meta('form_edit_email', form_edit_email.get_client_id())
    self.set_view_data_item('render_form_edit_email', form_edit_email.render())
    
    form_edit_password = ZNodeSettingsFormEditPassword(self.get_handler(), meta)
    self.add_child(form_edit_password)
    self.set_meta('form_edit_password', form_edit_password.get_client_id())
    self.set_view_data_item('render_form_edit_password', form_edit_password.render())
    
  # def render_form_edit_name(self, form_edit_name):
  #   return form_edit_name.render()
    
    
    
    





