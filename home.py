import webapp2
from google.appengine.api import users
from shared import *
from model.question import Question
from service import answer as AnswerService

class HomeHandler(BaseHandler):
  def get(self):
    question_list = Question.query().fetch()
    context = {
      'question_list': question_list
    }
    self.render('home.html', context)

class ModalUpdateHandler(BaseHandler):
  def get(self):
    questions = Question.query().fetch()
    for q in questions:
      answers = AnswerService.get_answers_by_question(q.key)
      q.answers_num = len(answers)
      q.put()
      for a in answers:
        a.author = users.get_current_user()
        a.put()
      
    self.response.out.write("Update complete!")


# app = webapp2.WSGIApplication([
#     webapp2.Route(r'/', handler=HomeHandler, name='home'),
# 
#     # webapp2.Route(r'/question/<question_id:\d+>', handler=QuestionHandler, name="question"),
#     # webapp2.Route(r'/question/<question_id:\d+>/edit', handler=QuestionEditHandler, name="question.edit")
#     # webapp2.Route(r'/question/add', handler=AddQuestionHandler, name="question.add"),
# ], debug = SITE_CONFIG['is_debug'], config=SITE_CONFIG)