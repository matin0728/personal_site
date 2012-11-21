# coding=utf-8

import webapp2
from google.appengine.api import users
from shared.base_handler import BaseHandler
from shared.pagelet_processor import *
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
    # No need to set as root node.
    #comment_list.set_root_node()
    return comment_list.render()

class CommentDeleteHandler(BaseHandler):
  def post(self, comment_key_string):
    CommentService().delete_comment(comment_key_string)
    type_string = self.request.get('client_type')
    client_id = self.request.get('client_id')
    
    pagelet = Pagelet(None, type_string = type_string, client_id = client_id, markup = '')
    pagelet.set_render_type(PAGELET_RENDER_TYPE.UN_RENDER)
    response = self.get_ajax_response()
    response.add_pagelet(pagelet)
    self.output_ajax_response(response)
    # self.redirect(self.uri_for('home'))
  
  def get(self, comment_key_string):
    pass
    # return self.post(comment_key)
    
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
    
    meta = {
      'comment_key_string':entity_key_string
    }
    commentNode = nodes.ZNodeComment(self, meta)
    commentNode.set_view_data_item('comment', new_comment)
    # return new comment pagelet to client side.
    pagelet = Pagelet(commentNode)
    pagelet.set_ref_element(comments_wrap) \
      .set_render_position(PAGELET_RENDER_POSITION.APPEND) 
    
    response = self.get_ajax_response()
    response.add_pagelet(pagelet)
    self.output_ajax_response(response)
    
    # self.redirect(self.uri_for('home'))
    
    
    
    
    
    
    
    
    