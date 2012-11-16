import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from model.question import *
from model.answer import *
from shared.znode import ZNode
import service

from shared.znode import *


class ZNodeComment(ZNode):
  # meta should contains following data.
  # meta = {
  #   'comment_key_string',
  # }
  
  # view_data should contains(at least) following field.
  # view_data = {
  #  'comment' : None
  # }
  # 
  template_ = 'comment.html'
  client_type = 'ZH.ui.Comment'
    
  def fetch_data_internal(self):
    comment_key = ndb.Key(urlsafe = self.get_meta('comment_key_string'))
    comment = comment_key.get()
    self.set_view_data_item('comment', comment)
    
  def fetch_data(self):
    comment = self.get_view_data_item('comment')
    if not comment:
      self.fetch_data_internal()

class ZNodeCommentList(ZNode):
  # TODO: Forbidden anonymouse users to add comment.
  # meta should contains following data.
  # meta = {
  #   'entity_key_string',
  # }
  
  # view_data should contains(at least) following field.
  # view_data = {
  #  'comments' : None
  # }
  # 
  template_ = 'comment_list.html'
  client_type = 'ZH.ui.CommentList'
    
  def fetch_data_internal(self):
    comments = service.CommentService().get_comments(self.get_meta('entity_key_string'))
    
    self.set_view_data_item('comments', comments)
  
  def render_comment(self, comment):
    meta = {
      'comment_key_string': comment.key.urlsafe()
    }
    item = ZNodeComment(self.current_handler, meta = meta)
    item.set_view_data_item('comment', comment)
    self.add_child(item)
    return item.render()
  
  def fetch_data(self):
    comments = self.get_view_data_item('comments')
    if not comments:
      self.fetch_data_internal()
      
    self.set_view_data_item('entity_key_string',self.get_meta('entity_key_string'))
    self.set_view_data_item('render_comment', self.render_comment)
    # TODO: anonymouse check.
    self.set_view_data_item('allow_to_create_comment', True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    