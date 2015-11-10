
import bisect # to realize SortedList
from collections import OrderedDict as Dict

class Node(object):
	def __init__(self, letters='', weight=0, parentOf=[]):
		self.parent = None
		self.children = parentOf
		childletters = ''
		childweights = 0
		for child in self.children:
			if child.parent is not None:
				raise Exception("Node to connect should have no parent.")
			child.parent = self
			childletters += child.letters
			childweights += child.weight

		self.letters = ( letters if letters
		                         else childletters )
		self.weight = ( weight if weight
		                       else childweights )
	
	def __repr__(self):
		return "%s:%s" %(self.letters, self.weight)

	def __lt__(self, other):
		return (self.weight < other.weight)
	
	@property
	def isLeaf(self):
		return not bool(self.children)
	
	@property
	def leaves(self):
		if self.isLeaf:
			yield self, []
			return
		x = 0
		for child in self.children:
			for leaf, path in child.leaves:
				yield leaf, [x]+path
			x += 1
			

class Forest(list): 
	''' Forest of Nodes which are roots of a (letter-weight) tree '''
	def append(self, obj):
		bisect.insort(self, obj)
	add = append
	
	@property
	def leaves(self):
		''' generator yielding  root, path, leaf  triples for each leaf of each tree '''
		for root in self:
			for leaf, path in root.leaves:
				yield root, path, leaf
