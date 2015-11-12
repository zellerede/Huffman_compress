
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

	def test_countLetters(self):
		letters = H.countLetters(text)
		for x,weight in letters.items():
			print "%r:%s\t\t" %(x,weight),
		print
		H.getCodes(letters)
		for x in text: print H.codes[x],
		#encoded = sum([H.codes[x] for x in text], H.Bitarray())
		#print encoded

text = '''
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
'''



if __name__ == '__main__':
    unittest.main()
