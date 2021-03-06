import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import service

from shared.znode import *
import nodes

class ZNodeSettingsPage(ZNode):
  # meta = {
  #   'active_tab',
  # }
  
  # view_data = {
  # }
  # 
  template_ = 'settings/settings_page.html'
  client_type = 'ZH.page.SettingsPage'
  
  def __init__(self, current_handler, meta = {}):
    #TODO: merge options.
    meta['page_url'] = '/settings/' + meta['active_tab']
    super(ZNodeSettingsPage, self).__init__(current_handler, meta = meta)
  
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    self.set_view_data_item('render_main_content', self.render_main_content())
    self.set_view_data_item('render_nav_bar', self.render_nav_bar())
    
  def render_main_content(self):
    # Subclass should override this method.
    tab = self.get_meta('active_tab')
    account = self.get_handler().get_current_account()
    meta = {
      'account_id':account.key.id()
    }
    
    content = None
    
    if tab == 'account':
      content = nodes.ZNodeSettingsAccount(self.get_handler(), meta)
    elif tab == 'email':
      content = nodes.ZNodeSettingsEmail(self.get_handler(), meta)
    elif tab == 'notify':
      content = nodes.ZNodeSettingsNotify(self.get_handler(), meta)
    elif tab == 'bind':
      content = nodes.ZNodeSettingsBind(self.get_handler(), meta)
    elif tab == 'block_user':
      content = nodes.ZNodeSettingsBlockUser(self.get_handler(), meta)
    
    self.add_child(content)
    return content.render()

  def render_nav_bar(self):
    meta = {
      'active_tab': self.get_meta('active_tab'),
      'page_group_name': 'settings_tab'
    }
    nav_bar = nodes.ZNodeSettingsNav(self.get_handler(), meta)
    self.add_child(nav_bar)
    return nav_bar.render()  
    
    
    
    
    
