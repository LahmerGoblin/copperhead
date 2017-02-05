#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import codecs
import zipfile
from IPython import embed
# Cross Validation
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import Pipeline

from sklearn.svm import SVC

import re

filename = 'metadata_features_train.json'
if len(sys.argv)>1:
    if sys.argv[1] == 'test':
        filename = 'metadata_features_test.json'
        

tweets = json.load(codecs.open(filename,'r'))

X = []
y = []
for id in tweets[0].keys():
    X.append(tweets[0][id])
    y.append(tweets[1][id])

normalizer = Normalizer()
vectorizer = DictVectorizer()
svm = SVC()
feature_map = vectorizer.fit_transform(X)
#pipeline = Pipeline([vectorizer,svm])
embed()
normalized = normalizer.transform(feature_map)

scores = cross_val_score(svm,feature_map, y, cv=5)

print(scores)
print('\n')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
