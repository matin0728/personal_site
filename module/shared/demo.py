import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from model.question import *
from model.answer import *
from shared.znode import ZNode
# from service.feed import FeedService
# from service.entity import EntityService
# from service.question import QuestionService

class DemoNode(ZNode):
  template_ = 'demo_node.html'
    
  def fetch_data_internal(self):
    pass
    
  def fetch_data(self):
    pass