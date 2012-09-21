import webapp2
import jinja2
import os
from google.appengine.api import users


class BaseHandler(webapp2.RequestHandler):
  # @webapp2.cached_property
  def get_template_environment(self):
    jinja_environment = jinja2.Environment(
      loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__) + '/../templates')))
    return jinja_environment
        
  def render(self, template, context=None):
    context = context or {}
    extra_context = {
      'request': self.request,
      'uri_for': self.uri_for
    }

    for key, value in extra_context.items():
      if key not in context:
        context[key] = value
    
    env = self.get_template_environment()
    template = env.get_template(template)
    self.response.out.write(template.render(context))
    