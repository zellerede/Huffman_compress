
import bisect # to realize SortedList
from collections import OrderedDict as Dict

from my_bitarray import Bitarray

# Reads the text, evaluates the characters it contains, counting each.
# This will give each used character a  weight.
# According this weighting, calculates Huffman codes for characters,
# finally builds the translation bitstream

# Also, there should be a reading for each such a (valid) bitstream
#

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
	def walk(self):
		if self.isLeaf:
			yield self, []
			return
		x = 0
		for child in self.children:
			for leaf, path in child.walk:
				yield leaf, [x]+path
			x += 1
			

class Forest(list): 
	''' Forest of Nodes which are roots of a (letter-weight) tree '''
	def append(self, obj):
		bisect.insort(self, obj)
	add = append
	
	def __init__(self, arg=[]):
		if isinstance(arg, dict):
			for x,w in arg.items():
				self.add( Node(x,w) )
		else:
			list.__init__(self, arg)

	def grow(self):
		while self.bloom():
			print self
			pass
	def bloom(self):
		" the atomic step of forest growing up to a binary tree "
		if len(self)<2:
			return
		self.add( Node( 
		            parentOf=[self.pop(0), self.pop(0)] ) )
		return True
	
	def find_leaves(self):
		for root in self:
			for leaf, path in root.walk:
				print leaf, Bitarray(path)

# incoming parameter _letters, say:
_letters = {'a':15,'b':4,'c':5,'d':8,'e':2}

f = Forest( _letters )
f.grow()
print
f.find_leaves()
