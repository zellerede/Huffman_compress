
BITS = [1<<n for n in range(8)]

class Bitstream(object):
	def __init__(self, bytes=[], length=None):
		self.bytes = bytearray(bytes)
		if length is None:
			length = len(bytes) * 8
		self.len = length
		byteLen = length/8 + (1 if length%8 else 0)
		diff = byteLen - len(self.bytes)
		if diff > 0:
			self.bytes += bytearray([0]*diff)
		elif diff < 0:
			self.bytes = self.bytes[:byteLen]
	
	def __repr__(self):
		return '0b' + ''.join( str(self[i]) 
		                         for i in range(self.len) )
	
	def _shifted(self, bits):
		' bits expected to be between 1 and 7 '
		bits %= 8
		if bits==0: 
			return self.bytes[:]
		bytes = [byte >>bits for byte in self.bytes]
		bytes.append(self.bytes[-1] <<(8-bits))
		return bytes
	
	def __add__(self, other):
		bytes = self.bytes[:]
		shift = self.len % 8
		shifted = other._shifted(shift)
		if shift:
			bytes[-1] &= (BITS[shift]-1)
			bytes[-1] |= shifted[0]
		bytes += shifted
		return Bitstream(bytes, self.len + other.len)
	
	def __
	
	def __getitem__(self, idx):
		n = idx/8
		bit = idx % 8
		return (1 if (self.bytes[n] & BITS[bit])
		          else 0)
	
