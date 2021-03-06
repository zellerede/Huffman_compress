
from neighbors import neighbors

_BIT_PLACES = [1<<n for n in range(8)]
_CLEAR_BITS = [255-bitPlace for bitPlace in _BIT_PLACES]

# auxiliary functions
def _divide(idx):
	return (idx/8, idx % 8)


#########################
#
class Bitarray(object):
#########################
	def __init__(self, bits=[], bytes=[], length=None):
		if bits:
			self._buildByBits(bits)
		else:
			self._buildByBytes(bytes, length)

	def __repr__(self):
		return '0b' + ''.join( str(self[i]) 
		                         for i in range(self.len) )

	def __add__(self, other):
		if self.len == 0:
			return other
		if other.len == 0:
			return self
		bytes = self.bytes[:]
		shift = self.len % 8
		shifted = other._shifted(shift)
		if shift:
			bytes[-1] &= (_BIT_PLACES[shift]-1)
			bytes[-1] |= shifted.pop(0)
		bytes += shifted
		return Bitarray(bytes=bytes, length = self.len + other.len)
	
	def append(self, bit=0):
		if (self.len % 8) == 0:
			self.bytes.append(0)
		last = self.len
		self.len += 1
		self[last] = bit # will call _setitem_(self, last, bit)
	
	def __len__(self):
		return self.len
	
	def __getitem__(self, idx):
		return self._dice(idx, self._getitems_, self._getitem_)

	def __setitem__(self, idx, value):
		self._dice(idx, self._setitems_, self._setitem_, value)
	
	def __eq__(self, other):
		return (self.bytes == other.bytes) and (self.len == other.len)
	
	def __nonzero__(self):
		return bool(self.len)

	def pop(self, idx=-1):
		if self.len==0:
			raise IndexError("pop from empty Bitarray")
		idx = self._handle_negative(idx)
		value = self[idx]
		before = self[:idx]
		after = self[(idx+1):]
		new = before + after
		self._buildByBytes(new.bytes, new.len)
		return value

	@property
	def popHead(self):
		return self.pop(0)

	def _buildByBytes(self, bytes, length):
		self.bytes = bytearray(bytes)
		if length is None:
			length = len(bytes) * 8
		self.len = length
		n, bit = _divide(length)
		byteLen = n + (1 if bit else 0)
		diff = byteLen - len(self.bytes)
		if diff > 0:
			self.bytes += bytearray([0]*diff)
		elif diff < 0:
			self.bytes = self.bytes[:byteLen]
			if bit: 
				self.bytes[-1] &= (_BIT_PLACES[bit]-1)

	def _buildByBits(self, bits):
		self._buildByBytes([],0)
		for bit in bits:
			self.append(bit)
	
	def _shifted(self, bits):
		' bits expected to be between 1 and 7 '
		bits %= 8
		if bits==0: 
			return self.bytes[:]

		_left = lambda byte: byte >> (8-bits)
		_right = lambda byte: (byte << bits) & 255
			
		bytes = [ _right(self.bytes[0]) ]
		bytes += [ _left(byte1) | _right(byte2)
		           for byte1, byte2  in neighbors(self.bytes)]
		bytes += [ _left(self.bytes[-1]) ]
		return bytearray(bytes)

	def _handle_negative(self, idx):
		return (idx  if idx>=0 
		             else  idx+self.len)

	def _handle_slice(self, idx):
		return range( *idx.indices(self.len) )

	# common slice handling for getitem and setitem
	def _dice(self, idx, forSlice, forPlain, *value):
		if isinstance(idx, slice):
			return forSlice( self._handle_slice(idx), *value )
		else:
			return forPlain( self._handle_negative(idx), *value )

	def _getitem_(self, idx):
		n, bit = _divide(idx)
		try:
			return (1 if (self.bytes[n] & _BIT_PLACES[bit])
			          else 0)
		except IndexError as e:
			e.args = ('Bitarray index %s out of range' % idx, )
			raise e
	def _getitems_(self, rng):
		# later should be optimized -> to get on byte level
		req_bits = [self[ie]  for ie in rng]
		return Bitarray(req_bits)

	def _setitem_(self, idx, value):
		n, bit = _divide(idx)
		if value and value!='0':
			self.bytes[n] |= _BIT_PLACES[bit]
		else:
			self.bytes[n] &= _CLEAR_BITS[bit]
	
	def _setitems_(self, rng, valarray):
		raise NotImplementedError()

	def writeBinary(self, filename):
		n, bit = _divide(self.len +3) # 3 bits represent the remainder mod 8
		content = Bitarray(bytes=[bit], length=3) + self
		with open(filename, 'w') as f:
			f.write(content.bytes)

	@staticmethod
	def readBinary(filename):
		# later to handle looong bytestreams
		with open(filename) as f:
			content = bytearray(f.read())
		len8 = len(content)
		bits = Bitarray(content)
		len7 = bits.popHead + 2*bits.popHead + 4*bits.popHead
		if len7: 
			len8 -= 1
		bits.len = 8*len8 + len7 -3
		return bits

# Bitarray constants
_0 = Bitarray(length=1)
_1 = Bitarray(bytes=[1],length=1)
BIT = [_0, _1]

Bitarray.EMPTY = Bitarray()

	