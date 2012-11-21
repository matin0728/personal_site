# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from model.answer import Answer
from model.question import Question
from model.accountxquestion import AccountXQuestion
from singleton import Singleton
from base_service import BaseService
from account_question_relation import *
from entity import EntityService

class AnswerService(Singleton, BaseService):
  def votedown_answer(self, actor, question_id, answer_id):
    question = Question.get_by_id(int(question_id))
    answer = Answer.get_by_id(parent = question.key, id = int(answer_id))
    relation = AccountQuestionRelationService().get_relationship(actor.key, question.key)
    if answer.key in relation.down_voted_answers:
      relation.down_voted_answers = [ a for a in relation.down_voted_answers if a != answer.key ]
      answer.down_voted_users = [ u for u in answer.up_voted_users if u != actor.key ]
    else:
      relation.down_voted_answers.append(answer.key)
      answer.down_voted_users.append(actor.key)
      
    #remove from upvoted.  
    relation.up_voted_answers = [ a for a in relation.up_voted_answers if a != answer.key ]
    answer.up_voted_users = [ u for u in answer.up_voted_users if u != actor.key ]
    answer.put()
    relation.put()
    
  def voteup_answer(self, actor, question_id, answer_id):
    question = Question.get_by_id(int(question_id))
    answer = Answer.get_by_id(parent = question.key, id = int(answer_id))
    relation = AccountQuestionRelationService().get_relationship(actor.key, question.key)
    if answer.key in relation.up_voted_answers:
      relation.up_voted_answers = [ a for a in relation.up_voted_answers if a != answer.key ]
      answer.up_voted_users = [ u for u in answer.up_voted_users if u != actor.key ]
    else:
      relation.up_voted_answers.append(answer.key)
      answer.up_voted_users.append(actor.key)
      
    relation.down_voted_answers = [ a for a in relation.down_voted_answers if a != answer.key ]
    answer.down_voted_users = [ u for u in answer.down_voted_users if u != actor.key ]
    answer.put()
    relation.put()
    
  def thanks_for_answer(self, actor, question_id, answer_id):
    question = Question.get_by_id(int(question_id))
    answer = Answer.get_by_id(parent = question.key, id = int(answer_id))
    relation = AccountQuestionRelationService().get_relationship(actor.key, question.key)
    if not answer.key in relation.thanksed_answers:
      relation.thanksed_answers.append(answer.key)
      
    relation.put()
    
  def set_no_help(self, actor, question_id, answer_id):
    question = Question.get_by_id(int(question_id))
    answer = Answer.get_by_id(parent = question.key, id = int(answer_id))
    relation = AccountQuestionRelationService().get_relationship(actor.key, question.key)
    if not answer.key in relation.no_help_answers:
      relation.no_help_answers.append(answer.key)
    
    relation.put()
    
  def cancel_no_help(self, actor, question_id, answer_id):
    question = Question.get_by_id(int(question_id))
    answer = Answer.get_by_id(parent = question.key, id = int(answer_id))
    relation = AccountQuestionRelationService().get_relationship(actor.key, question.key)
    relation.no_help_answers = [ a for a in relation.no_help_answers if a != answer.key ]
    relation.put() 
    
  def get_answers_by_question_key(self, question_key, keys_only = True):
    answers = Answer.query(ancestor = question_key).fetch(keys_only = keys_only)
    return answers

  def get_answers_by_question_id(self, question_id):
    #don't need call entity service for single get operation
    question = Question.get_by_id(int(question_id))
    answers = Answer.query(ancestor = question.key).fetch()
    return answers
    
    
    
    
  