import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import service

from shared.znode import *

class ZNodeSettingsNav(ZNode):
  # meta = {
  #   'active_tab',
  # }
  
  # view_data = {
  # }
  # 
  template_ = 'settings/settings_nav.html'
  client_type = 'ZH.ui.SettingsTabPane'
  
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    settings_tab = {
    }
    active_tab = self.get_meta('active_tab')
    if not active_tab:
      active_tab = 'account'
      
    settings_tab[active_tab] = ' class="active"'
    self.set_view_data_item('settings_tab', settings_tab)
    
    
    
    
    
    