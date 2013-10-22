# coding=utf-8

from shared import node

class TestNode2(node.ZNode):
	constructor_name = 'TestNode2'
	js_path = 'test_node_2.js'
	template = 'test_node_2.html'

class TestNode(node.ZNode):
	constructor_name = 'TestNode'
	js_path = 'test_node.js'
	template = 'test_node.html'

	def fetch_data(self):
		self.set_view_data_item('render_test_node_2', self.render_test_node_2())

	def render_test_node_2(self):
		node2 = TestNode2(meta = {'a':1}, parent_node = self)
		# important step.
		self.add_child(node2)
		return node2.render()


