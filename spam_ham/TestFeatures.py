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
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer

import os
import pickle
import codecs

import itertools

k = 5
reader = DataReader('trainingsdata.zip')
stemmer = PorterStemmer() 
fold_runs = []

if not os.path.isfile('train_features_' + str(k) + '_preextracted.pickle'):
        
    # k-fold cross validation
    # k defaults to 5
    k_folds = reader.k_fold(k=k,rand=True)   

    extracted_k_folds = []
    for fold in k_folds:
        feature_matrix = []
        groundtruth_matrix = []
        for mail in fold:
            print('Performing Feature Extraction '+ mail[0])
            tokenized_mail = word_tokenize(mail[1])
            # remove stopwords and stemming
            stemmed_mail_nostops = [ stemmer.stem_word(word) for word in tokenized_mail if word not in stopwords.words('english')]
            # remove characters of length one - such as parentheses
            stemmed_mail_nostops = [ word for word in stemmed_mail_nostops if len(word)>1]

            # build dict
            bow = {}
            for word in stemmed_mail_nostops:
                try:
                    bow[word] += 1
                except KeyError:
                    bow[word] = 1
            # get rid of prefix 
            spam_ham = mail[0][len('spam1-train/'):]
            #acquire groundtruth
            groundtruth_matrix.append(reader.groundtruth_dict[spam_ham])
            #extract_features
            #n_grams = Features.n_grams(stemmed_mail_nostops,n=2)
            #X.append(list(n_grams))
            feature_matrix.append((mail[0],bow))
        # does contain all k folds. For k = 5 len(extracted_k_folds) -> 5
        extracted_k_folds.append((feature_matrix,groundtruth_matrix))
    
    for i,test_fold in enumerate(k_folds):
        # exclude current test_fold

        #X : {array-like, sparse matrix}, shape = [n_samples, n_features]
        #y : array-like, shape = [n_samples]
        
        # exclude current test_fold
        extracted_folds_train = [ ext_fold for ext_fold in extracted_k_folds if ext_fold is not extracted_k_folds[i]]
        ext_test_fold = extracted_k_folds[i]

        #determining vocab
        # isolate words from trainingsset only
        words = []
        for fold in extracted_folds_train:
            for mail in fold[0]:
                words.append(mail[1].keys())
        features = set(itertools.chain(*words))

        fold_runs.append((ext_test_fold,extracted_folds_train,features))
    # pickle away
    pickle.dump(fold_runs,
                codecs.open('train_features_' + str(k) + '_preextracted.pickle', 'wb'))
else:
    fold_runs = pickle.load(codecs.open('train_features_' + str(k) + '_preextracted.pickle', 'rb'))

res_sets = []
for run in fold_runs:
    ext_test_fold = run[0]
    ext_folds_train = run[1]
    features = run[2] 
    
    tokenized_mails = []
    groundtruth = []
    for fold in ext_folds_train:
        for mail in fold[0]:
            tokenized_mails.append(mail[1])
        for gt in fold[1]:
            groundtruth.append(gt)
        
    # TODO: transform X into feature matrix
    print('No. of features ' + str(len(features)))
    #vectorizer = DictVectorizer(vocabulary=features)
    vectorizer = DictVectorizer()
    # Now transform every tokenized mail back into one string
    # transform all the strings into a sparse matrix
    sparse_X = vectorizer.fit_transform(tokenized_mails)         

    # train model 
    bayes = ('mbayes',MultinomialNB())
    #svm = ('svc',SVC(kernel='linear'))
    class_pipeline = Pipeline([bayes])
    class_pipeline.fit(sparse_X,groundtruth)

    res_set = {}
    # evaluate each mail and add classification to res_set
    for mail in ext_test_fold[0]:
        mail_vec = vectorizer.transform(mail[1])
        res_set[mail[0]] = class_pipeline.predict(mail_vec)

    res_sets.append(res_set)
persist_path = 'eval_' + str(k) + '_bayes_preextracted.pickle'
if not os.path.isfile(persist_path):
    pickle.dump(res_sets,codecs.open(persist_path,'wb'))
embed()








