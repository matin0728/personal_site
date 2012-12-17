import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import service

from shared.znode import *

class ZNodeSettingsBind(ZNode):
  # meta = {
  #   account_id
  # }
  
  # view_data = {
  #   account
  # }
  # 
  template_ = 'settings/settings_bind.html'
  client_type = 'ZH.page.SettingsBind'
  
  def __init__(self, current_handler, meta = {}):
    #TODO: merge options.
    meta['page_url'] = '/settings/bind'
    meta['page_group'] = 'settings_tab'
      
    super(ZNodeSettingsBind, self).__init__(current_handler, meta = meta)
  
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    pass
    
    
    
    
    
