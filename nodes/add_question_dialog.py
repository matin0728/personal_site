import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import model
import service

from shared.znode import *

class ZNodeAddQuestionDialog(ZNode):
  template_ = 'add_question_dialog.html'
  client_type = 'ZH.ui.AddQuestionDialog'
    
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    pass