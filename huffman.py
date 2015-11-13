
from collections import defaultdict

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
		            parentOf=[self.popHead, self.popHead] ) )
		return True
	
	@property
	def popHead(self):
		return self.pop(0)
	
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
#   decode = readBits
#   encode( text )
#    - encodes the text to Bitarray using module's current 'codes'
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
	if bits.len==0:
		# raise Exception('No bits to read.')
		return
	remains = bits[:]
	reading = Bitarray()
	found = None
	try:
		while not found:
			reading.append( bits.popHead )
			found = [letter for letter,target in codes.items() 
			                if target==reading]
	except IndexError:
		print "Remaining bits:", remains
	else:
		[letter] = found # should contain 1 element exactly
		return letter

decode = readBits

def encode(text, weights=None, keepCodes=False):
	'''
	   If keepCodes==True, the current 'codes' is preserved, and the
	   used codes are returned together with the encoded value:
	     return (encoded, codes)
	   Otherwise module's variable 'codes' is replaced and only 
	   the encoded Bitarray is returned.'''
	global codes
	if keepCodes:
		codes_saved = codes.copy()
	if weights is None:
		weights = countLetters(text)
		getCodes(weights)
	encoded = sum([codes[x] for x in text], Bitarray.EMPTY)
	if keepCodes:
		encoded = (encoded, codes)
		codes = codes_saved
	return encoded


#########################################
#
def countLetters(text):
#########################################
	# later to handle looong bytestreams
	letters = defaultdict(lambda:0)
	for c in text:
		letters[c] += 1
	return letters
