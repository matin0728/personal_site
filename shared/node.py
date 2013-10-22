# coding=utf-8

import os
import time, datetime
import json
from shared import node_renderer
from vendor.znode import zh_node

class ZNode(zh_node.ZNode):
  def get_renderer(self, template = '', view_data = None):
    return node_renderer.NodeRenderer(template, view_data)