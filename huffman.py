
#from bisect import insort as insert
from collections import OrderedDict as Dict

# Reads the text, evaluates the characters it contains, counting each.
# This will give each used character a  weight.
# According this weighting, calculates Huffman codes for characters,
# finally builds the translation bitstream

# Also, there should be a reading for each such a (valid) bitstream
#

# incoming parameter _letters, say:
_letters = {'a':15,'b':4,'c':5,'d':8,'e':2}
# create a sorted dict for work
letters = Dict()
for x in sorted(_letters, key=_letters.get):
	letters[x] = _letters[x]

while len(letters) > 1:
	# melt the two least frequent
	char = ''
	weight = 0
	for i in range(2):
		ch, w = letters.popitem(0)
		char += ch
		weight += w
