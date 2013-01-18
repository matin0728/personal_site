import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import service

from shared.znode import *

class ZNodePageHeader(ZNode):
  template_ = 'page_header.html'
  client_type = 'ZH.ui.PageHeader'
    
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    pass