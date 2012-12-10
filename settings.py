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
      'render_main_content': self.render_main_content(),
      'render_nav_bar': self.render_nav_bar()
    }
    
    self.render('settings_base.html', context)
  
  def render_main_content(self):
    # Subclass should override this method.
    return ''
    
  def render_nav_bar(self):
    meta = {
      'active_tab': self.active_tab
    }
    nav_bar = nodes.ZNodeSettingsNav(self, meta)
    nav_bar.set_root_node()
    return nav_bar.render()
      
  def render_main_content(self):
    return 'Settings page'

class SettingsAccountHandler(SettingsBaseHandler):
  active_tab = 'account'
  def render_main_content(self):
    account_node = self.get_account_node_()
    account_node.set_root_node()
    return account_node.render()
  
  def get_account_node_(self):
    account = self.get_current_account()
    meta = {
      'account_id':account.key.id()
    }
    account_node = nodes.ZNodeSettingsAccount(self, meta)
    return account_node
    
  def pagelet(self):
    account_node = self.get_account_node_()
    ref_element = self.request.get('ref_element')
    
    response = self.get_ajax_response();
    pagelet = Pagelet(account_node)
    
    pagelet.set_ref_element(ref_element)
    pagelet.set_render_position(PAGELET_RENDER_POSITION.BEFORE)
    pagelet.set_render_type(PAGELET_RENDER_TYPE.DECORATION)

    response.add_pagelet(pagelet)
    self.output_ajax_response(response)
    
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
  def render_main_content(self):
    email_node = self.get_email_node_()
    email_node.set_root_node()
    return email_node.render()
  
  def get_email_node_(self):
    account = self.get_current_account()
    meta = {
      'account_id':account.key.id()
    }
    email_node = nodes.ZNodeSettingsEmail(self, meta)
    return email_node
    
  def pagelet(self):  
    email_node = self.get_email_node_()
    ref_element = self.request.get('ref_element')
    
    response = self.get_ajax_response();
    pagelet = Pagelet(email_node)
    
    pagelet.set_ref_element(ref_element)
    pagelet.set_render_position(PAGELET_RENDER_POSITION.BEFORE)
    pagelet.set_render_type(PAGELET_RENDER_TYPE.DECORATION)

    response.add_pagelet(pagelet)
    self.output_ajax_response(response)

  
    

      



