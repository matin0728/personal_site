import webapp2
from google.appengine.api import users


class AdminMainPage(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      
      self.response.out.write('Your are admin!!!')
          
app = webapp2.WSGIApplication([('/admin.*', AdminMainPage)],
                            debug=True)

