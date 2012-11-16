import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from model import *
from singleton import Singleton
from base_service import BaseService

class CommentService(Singleton, BaseService):
  def get_comments(self, entity_key_string):
    key = ndb.Key(urlsafe = entity_key_string)
    comments = Comment.query(ancestor = key).fetch()
    return comments
    
  def delete_comment(self, comment_key_string):
    key = ndb.Key(urlsafe = comment_key_string)
    entity_key = key.parent()
    key.delete()
    self.update_comment_num(entity_key)
    
  def add_comment(self, account, entity_key, content):
    # TODO: Check anonymouse status for user on question.
    # anonymouse user couldn't comment, except the question author or answer author.
    parent_key = ndb.Key(urlsafe = entity_key)
    comment = Comment(
      parent = parent_key,
      author = account.key,
      real_author = account.key,
      content = content
    )
    comment.put()
    self.update_comment_num(entity_key)
    
  def update_comment_num(self, entity_key):
    count = Comment.query(ancestor = entity_key).count()
    entity.comment_num = count
    entity.put()
    
    
    
    # def get_question_comments(self, question_id):
    #      question = Question.get_by_id(int(question_id))
    #      return self.get_entity_comments(question)
    # 
    #    def delete_answer_comment(self, question_id, comment_id):
    #      question = Question.get_by_id(int(question_id))
    #      self.delete_entity_comment(question, comment_id)
    # 
    #    def add_answer_comment(self, account, question_id, content):
    #      question = Question.get_by_id(int(question_id))
    #      self.add_entity_comment(account, question, content)
    # 
    # 
    #    def get_answer_comments(self, question_id, answer_id):
    #      question = Question.get_by_id(int(question_id))
    #      answer = Answer.get_by_id(parent = question.key, id = int(answer_id))
    #      return self.get_entity_comments(answer)
    # 
    #    def delete_answer_comment(self, question_id, answer_id, comment_id):
    #      question = Question.get_by_id(int(question_id))
    #      answer = Answer.get_by_id(parent = question.key, id = int(answer_id))
    #      self.delete_entity_comment(answer, comment_id)
    # 
    #    def add_answer_comment(self, account, question_id, answer_id, content):
    #      question = Question.get_by_id(int(question_id))
    #      answer = Answer.get_by_id(parent = question.key, id = int(answer_id))
    #      self.add_entity_comment(account, answer, content)
    #    
    #    
    #    