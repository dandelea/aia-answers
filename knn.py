from preprocessing import preprocessing
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from preprocessing import preprocessing
import functions
import glossary
import json


def knn(matrix, k=3, test_size=0.25, validation_parts=5):
	neigh = KNeighborsClassifier(n_neighbors=k)
	X = matrix[:,:-1]
	y = matrix[:,-1]

	kfold5 = KFold(X.shape[0], validation_parts, shuffle = True)

	model = Pipeline([('normalizador', StandardScaler()), ('knnpredictor', KNeighborsClassifier(n_neighbors=k))])

	valores = cross_val_score(model, X, y, cv=kfold5)

	return np.mean(valores)

if __name__=='__main__':
	filepath = 'files/graphic-design.xml'
	glossary_path = 'files/glossary_graphicdesign.json'
	glossary.get_graphicdesign()
	with open(glossary_path, 'r') as outfile:
		glossary = json.load(outfile)
	matrix = preprocessing(filepath, [1,1,1,1,1,1], glossary)
	print("Finish preprocessing")
	r = knn(matrix)
	print(np.mean(r))