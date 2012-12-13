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
  
  def __init__(self, current_handler, meta = {}):
    # TODO: Can we retrive current request path from 
    # request object(Not include question string and hash)?
    # Only [list like] page needs to be set as base page, whick will be reserved dring
    # loading new pages.
    
    #TODO: merge options.
    meta['page_url'] = '/'
    # default group is no need to set
    # meta['page_group'] = 'default'
    meta['is_base'] = 1
    super(ZNodeHomePage, self).__init__(current_handler, meta = meta)
  
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