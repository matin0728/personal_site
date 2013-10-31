# coding=utf-8

import os
from google.appengine.ext import ndb
import model
import shared.node as znode
import service
import datetime


class AnswerEditFormDisabledInfo(znode.ZNode):
  # IMPORTANT: This node is simple enough to use base class: live component,
  # If any action need add in, you should create a new subclass from liveComponent.
  def __init__(self, meta = {}, parent_node = None):
    super(AnswerEditForm, self).__init__(meta = meta, parent_node = parent_node)
    self.template = 'answer_edit_form_disabled_info.html'
    self.js_path = 'answer_edit_form_disabled_info'


class AnswerEditForm(znode.ZNode):
  def __init__(self, meta = {}, parent_node = None):
    super(AnswerEditForm, self).__init__(meta = meta, parent_node = parent_node)
    self.template = 'answer_edit_form.html'
    self.js_path = 'answer_edit_form'
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
  