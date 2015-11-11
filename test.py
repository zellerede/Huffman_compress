
import unittest

import huffman as H

_letterSet = [
		{'a':15,'b':4,'c':5,'d':8,'e':2},
		{'_':100, 'a':20, 'x':14, 'e':40, 's':28},
]

class TestHuffman(unittest.TestCase):
	def test_grow_forest(self):
		for letters in _letterSet:
			print "\nWeighted letter set:\n%r\n" % letters
			f = H.HuffmanForest( letters )
			f.grow(prints=True)
			print
			f.printLeaves()
		
	def test_decode(self):
		letters = _letterSet[0]
		print H.getCodes(letters)
		s = H.Bitarray([0,1,1,0,1,1,1,0,1,0,1,1,1,1,0,0,0,1,1,0])
		print H.readBits(s)


if __name__ == '__main__':
    unittest.main()
