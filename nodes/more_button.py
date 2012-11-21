import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from shared.znode import ZNode


class ZNodeMoreButton(ZNode):
  template_ = 'more_button.html'
  client_type = 'ZH.ui.MoreButton'
  
  # meta = {
  #   'request_url',
  # }
  
  # view-data = {
  #   'request_url'
  # }
  
  def fetch_data(self):
    self.set_view_data_item('request_url', self.get_meta('request_url'))
  