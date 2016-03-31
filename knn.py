import numpy as np

from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def knn(matrix, k=3, validation_parts=5):
	X = matrix[:,:-1]
	y = matrix[:,-1]

	kfold5 = KFold(X.shape[0], validation_parts, shuffle = True)

	model = Pipeline([('normalizador', StandardScaler()), ('knnpredictor', KNeighborsClassifier(n_neighbors=k))])

	valores = cross_val_score(model, X, y, cv=kfold5)

	return np.mean(valores)