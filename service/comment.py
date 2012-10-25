import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from model import *
from singleton import Singleton
from base_service import BaseService

class CommentService(Singleton, BaseService):
  def get_answer_comments(self, question_id, answer_id):
    question = Question.get_by_id(int(question_id))
    answer = Answer.get_by_id(parent = question.key, id = int(answer_id))
    comments = Comment.query(ancestor = answer.key).fetch()
    return comments
    
  def delete_answer_comment(self, question_id, answer_id, comment_id):
    question = Question.get_by_id(int(question_id))
    answer = Answer.get_by_id(parent = question.key, id = int(answer_id))
    self.delete_entity_comment(answer, comment_id)
    
  def add_answer_comment(self, account, question_id, answer_id, content):
    question = Question.get_by_id(int(question_id))
    answer = Answer.get_by_id(parent = question.key, id = int(answer_id))
    self.add_entity_comment(account, answer, content)
    
  def delete_entity_comment(self, entity, comment_id):
    comment = Comment.get_by_id(parent = entity.key, id = int(comment_id))
    if comment:
      comment.key.delete()
      self.update_comment_num(entity)
    
  def add_entity_comment(self, account, entity, content):
    comment = Comment(
      parent = entity.key,
      author = account.key,
      real_author = account.key,
      content = content
    )
    comment.put()
    self.update_comment_num(entity)
    
  def update_comment_num(self, entity):
    count = Comment.query(ancestor = entity.key).count()
    entity.comment_num = count
    entity.put()
    
    
    
    
    
    
    