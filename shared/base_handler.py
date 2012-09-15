import webapp2
import jinja2
import os
from google.appengine.api import users


class BaseHandler(webapp2.RequestHandler):
  def get_template_environment(self):
    jinja_environment = jinja2.Environment(
      loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__) + '/../templates')))
    return jinja_environment
        
  def render(self, template_name, template_values):
    env = self.get_template_environment()
    template = env.get_template(template_name)
    self.response.out.write(template.render(template_values))
    