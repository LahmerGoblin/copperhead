#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pagereader import PageReader

import subprocess
import re
from IPython import embed
from features import osad
from features import mykernel

from sklearn.svm import SVC
from sklearn.feature_extraction import FeatureHasher

import numpy as np

import codecs

train_path = 'train_bin/'
#k = 10
c = 4**0

# get all the different pages
files = str(subprocess.check_output('ls -1 ' + train_path,shell=True))[2:-3].split('\\n')

X = []
y = []
for fil in files:
    with codecs.open(train_path+fil,'rU') as pageFile:
        for i,row in enumerate(pageFile):
            y.append(fil[0:-len('.bin')])
            list_row = list(row[0:-2])
            list_row = [ int(i) for i in list_row]
            X.append(list_row)


classifier = SVC(C=c,kernel=mykernel,decision_function_shape='ovo',probability=True)

#X = np.asarray(X)
#length = len(sorted(X,key=len, reverse=True)[0])
#X = np.array([xi+[None]*(length-len(xi)) for xi in X])
#for x in X:
#    new_x = np.asarray(x)
#    new_X.append(new_x)
#X = np.asarray(new_X)
y = np.asarray(y)

embed()
print('fitting')
classifier.fit(X,y)
print('fitting done')        
pickle.dump(classifier,codecs.open('trained_svm.pickle','w'))





    

