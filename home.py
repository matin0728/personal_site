import webapp2
from google.appengine.api import users
from shared import *


class HomeHandler(BaseHandler):
  def get(self):
    # self.response.out.write("This is Home page.<br /><br />")
    # self.response.out.write('<a href="/question/1">First Question</a><br /><br />')
    # self.response.out.write('<a href="/question/add">Add question!!</a>')
    view_data = {
      'your_name': "martin0728"
    }
    self.render('home.html', view_data)


app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=HomeHandler, name='home')
], debug = SITE_CONFIG['is_debug'], config=SITE_CONFIG)