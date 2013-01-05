# coding=utf-8

import webapp2
from google.appengine.api import users
from shared import *
from question import *
from answer import *
from home import *
from comment import *
from settings import *

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=HomeHandler, name='home'),
    webapp2.Route(r'/myquestion', handler=HomeMyQuestionHandler, name='home.myquestion'),
    
    webapp2.Route(r'/magic_node', handler=NodeHandler, name='node'),
    
    webapp2.Route(r'/question/<question_id:\d+>', handler=QuestionHandler, name="question"),
    webapp2.Route(r'/question/<question_id:\d+>/edit', handler=QuestionEditHandler, name="question.edit"),
    webapp2.Route(r'/question/<question_id:\d+>/delete', handler=QuestionDeleteHandler, name="question.delete"),
    webapp2.Route(r'/question/<question_id:\d+>/add_answer', handler=QuestionAddAnswerHandler, name="question.add_answer"),
    webapp2.Route(r'/question/<question_id:\d+>/focus', handler=QuestionFocusHandler, name="question.focus"),
    webapp2.Route(r'/question/<question_id:\d+>/unfocus', handler=QuestionUnFocusHandler, name="question.unfocus"),
    webapp2.Route(r'/question/<question_id:\d+>/bind', handler=QuestionBindTopicHandler, name="question.bind_topic"),
    webapp2.Route(r'/question/<question_id:\d+>/unbind', handler=QuestionUnBindTopicHandler, name="question.un_bind_topic"),
    
    
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>', handler=AnswerHandler, name='answer'),
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/edit', handler=AnswerEditHandler, name="answer.edit"),
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/delete', handler=AnswerDeleteHandler, name="answer.delete"),
    
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/voteup', handler=AnswerVoteUpHandler, name="answer.vote_up"),
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/votedown', handler=AnswerVoteDownHandler, name="answer.vote_down"),
    
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/thanks', handler=AnswerThanksHandler, name="answer.thanks"),
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/nohelp', handler=AnswerNoHelpHandler, name="answer.nohelp"),
    webapp2.Route(r'/question/<question_id:\d+>/answer/<answer_id:\d+>/cancel_nohelp', handler=AnswerCancelNoHelpHandler, name="answer.cancel_nohelp"),

    webapp2.Route(r'/comment/delete/<comment_key_string:[^/]+>', handler=CommentDeleteHandler, name="comment.delete"),    
    webapp2.Route(r'/comment/list/<entity_key_string:[^/]+>', handler=CommentListHandler, name="comment.list"),
    webapp2.Route(r'/comment/add/<entity_key_string:[^/]+>', handler=AddCommentHandler, name="comment.add"),
    
    webapp2.Route(r'/question/add', handler=QuestionAddHandler, name="question.add"),
    webapp2.Route(r'/signup', handler=SignupHandler, name='signup'),
    
    webapp2.Route(r'/settings/account', handler=SettingsAccountHandler, name='settings.account'),
    webapp2.Route(r'/settings/notify', handler=SettingsNotifyHandler, name='settings.notify'),
    webapp2.Route(r'/settings/email', handler=SettingsEmailHandler, name='settings.email'),
    webapp2.Route(r'/settings/bind', handler=SettingsBindHandler, name='settings.bind'),
    webapp2.Route(r'/settings/blockuser', handler=SettingsBlockUserHandler, name='settings.blockuser'),
    
    webapp2.Route(r"/update_modal", handler=ModalUpdateHandler),
    # For test purpose only
    webapp2.Route(r"/test", handler=TestHandler, name="test")
], debug = SITE_CONFIG['is_debug'], config=SITE_CONFIG)


