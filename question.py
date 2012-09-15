import webapp2
from google.appengine.api import users
from shared import *

class QuestionHandler(webapp2.RequestHandler):
  def get(self, question_id):
    self.response.out.write('This is question page.')
      
class AddQuestionHandler(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('Add question page.')
    
  def post(self):
    self.response.out.write('You post the form.')


app = webapp2.WSGIApplication([
    webapp2.Route(r'/question/add', handler=AddQuestionHandler, name="add_question"),
    webapp2.Route(r'/question/<question_id:\d+>', handler=QuestionHandler, name="question")
], debug = SITE_CONFIG['is_debug'], config=SITE_CONFIG)