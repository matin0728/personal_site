# coding=utf-8

import jinja2
import os
import time, datetime
import json
import vendor.znode as znode

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__) + '/../templates')))

class NodeRenderer(znode.ZNodeDefaultRenderer):
  def render(self):
    template = jinja_environment.get_template(self.template)
    return template.render(self.view_data)