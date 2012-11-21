import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import shared
import service
from feed import *

class ZNodeHomePage(ZNode):
  # meta = {
  #   None
  # }
  
  # view_data = {
  #  
  # }
  # 
  template_ = 'home_page.html'
  client_type = 'ZH.page.HomePage'
  
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    self.set_view_data_item('render_feed_list', self.render_feed_list)
    
  def render_feed_list(self):
    meta = {
      'start': 0
    }
    feed_list = ZNodeHomeFeedList(self.get_handler(), meta)
    self.add_child(feed_list)
    return feed_list.render()