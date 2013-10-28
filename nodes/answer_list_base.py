# import webapp2
# import jinja2
import os
from google.appengine.ext import ndb
import model
import service
import nodes
import shared

# class AnswerListHeader(sharedZNode):
#   template_ = 'answer_list_header.html'
#   client_type = 'ZH.ui.AnswerListHeader'
#   # meta = {
#   #   'question_id',
#   # }
  
#   # view_data = {
#   #   'question',
#   # }

#   def __init__(self, meta = {}):
#     self.template = 'question_page.html'
#     self.js_path = 'question_page'
#     #TODO: merge options.
#     # meta['page_url'] = '/question/' + meta['question_id']
#     super(QuestionPage, self).__init__(meta = meta)

#   def fetch_data_internal(self):
#     question = model.Question.get_by_id(int(self.get_meta('question_id')))
#     self.set_view_data_item('question', question)
    
#   def fetch_data(self):
#     question = self.get_view_data_item('question')
#     if not question:
#       self.fetch_data_internal()

class AnswerListBase(shared.ZNode):
  #NOTE: Why we call this "ListBase"? This collapsed answerlist is another type of answer list
  # and it will only need to override the fetch data method and has another client name.
  
  # meta should contains following data.
  # meta = {
  #   'question_id',
  # }
  
  # view_data should contains(at least) following field.
  # view_data = {
  #  'answers' : []
  #  'relation' : None
  #  'question': None, question entity.
  # }
  # 

  def __init__(self, meta = {}, parent_node = None):
    super(AnswerListBase, self).__init__(meta = meta, parent_node = parent_node)
    self.template = 'answer_list.html'
    self.js_path = 'answer_list'
    #TODO: merge options.
    # meta['page_url'] = '/question/' + meta['question_id']
  
  def render_answer(self, answer_key, relation):
    meta = {
      'answer_id': answer_key.id(),
      'hide_answer_meta': 0
    }
    a = nodes.Answer(meta = meta, parent_node = self)
    a.set_view_data_item('answer', service.EntityService().get(answer_key))
    a.set_view_data_item('relation', relation)
    return a.render()
  
  def fetch_data_internal(self):
    pass
    # self.set_meta('node_name', 'ZNodeAnswerListBase')
    
  def fetch_data(self):
    question = self.get_view_data_item('question')
    if not question:
      question = model.Question.get_by_id(int(self.get_meta('question_id')))
      self.set_view_data_item('question', question)
      
    # relation = self.get_view_data_item('relation')
    # if not relation:
    #   relation = service.AccountQuestionRelationService().get_relationship(self.get_handler().get_current_account().key, question.key)
    #   self.set_view_data_item('relation', relation)
    
    answers = self.get_view_data_item('answers')
    if not answers:
      self.fetch_data_internal()
     
    answer_ids = self.get_view_data_item('answers')
    # Batch fetch entity!!
    service.EntityService().get_multi(answer_ids)
    
    self.set_view_data_item('render_answer', self.render_answer)
    
class ZNodeAnswerList(ZNodeAnswerListBase):  
  def fetch_data_internal(self):
    # add a extra name for this component, in future, there will be another answer list
    # whos name is collapsed_answers
    # 'instance_name': 'normal_answers'
    self.set_meta('instance_name', 'normal_answers')
    
    question = self.get_view_data_item('question')
    answers = service.AnswerService().get_answers_by_question_key(question.key, keys_only = True)
    
    # self.get_handler().response.out.write(answers)
    # self.set_view_data_item('answers', [])
    # return
    self.set_view_data_item('answers', answers)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    