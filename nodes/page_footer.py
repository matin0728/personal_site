import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import service

from shared.znode import *

class ZNodePageFooter(ZNode):
  template_ = 'page_footer.html'
  client_type = 'ZH.ui.PageFooter'
    
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    pass