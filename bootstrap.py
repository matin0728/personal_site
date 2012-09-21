# coding=utf-8

import webapp2
from google.appengine.api import users
from shared import *
from question import *
from answer import *
from home import *

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=HomeHandler, name='home'),
    webapp2.Route(r'/answer/<answer_id:\d+>/edit', handler=AnswerEditHandler, name="answer.edit"),
    webapp2.Route(r'/answer/<answer_id:\d+>/delete', handler=AnswerDeleteHandler, name="answer.delete"),
    
    webapp2.Route(r'/question/<question_id:\d+>', handler=QuestionHandler, name="question"),
    webapp2.Route(r'/question/<question_id:\d+>/edit', handler=QuestionEditHandler, name="question.edit"),
    webapp2.Route(r'/question/<question_id:\d+>/delete', handler=QuestionDeleteHandler, name="question.delete"),
    webapp2.Route(r'/question/<question_id:\d+>/add_answer', handler=QuestionAddAnswerHandler, name="question.add_answer"),
    webapp2.Route(r'/question/add', handler=QuestionAddHandler, name="question.add"),
    
    webapp2.Route(r"/update_modal", handler=ModalUpdateHandler),
], debug = SITE_CONFIG['is_debug'], config=SITE_CONFIG)