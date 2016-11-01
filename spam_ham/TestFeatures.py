#!/usr/bin/python3
# -*- coding: utf-8 -*-

from DataReader import DataReader
import Features
from nltk.tokenize import word_tokenize            
from nltk.corpus import stopwords
from IPython import embed
from nltk.stem.porter import PorterStemmer

from sklearn.pipeline import Pipeline

reader = DataReader('trainingsdata.zip')
stemmer = PorterStemmer() 
# k-fold cross validation
# k defaults to 5
k_folds = reader.k_fold(k=2)   
for test_fold in k_folds:
    # exclude current test_fold
    folds = [ fold for fold in k_folds if fold is not test_fold ]
    for fold in folds:
        for mail in fold:
            tokenized_mail = word_tokenize(mail[1])
            # remove stopwords
            stemmed_mail_nostops = [ stemmer.stem_word(word) for word in tokenized_mail if word not in stopwords.words('english')]
            # stem
            n_grams = Features.n_grams(stemmed_mail_nostops)
            embed()







