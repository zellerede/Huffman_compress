
def neighbors(iterable):
	it = iter(iterable)
	a = next(it)
	
	for b in it:
	  yield a,b
	  a=b
