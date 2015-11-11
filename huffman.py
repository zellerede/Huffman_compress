
from my_bitarray import Bitarray, BIT
from trees import Node, Forest

# Reads the text, evaluates the characters it contains, counting each.
# This will give each used character a  weight.
# According this weighting, calculates Huffman codes for characters,
# finally builds the translation bitstream

# Also, there should be a reading for each such a (valid) bitstream
#

class HuffmanForest(Forest):
	def __init__(self, weights):
		for x,w in weights.items():
			self.add( Node(x,w) )

	def grow(self, prints=False):
		while self.bloom():
			if prints:  print self

	def bloom(self):
		" the atomic step of forest growing up to a binary tree "
		if len(self)<2:
			return
		self.add( Node( 
		            parentOf=[self.pop(0), self.pop(0)] ) )
		return True
	
	def printLeaves(self):
		for root, path, leaf in self.leaves:
			print leaf, Bitarray(path)

###########################################################################
#
# user interface:
#   getCodes( dict of letters:weights )
#    - calculates the Huffman codes by building a Huffman tree on given
#      weighted letter set
#   readBits( Bitarray )
#    - decodes the given bitarray according to the module variable 'codes'
#   readOne( Bitarray )
#    - reads one symbol according to the module variable 'codes'
#
###########################################################################

codes = {'0':BIT[0], '1':BIT[1]}

def getCodes(weightedLetterSet):
	global codes
	f = HuffmanForest( weightedLetterSet )
	f.grow()
	codes = { leaf.letters:Bitarray(path)
	             for _,path,leaf in f.leaves }
	return codes

def readBits(bits):
	decoded = ''
	while bits:
		decoded += readOne(bits)
	return decoded

def readOne(bits):
	remains = bits[:]
	reading = Bitarray()
	found = None
	try:
		while not found:
			reading.append( bits.pop(0) )
			found = [letter for letter,target in codes.items() 
			                if target==reading]
	except IndexError:
		print "Remaining bits:", remains
	else:
		[letter] = found # should contain 1 element exactly
		return letter
