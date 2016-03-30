import itertools

def gen_bitlist(length):
	bits = []
	for j in itertools.product('01', repeat=length):
		bit = []
		for i in j:
			bit.append(int(i))
		bits.append(bit)
	return bits