#!/usr/bin/python3
# -*- coding: utf-8 -*-

from DataReader import DataReader
import Features

from nltk.tokenize import word_tokenize            
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from IPython import embed

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

import os
import pickle
import codecs

import itertools

reader = DataReader('trainingsdata.zip')
stemmer = PorterStemmer() 
fold_runs = []

if not os.path.isfile('train_features.pickle'):
        
    # k-fold cross validation
    # k defaults to 5
    # TODO: k_folds does not work
    k_folds = reader.k_fold(k=2)   
    embed()
    
    for test_fold in k_folds:
        # exclude current test_fold
        folds = [ fold for fold in k_folds if fold is not test_fold ]
        #X : {array-like, sparse matrix}, shape = [n_samples, n_features]
        #y : array-like, shape = [n_samples]
        y = []
        X = []
        for fold in folds:
            for mail in fold:
                # TODO: Why is mail 00001 missing here? -> k_folds not working as it should
                print('Performing Feature Extraction '+ mail[0])
                tokenized_mail = word_tokenize(mail[1])
                # remove stopwords and stemming
                stemmed_mail_nostops = [ stemmer.stem_word(word) for word in tokenized_mail if word not in stopwords.words('english')]
                # remove characters of length one - such as parentheses
                stemmed_mail_nostops = [ word for word in stemmed_mail_nostops if len(word)>1]
                
    
                # get rid of prefix 
                spam_ham = mail[0][len('spam1-train/'):]
                #acquire groundtruth
                y.append(reader.groundtruth_dict[spam_ham])
                #extract_features
                #n_grams = Features.n_grams(stemmed_mail_nostops,n=2)
                #X.append(list(n_grams))
                X.append(stemmed_mail_nostops)
    
                # Which classifier to use? Word Embedding might perform best?
        #determining vocab
        features = set(itertools.chain(*X))
        fold_runs.append((test_fold,folds,X,y,features))
    # pickle away
    pickle.dump(fold_runs,
                codecs.open('train_features.pickle', 'wb'))
else:
    fold_runs = pickle.load(codecs.open('train_features.pickle', 'rb'))

for run in fold_runs:
    test_fold = run[0]
    folds = run[1]
    X = run[2]
    y = run[3]
    features = run[4] 
    
    # TODO: transform X into feature matrix
    print('No. of features ' + str(len(features)))
    vectorizer = CountVectorizer(vocabulary=features)
    # Now transform every tokenized mail back into one string
    concat_X = []
    for x in X:
        concat_X.append(' '.join(x))
    # transform all the strings into a sparse matrix
    sparse_X = vectorizer.transform(concat_X)         

    bayes = ('mbayes',MultinomialNB())
    class_pipeline = Pipeline([bayes])
    class_pipeline.fit(sparse_X,y)

    res_set = {}
    for mail in test_fold:
        tokenized_mail = word_tokenize(mail[1])
        # remove stopwords and stemming
        stemmed_mail_nostops = [ stemmer.stem_word(word) for word in tokenized_mail if word not in stopwords.words('english')]
        # remove characters of length one - such as parentheses
        stemmed_mail_nostops = [ word for word in stemmed_mail_nostops if len(word)>1]
        conc_mail = vectorizer.transform(' '.join(stemmed_mail_nostops))
        
        res_set[mail[0]] = class_pipeline.predict(conc_mail)

    embed()








