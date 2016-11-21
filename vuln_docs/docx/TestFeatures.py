#!/usr/bin/python3
# -*- coding: utf-8 -*-

from DocXReader import DocXReader
import DocXFeatures


from IPython import embed

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

import zipfile
import os
import pickle
import codecs
import sys

import itertools

k = 5
reader = DocXReader('training.zip')
fold_runs = []
feature_path = 'train_features_' + str(k) + 'folderbranch_preextracted.pickle'


#doc_file_vuln = reader.read_content('docx-train/02252.1')
#doc_file_non_vuln = reader.read_content('docx-train/00180.0')
#embed()

# 02252.1
        
#    # k-fold cross validation
#    # k defaults to 5
k_folds = reader.k_fold(k=k,rand=True)   
#
extracted_k_folds = []
for fold in k_folds:
    feature_matrix = []
    groundtruth_matrix = []
    for doc in fold:
        document = (doc,reader.read_content(doc))
        print('Performing Feature Extraction '+ document[0])

        file_structure = document[1].namelist()
        
        # build dict
        feature_vector = {}
        for word in file_structure:
            try:
                feature_vector[word] += 1
            except KeyError:
                feature_vector[word] = 1
        # get rid of prefix 
        vuln_nonvuln = document[0][len('docx-train/'):]
        #acquire groundtruth
        groundtruth_matrix.append(reader.groundtruth_dict[vuln_nonvuln])
        #extract_features
        feature_matrix.append((document[0],feature_vector))
    # does contain all k folds. For k = 5 len(extracted_k_folds) -> 5
    extracted_k_folds.append((feature_matrix,groundtruth_matrix))

for i,test_fold in enumerate(k_folds):
    # exclude current test_fold

    extracted_folds_train = [ ext_fold for ext_fold in extracted_k_folds if ext_fold is not extracted_k_folds[i]]
    ext_test_fold = extracted_k_folds[i]

    #determining vocab
    # isolate words from trainingsset only
    words = []
    for fold in extracted_folds_train:
        for doc in fold[0]:
            words.append(doc[1].keys())
    features = set(itertools.chain(*words))

    fold_runs.append((ext_test_fold,extracted_folds_train,features))
# pickle away
if not os.path.isfile(feature_path):
    print('saving new featurepool')
    pickle.dump(fold_runs,
                codecs.open(feature_path, 'wb'))
else:
    print('Using previously safed featurepool')
    fold_runs = pickle.load(codecs.open(feature_path, 'rb'))

res_sets = []
for run in fold_runs:
    ext_test_fold = run[0]
    ext_folds_train = run[1]
    features = run[2] 
    
    feature_list = []
    groundtruth = []
    for fold in ext_folds_train:
        for doc in fold[0]:
            feature_list.append(doc[1])
        groundtruth.extend(fold[1])
        
    # TODO: transform X into feature matrix
    print('No. of features ' + str(len(features)))
    #vectorizer = DictVectorizer(vocabulary=features)
    vectorizer = DictVectorizer()
    # Now transform every tokenized mail back into one string
    # transform all the strings into a sparse matrix
    sparse_X = vectorizer.fit_transform(feature_list)         

    # train model 
    classifier = {} 
    classifier['bayes'] = ('mbayes',MultinomialNB())
    classifier['svm'] = ('svc',SVC(kernel='linear'))
    classifier['tfidf'] = ('tfidf',TfidfTransformer())
    classifier['randfor'] = ('random_forest',RandomForestClassifier())
    classifier_chain = []
    for arg in sys.argv[1:]:
        classifier_chain.append(classifier[arg])

    class_pipeline = Pipeline(classifier_chain)
    class_pipeline.fit(sparse_X,groundtruth)

    res_set = {}
    # evaluate each doc and add classification to res_set
    for doc in ext_test_fold[0]:
        doc_vec = vectorizer.transform(doc[1])
        res_set[doc[0]] = class_pipeline.predict(doc_vec)

    res_sets.append(res_set)
classifiers = ''
for arg in sys.argv[1:]:
    classifiers += arg + '_'
persist_path = 'eval_' + str(k) + '_' + classifiers + '_folderbranches_preextracted.pickle'
if not os.path.isfile(persist_path):
    pickle.dump(res_sets,codecs.open(persist_path,'wb'))








