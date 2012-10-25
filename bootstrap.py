# coding=utf-8

import webapp2
from google.appengine.api import users
from shared import *
from question import *
from answer import *
from home import *

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=HomeHandler, name='home'),    
    webapp2.Route(r'/question/<question_id:\d+>', handler=QuestionHandler, name="question"),
    webapp2.Route(r'/question/<question_id:\d+>/edit', handler=QuestionEditHandler, name="question.edit"),
    webapp2.Route(r'/question/<question_id:\d+>/delete', handler=QuestionDeleteHandler, name="question.delete"),
    webapp2.Route(r'/question/<question_id:\d+>/add_answer', handler=QuestionAddAnswerHandler, name="question.add_answer"),
    webapp2.Route(r'/question/<question_id:\d+>/focus', handler=QuestionFocusHandler, name="question.focus"),
    webapp2.Route(r'/question/<question_id:\d+>/unfocus', handler=QuestionUnFocusHandler, name="question.unfocus"),
    
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/edit', handler=AnswerEditHandler, name="answer.edit"),
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/delete', handler=AnswerDeleteHandler, name="answer.delete"),
    
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/voteup', handler=AnswerVoteUpHandler, name="answer.vote_up"),
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/votedown', handler=AnswerVoteDownHandler, name="answer.vote_down"),
    
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/thanks', handler=AnswerThanksHandler, name="answer.thanks"),
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/nohelp', handler=AnswerNoHelpHandler, name="answer.nohelp"),
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/cancel_nohelp', handler=AnswerCancelNoHelpHandler, name="answer.cancel_nohelp"),

    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/comment/<comment_id:\d+>/delete', handler=AnswerCommentDeleteHandler, name="answer.comment.delete"),    
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/comment_list', handler=AnswerCommentListHandler, name="answer.comment.list"),
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/add_comment', handler=AnswerAddCommentHandler, name="answer.comment.add"),
    
    webapp2.Route(r'/question/add', handler=QuestionAddHandler, name="question.add"),
    webapp2.Route(r'/signup', handler=SignupHandler, name='signup'),
    webapp2.Route(r"/update_modal", handler=ModalUpdateHandler),
], debug = SITE_CONFIG['is_debug'], config=SITE_CONFIG)