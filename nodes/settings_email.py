import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import service

from shared.znode import *

class ZNodeSettingsEmail(ZNode):
  # meta = {
  #   account_id
  # }
  
  # view_data = {
  #   account
  # }
  # 
  template_ = 'settings_email.html'
  client_type = 'ZH.page.SettingsEmail'
  
  def __init__(self, current_handler, meta = {}):
    #TODO: merge options.
    meta['page_url'] = '/settings/email'
    meta['page_group'] = 'settings_tab'
      
    super(ZNodeSettingsEmail, self).__init__(current_handler, meta = meta)
  
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    pass
    
    
    
    
    
