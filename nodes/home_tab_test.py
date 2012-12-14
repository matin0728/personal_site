import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import shared
import service
from feed import *
import nodes

class ZNodeHomeTabTest(ZNode):
  # meta = {
  #   'active_tab',
  # }
  
  # view_data = {
  #  
  # }
  # 
  template_ = 'home_tab_test.html'
  client_type = 'ZH.ui.HomeTabPane'
  
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    home_tab = {
    }
    active_tab = self.get_meta('active_tab')
    if not active_tab:
      active_tab = 'home'
      
    home_tab[active_tab] = ' class="active"'
    self.set_view_data_item('home_tab', home_tab)
    
    
    
    
    
    
    