# coding=utf-8

import webapp2
from google.appengine.api import users
from shared.base_handler import BaseHandler
from model import *
from service import *
import nodes

class CommentListHandler(BaseHandler):
  def get(self, entity_key_string):
    context = {
      'entity_key_string': entity_key_string,
      'render_comment_list': self.render_comment_list
    }
    self.render('comment_list_page.html', context)
  
    
  def render_comment_list(self, entity_key_string):
    meta = {
      'entity_key_string': entity_key_string
    }
    comment_list = nodes.ZNodeCommentList(self, meta = meta)
    comment_list.set_root_node()
    return comment_list.render()

class CommentDeleteHandler(BaseHandler):
  def post(self, comment_key):
    CommentService().delete_comment(comment_key)
    self.redirect(self.uri_for('home'))
  
  def get(self, comment_key):
    return self.post(comment_key)
    
class AddCommentHandler(BaseHandler):
  def post(self, entity_key_string):
    content = self.request.get('content')
    comments_wrap = self.request.get('comments_wrap')
    if not content:
      #TODO: Handle error report, when in ajax mode.
      # self.redirect(self.uri_for('home'))
      return
      
    account = self.get_current_account()
    new_comment = CommentService().add_comment(account, entity_key_string, content) 
    # TODO: return new comment pagelet to client side.
    # self.redirect(self.uri_for('home'))
    
    
    
    
    
    
    
    
    