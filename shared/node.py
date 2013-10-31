# coding=utf-8

import os
import time, datetime
import json
import webapp2
import node_renderer
import vendor.znode as znode
import app_config

class ZNode(znode.ZNode):
  def render(self):
    self.set_view_data_item('uri_for', webapp2.uri_for)
    self.set_view_data_item('config', app_config.SITE_CONFIG)

    return super(ZNode, self).render()

  def get_renderer(self, template = '', view_data = None):
    return node_renderer.NodeRenderer(template, view_data)