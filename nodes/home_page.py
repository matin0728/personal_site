import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import shared
import service
from feed import *
import nodes

class ZNodeHomePageBase(ZNode):
  # meta = {
  #   'active_tab',
  # }
  
  # view_data = {
  #  
  # }
  # 
  template_ = 'home_page.html'
  client_type = 'ZH.page.HomePage'
  tab_ = ''
  
  def __init__(self, current_handler, meta = {}):
    meta['is_base'] = 1
    super(ZNodeHomePageBase, self).__init__(current_handler, meta = meta)
  
  def render_feed_list(self):
    meta = {
      'start': 0
    }
    feed_list = ZNodeHomeFeedList(self.get_handler(), meta)
    self.add_child(feed_list)
    return feed_list.render()

  def fetch_data_internal(self):
    pass

  def fetch_data(self):
    self.set_view_data_item('render_feed_list', self.render_feed_list)
    self.set_view_data_item('render_home_tab', self.render_home_tab)
    
  def render_home_tab(self):
    meta = {
      'active_tab': self.tab_
    }
    home_tab = nodes.ZNodeHomeTabTest(self.get_handler(), meta)
    self.add_child(home_tab)
    return home_tab.render()
    
    
class ZNodeHomePageFeed(ZNodeHomePageBase):
  tab_ = 'home'
  def __init__(self, current_handler, meta = {}):
    meta['page_url'] = '/'
    super(ZNodeHomePageFeed, self).__init__(current_handler, meta = meta)

class ZNodeHomeMyQuestion(ZNodeHomePageBase):
  template_ = 'home_page_myquestion.html'
  tab_ = 'my_question'
  def __init__(self, current_handler, meta = {}):
    meta['page_url'] = '/myquestion'
    super(ZNodeHomeMyQuestion, self).__init__(current_handler, meta = meta)   
    
    
    
    