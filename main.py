import argparse
import math

from glossary import get_graphicdesign, get_chemistry
from knn import knn
from logistic_regression import logistic_regression
from preprocessing import preprocessing

def run(source, method, k):
	tags = [1,1,1,1,1,1]
	if method=='knn' and k is None:
		raise ValueError('Argument k is mandatory for KnnClassifier')
	else:
		if source=='chemistry':
			if tags[5]:
				glossary = get_chemistry()
			else:
				glossary = None
			filepath = 'files/chemistry.xml'
		else:
			if tags[5]:
				glossary = get_graphicdesign()
			else:
				glossary = None
			filepath = 'files/graphic-design.xml'
			
		matrix, tag_names = preprocessing(filepath, tags, glossary)

		print(tag_names)

		if method=='knn':
			k = int(math.fabs(int(k) or 5))
			r = knn(matrix, k)
		else:
			r = logistic_regression(matrix)

		print(r)


if __name__=="__main__":
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