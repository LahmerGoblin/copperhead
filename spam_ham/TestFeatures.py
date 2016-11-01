#!/usr/bin/python3
# -*- coding: utf-8 -*-

from DataReader import DataReader
#from Features import ngrams
from nltk.tokenize import word_tokenize            
from nltk.corpus import stopwords
from IPython import embed
from nltk.stem.porter import PorterStemmer

reader = DataReader('trainingsdata.zip')
stemmer = PorterStemmer 
# k-fold cross validation
# k defaults to 5
k_folds = reader.k_fold()   
for test_fold in k_folds:
    # exlude current test_fold
    folds = [ fold for fold in k_folds if fold is not test_fold]
    for fold in folds:
        for mail in fold:
            tokenized_mail = word_tokenize(mail[1])
            # remove stopwords
            tokenized_mail = [ word for word in tokenized_mail if word is not in stopwords.words('english')]
            # stem
            stemmed_mail = stemmer.stem(tokenized_mail)





