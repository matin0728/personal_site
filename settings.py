# coding=utf-8

import webapp2
from google.appengine.api import users
from shared.base_handler import BaseHandler
import model
import service
import nodes
import shared.client_type_map as type_map
from shared.pagelet_processor import *

class SettingsBaseHandler(BaseHandler):
  active_tab = 'account'
  def get(self):
    context = {
      'render_settings_page': self.render_settings_page()
    }
    self.render('settings_base.html', context)
  
  def render_settings_page(self):
    page = self.get_content_node()
    page.set_root_node()
    return page.render()
    
  def get_content_node(self):
    meta = {
      'active_tab': self.active_tab
    }
    page = nodes.ZNodeSettingsPage(self, meta)
    return page
    
  def tab_content_pagelet(self):
    #subclass override.
    pass
    
  def pagelet(self):
    group_name = self.request.get('page_group')
    if group_name == 'default':
      content = self.get_content_node()
      self.pagelet_(content)
    else:
      self.tab_content_pagelet()

class SettingsAccountHandler(SettingsBaseHandler):
  active_tab = 'account'
  
  def tab_content_pagelet(self):
    account = self.get_current_account()
    meta = {
      'account_id':account.key.id()
    }
    content = nodes.ZNodeSettingsAccount(self, meta)
    self.pagelet_(content)
    
  def edit_name(self):
    nick_name = self.request.get('nickname')
    response = self.get_ajax_response()
    # Validation logic locats in service layer.
    success, error_messages = service.AccountService().update_nick_name(nick_name, self.get_current_account())
    
    edit_name_form_pagelet_ = response.get_pagelet_by_type('ZH.ui.SettingsFormEditName')
    edit_name_form_node_ = edit_name_form_pagelet_.get_node_instance()
    
    if success:
      # Close the edit form.
      edit_name_form_node_.set_expanded(False)
      response.set_message('保存成功！').set_refresh(True)
    else:
      for err in error_messages:
        edit_name_form_node_.append_error_message(err)

    self.output_ajax_response(response)
    
class SettingsEmailHandler(SettingsBaseHandler):
  active_tab = 'email'    

  def tab_content_pagelet(self):
    account = self.get_current_account()
    meta = {
      'account_id':account.key.id()
    }
    content = nodes.ZNodeSettingsEmail(self, meta)
    self.pagelet_(content)  

  
    

      



