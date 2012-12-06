# coding=utf-8

import webapp2
from google.appengine.api import users
from shared.base_handler import BaseHandler
import model
import service
import nodes

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
    meta = {}
    account_node = nodes.ZNodeSettingsAccount(self, meta)
    account_node.set_root_node()
    return account_node.render()
    
class SettingsEmailHandler(SettingsBaseHandler):
  active_tab = 'email'
  def render_main_content(self):
    return ''

  
    

      



