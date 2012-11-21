# coding=utf-8

import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from model.question import Question
from model.answer import Answer
from model.accountxquestion import AccountXQuestion
from answer import AnswerService
from entity import EntityService
from account_question_relation import *
from singleton import Singleton
from base_service import BaseService
from account_question_relation import *

class QuestionService(Singleton, BaseService):
  def focus_question(self, account_key, question_id):
    self.focus_question_(True, account_key, question_id)
  
  def unfocus_question(self, account_key, question_id):
    self.focus_question_(False, account_key, question_id)
    
  def focus_question_(self, is_focus, account_key, question_id):
    question = Question.get_by_id(int(question_id))
    relation = AccountQuestionRelationService().get_relationship(account_key, question.key)
    relation.focused = is_focus
    relation.put()
    
    
  def update_answer(self, question_id, answer_id, source):
    current_question = Question.get_by_id(int(question_id))
    if not current_question:
      return
      
    answer = Answer.get_by_id(int(answer_id), parent = current_question.key)
    #TODO: raise 404 error.
    if not answer:
      return
    
    #TODO: filter desc content using hlper method.
    content = source.replace("\n", "<br />")
    
    answer.content = content
    answer.source = source

    answer.put()
      
      
  def add_answer(self, question_id, source, author):
    question = Question.get_by_id(int(question_id))
    if not question or not source:
      self.set_error_code(500)
      return
    
    #TODO: if answer is added by anonymouse, author should be set to None, 
    #      real_author is always set.(eg. question_relationship = get_relationshiop(question))
    
    new_answer = Answer(
      parent = question.key, 
      summary = source[0:100], 
      question = question.key, 
      author = author.key,
      real_author = author.key,
      content = source.replace("\n", "<br />"),
      source = source) 

    new_answer.put()
    
    relation = AccountQuestionRelationService().get_relationship(author.key, question.key)
    relation.my_answer = new_answer.key
    relation.put()
    QuestionService().update_answer_num(question.key)
    return new_answer
      
  def update_answer_num(self, question_key):
    question = question_key.get()
    if question:
      answers_num = Answer.query(ancestor=question_key).count()
      question.answers_num = answers_num
      question.put()
      
  def remove_answer_from_question(self, question_id, answer_id):
    question = Question.get_by_id(int(question_id))
    if not question:
      return
      
    answer = Answer.get_by_id(int(answer_id), parent = question.key)
    if not answer:
      return

    answer.key.delete()
    self.update_answer_num(question.key)
    return question
    
  def delete_question(self, question_id):
    question = Question.get_by_id(int(question_id))
    if not question:
      return
      
    question.key.delete()
    
    
    
    
    
    
    

