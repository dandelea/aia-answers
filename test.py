from knn import knn
import functions
from glossary import get_graphicdesign
import json

from preprocessing import preprocessing

def test_knn(filepath, glossary_path, k=3, test_size=0.25):
	bits = functions.gen_bitlist(6)[1:]

	get_graphicdesign()

	with open(glossary_path, 'r') as outfile:
		glossary = json.load(outfile)

	total = len(bits)*3*5
	max = 0
	max_tags = []
	max_k = 0
	max_parts = 0
	counter = 1
	for tags in bits:
		for i in range(3,6):
			for j in range(3,8):
				matrix, tag_names = preprocessing(filepath, tags, glossary)
				r = knn(matrix)
				print(str(counter) + "/" + str(total), end='\r')
				if r > max:
					max = r
					max_tags = tag_names
					max_k = i
					max_parts = j
				counter += 1
	print("---Mejor---")
	print("Valoracion: " + str(max))
	print("Tag names: " + str(max_tags))
	print("k: " + str(max_k))
	print("parts: " + str(max_parts))



if __name__=='__main__':
	test_knn('files/graphic-design.xml', 'files/glossary_graphicdesign.json')
