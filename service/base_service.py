# coding=utf-8

class BaseService(object):
  def __init__(self):
    super(BaseService, self).__init__()
    self.error_msg = {"r":1, "msg":"server error.", "code":0}
    
  def get_last_error(self):
    return self.error_msg
  
  def set_error_message(self, msg):
    self.error_msg["msg"] = msg
  
  def set_error_code(self, code):
    self.error_msg["code"] = code