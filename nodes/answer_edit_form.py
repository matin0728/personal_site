import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from model.question import *
from model.answer import *
from shared.znode import ZNode
from service import *



class ZNodeAnswerEditForm(ZNode):
  # meta should contains following data.
  # meta = {
  #   'question_id',
  # }
  
  # view_data should contains(at least) following field.
  # view_data = {
  #  'question' : None
  #  'draft' : None
  # }
  # 
  template_ = 'answer_edit_form.html'
  client_type = 'ZH.ui.AnswerEditForm'