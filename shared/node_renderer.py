# coding=utf-8

# import webapp2
import jinja2
import os
import time, datetime
import json
from vendor.znode import zh_node_default_renderer

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__) + '/../templates')))

class NodeRenderer(zh_node_default_renderer.ZNodeDefaultRenderer):
  def render(self):
    template = jinja_environment.get_template(self.template)
    return template.render(self.view_data)