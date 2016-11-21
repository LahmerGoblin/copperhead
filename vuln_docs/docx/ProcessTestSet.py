#!/usr/bin/python3
# -*- coding: utf-8 -*-

from DocXReader import DocXReader

from IPython import embed

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

import os
import pickle
import codecs

import itertools

vectorizer = None
class_pipeline = None
model_path = 'svm_folderstructure_classpipe.pickle'
out_path = 'out_svm_folderstructure.pickle';
if not os.path.isfile(model_path):

    train_reader = DocXReader('training.zip')
    
    train_features = []
    groundtruth = []
    for doc in train_reader.docnames:
        document = (doc,train_reader.read_content(doc))
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
        groundtruth.append(train_reader.groundtruth_dict[vuln_nonvuln])
        #extract_features
        train_features.append((document[0],feature_vector))

    
    
    vectorizer = DictVectorizer()
    # Now transform every tokenized mail back into one string
    # transform all the strings into a sparse matrix
    sparse_vecs = vectorizer.fit_transform([t[1] for t in train_features])         
    # train model 
    #bayes = ('mbayes',MultinomialNB())
    svm = ('svc',SVC(kernel='linear'))
    tfidf = ('tfidf',TfidfTransformer())
    #randfor = ('random_forest',RandomForestClassifier())
    print('Training model')
    class_pipeline = Pipeline([svm])
    class_pipeline.fit(sparse_vecs,groundtruth)
    pickle.dump((vectorizer,class_pipeline),codecs.open(model_path,'wb'))
else:
    tupl = pickle.load(codecs.open(model_path,'rb'))
    class_pipeline = tupl[1]
    vectorizer = tupl[0]

test_reader = DocXReader('testing.zip',gt=False)

output = []
if os.path.isfile(out_path):
    output = pickle.load(codecs.open(out_path,'rb'))
else:
    for doc in test_reader.docnames:
        document = None
        document = (doc,test_reader.read_content(doc))
        print('Performing Feature Extraction '+ document[0])

        file_structure = document[1].namelist()
        
        # build dict
        feature_vector = {}
        for word in file_structure:
            try:
                feature_vector[word] += 1
            except KeyError:
                feature_vector[word] = 1
        
        mail_vec = vectorizer.transform(feature_vector)
        result = int(class_pipeline.predict(mail_vec)[0])
        mail_title = document[0][len('docx-test/'):]
    
        output.append(mail_title + ';' + str(result))
    pickle.dump(output,codecs.open(out_path,'wb'))
output = [ out+'\n' for out in output] 
with codecs.open('copperhead_testset_01_docx_svm_folderstructure.csv','wb','utf-8') as out_file:
    out_file.writelines(output)

    
    
    

