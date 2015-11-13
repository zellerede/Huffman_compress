
import unittest

import my_bitarray as B

class TestBitarray(unittest.TestCase):
	def test_equalities(self):
		self.assertEqual( B.Bitarray(),
		                  B.Bitarray(bytes=[28],length=0) )
		self.assertEqual( B.Bitarray([1,1,1,1,0]),
		                  B.Bitarray(bytes=[15+128,255], length=5) )

	def test_add(self):
		a = B.Bitarray(bytes=[15+128,255], length=5)
		b = B.Bitarray([0,0,0,1,1])
		self.assertEqual( a+b,
		                  B.Bitarray([1,1,1,1,0, 0,0,0,1,1]) )


if __name__ == '__main__':
	unittest.main(exit=False)

