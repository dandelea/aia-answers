import argparse
import functions
import math

from glossary import get_chemistry, get_graphicdesign
from knn import knn
from logistic_regression import logistic_regression
from preprocessing import preprocessing

def test_knn(filepath, glossary, k=5):
	bits = functions.gen_bitlist(6)[1:]

	total = len(bits)
	max = 0
	max_tags = []
	counter = 1
	for tags in bits:
		matrix, tag_names = preprocessing(filepath, tags, glossary)
		r = knn(matrix, k)
		print(str(counter) + "/" + str(total), end='\r')
		if r > max:
			max = r
			max_tags = tag_names
		counter += 1
	print("---Mejor---")
	print("Valoracion: " + str(max))
	print("Tag names: " + str(max_tags))

def test_logistic(filepath, glossary):
	bits = functions.gen_bitlist(6)[1:]

	total = len(bits)
	max = 0
	max_tags = []
	max_k = 0
	counter = 1
	for tags in bits:
		matrix, tag_names = preprocessing(filepath, tags, glossary)
		r = logistic_regression(matrix)
		print(str(counter) + "/" + str(total), end='\r')
		if r > max:
			max = r
			max_tags = tag_names
		counter += 1
	print("---Mejor---")
	print("Valoracion: " + str(max))
	print("Tag names: " + str(max_tags))

def run(source, method, k):
	if method=='knn' and k is None:
		raise ValueError('Argument k is mandatory for KnnClassifier')
	else:
		if source=='chemistry':
			glossary = get_chemistry()
			filepath = 'files/chemistry.xml'
		else:
			glossary = get_graphicdesign()
			filepath = 'files/graphic-design.xml'

		if method=='knn':
			k = int(math.fabs(int(k) or 5))
			test_knn(filepath, glossary, k)
		else:
			test_logistic(filepath, glossary)

if __name__=='__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-s", "--source", required=True, choices=[
                    'chemistry', 'graphic-design'],
                    help="Data source used: Chemistry /\
                     Graphic design")
	ap.add_argument("-m", "--method", required=True, choices=[
					'knn', 'logistic'],
					help="Classifier method")
	ap.add_argument("-k", "--k", required=False,
					help="k neighbours")
	args = vars(ap.parse_args())
	run(args['source'], args['method'], args['k'])
