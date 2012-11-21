# import webapp2
# import jinja2
import logging
import os
import json
# from module.shared import *
from znode import ParentsMap
from nodes import *
from client_type_map import *

# from google.appengine.api import users
# from model.account import Account
# from service.entity import EntityService

class AjaxResponse(object):
  # this.isError = (result["r"] == 1);
  # this.message = result["msg"];
  # this.redirectUrl = result["redirect"];
  # this.refreshFlag = result["refresh"];
  def __init__(self, parents_map):
    self.error_flag = 0
    self.message = ''
    self.redirect_url = ''
    self.refresh_flag = 0
    self.pagelets = []
    self.extra_data = None
    self.parents_map = parents_map
  
  """Extra json data object send to client.
    Custom json data.
  """
  def set_data(self, extra_data):
    self.extra_data = extra_data
    return self
    
  def set_refresh(self, is_refresh):
    if is_refresh:
      self.refresh_flag = 1
    else:
      self.refresh_flag = 0
    
    return self
  
  """Redirect url
    if message is set, show msg first then redirect to this url.
  """
  def set_redirect(self, redirect_url):
    self.redirect_url = redirect_url
    return self
  
  def set_error_flag(self, is_error):
    if is_error:
      self.error_flag = 1
    else:
      self.error_flag = 0
    
    return self
      
  """String message send to client
    Success or fail message.
  """
  def set_message(self, message):
    self.message = message
    return self
    
  def get_pagelet_json_objects(self):
    pagelet_json_objects = [ p.get_json_object() for p in self.pagelets]
    return pagelet_json_objects
  
  def get_json(self):
    #ru: redirect_url, rf: refresh_flag, p: pagelets, d: extra_data, rn:root_nodes, mp: parents_map

    result = {
      'r': self.error_flag,
      'msg': self.message,
      'ru': self.redirect_url,
      'rf': self.refresh_flag,
      'd': self.extra_data,
      'mp': self.parents_map.get_parents_map(),
      'rn': self.parents_map.get_root_nodes(),
      'p': self.get_pagelet_json_objects()
    }
    return json.dumps(result)
  
  def get_pagelet_by_type(self, type_string):
    for p in self.pagelets:
      if p.type_string == CLIENT_TYPE_MAP[type_string]:
        return p
        
  def get_pagelets_by_type(self, type_string):
    found = []
    for p in self.pagelets:
      if p.type_string == CLIENT_TYPE_MAP[type_string]:
        found.append(p)
    
    return found
    
  def add_pagelet(self, pagelet):
    self.pagelets.append(pagelet)

class PAGELET_RENDER_TYPE(object):
    UPDATING = 'updating'
    DECORATION = 'decoration'
    UN_RENDER = 'un_render'
    
class PAGELET_RENDER_POSITION(object):
  INNER = 'inner'
  APPEND = 'append'
  BEFORE = 'before'
  AFTER = 'after'

class Pagelet(object):
  def __init__(self, znode_instance, type_string = '', client_id = '', markup = ''):
    self.znode = None
    if znode_instance:
      self.znode = znode_instance
      self.type_string = znode_instance.get_type()
      self.client_id = znode_instance.get_client_id()
    else:
      self.type_string = type_string
      self.client_id = client_id
      self.markup = markup
      
    self.ref_element = ''
    # default set to decoration, case most use case is in the handler, to append
    # extra pagelet to page, and in live query, default set to UPDATING.
    self.render_type = PAGELET_RENDER_TYPE.DECORATION
    self.render_position = PAGELET_RENDER_POSITION.APPEND
    self.event_type = ''
    self.event_args = '' #Should be json object.
    
  def set_ref_element(self, ref_element):
    self.ref_element = ref_element
    return self
  
  def set_render_type(self, render_type):
    self.render_type = render_type
    return self
    
  def set_render_position(self, render_position):
    self.render_position = render_position
    return self
    
  def set_event(self, event_type_string, event_arg_string):
    #NOTE: Currently we don't support multi events.
    self.event_type = event_type_string
    self.event_args = event_arg_string
    return self
    
  def get_node_instance(self):
    return self.znode
  
  def get_json_object(self):
    if self.znode:
      node_meta_json = self.znode.get_pagelet_meta()
    else:
      node_meta_json = [
        self.type_string,
        self.client_id,
        self.markup
      ]
      
    node_meta_json.extend([
      self.ref_element,
      self.render_type,
      self.render_position,
      self.event_type,
      self.event_args
    ])
    return node_meta_json

class LiveQueryProcessor(object):
  def __init__(self, live_queries):
    super(LiveQueryProcessor, self).__init__()
    
    if live_queries:
      self.queries_ = json.loads(live_queries)
    else:
      self.queries_ = []      
      
    self.result_ = None
    
  @classmethod 
  def deserialize_meta(cls, meta_data):
    return json.loads(meta_data)
    # meta = {}
    # data = meta_data.split("&")
    # for item in data:
    #   d = item.split('=')
    #   if len(d) == 2:
    #     meta[d[0]] = d[1]
    
    # return meta
  
  @classmethod 
  def create_node(cls, node_name, instance_identity, meta_data, handler): 
    nodes = {
      'demo':DemoNode,
      'ZH.ui.FeedMeta': ZNodeFeedMeta,
      'ZH.ui.VoteBar': ZNodeVote,
      'ZH.ui.CommentList': ZNodeCommentList,
      'ZH.ui.Comment': ZNodeComment,
      'ZH.ui.AnswerMeta': ZNodeAnswerMeta,
      'ZH.ui.Answer': ZNodeAnswer,
      'ZH.ui.AnswerListHeader': ZNodeAnswerListHeader,
      'ZH.ui.MoreButton': ZNodeMoreButton,
      'ZH.ui.FeedItem':ZNodeFeedItem
    }
    
    # NOTE: could be a dic.
    if isinstance(meta_data, basestring):
      meta_data = cls.deserialize_meta(meta_data)
  
    if node_name in nodes.keys():
      node_ = nodes[node_name]
      if not node_:
        # TODO: Error handling, can't identify component type.
        pass
        
      instance = node_(handler, meta = meta_data)
      if instance_identity:
        instance.set_client_id(instance_identity)
         
      return instance
    
        
  def get_response(self, handler):
    pagelets = []

    for q in self.queries_:
      # t: type_string, i: instance_identity, m: meta_data, r: render_position, rf: ref element, rt: reder type
      #NOTE: whether update or create new node, this instance should always be trit as root element.
      instance = LiveQueryProcessor.create_node(CLIENT_TYPE_REVERSE_MAP[q['t']], q['i'], q["m"], handler)
      
      # NOTE: no need to set as root node, see also: 2012-11-17's notes on ever note.
      #instance.set_root_node()
      pl = Pagelet(instance)
      # NOTE: default is to update current component.
      if not 'rt' in q.keys():
        pl.set_render_type(PAGELET_RENDER_TYPE.UPDATING)
      else:
        pl.set_render_type(q['rt'])
        
      
      if 'rf' in q.keys():
        pl.set_ref_element(q['rf'])
      
      if 'r' in q.keys():
        pl.set_render_position(q['r'])
      
      pagelets.append(pl)
      
    result = AjaxResponse(handler.get_parents_map())
    result.pagelets = pagelets

    return result
          
    # if not self.result_:
    # 
    #   self.result_ = result
    #     
    # return self.result_  
      
      
      
      