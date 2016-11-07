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
from sklearn.feature_extraction import DictVectorizer

import os
import pickle
import codecs

import itertools

vectorizer = None
class_pipeline = None
stemmer = PorterStemmer() 
model_path = 'nb_trained_class_pipe.pickle'
if not os.path.isfile(model_path):

    train_reader = DataReader('trainingsdata.zip')
    
    train_features = []
    groundtruth = []
    for mailname in train_reader.mailnames:
        mail = train_reader.read_content(mailname)
        tokenized_mail = word_tokenize(mail)
        # remove stopwords and stemming
        stemmed_mail_nostops = [ stemmer.stem_word(word) for word in tokenized_mail if word not in stopwords.words('english')]
        # remove characters of length one - such as parentheses
        stemmed_mail_nostops = [ word for word in stemmed_mail_nostops if len(word)>1]
        bow = {}
        for word in stemmed_mail_nostops:
            try:
                bow[word] += 1
            except KeyError:
                bow[word] = 1
        spam_ham = mail[0][len('spam1-train/'):]
        train_features.append(bow)
        gt_key = mailname[len('spam1-train/'):]
        groundtruth.append(int(train_reader.groundtruth_dict[gt_key]))
    
    
    vectorizer = DictVectorizer()
    # Now transform every tokenized mail back into one string
    # transform all the strings into a sparse matrix
    sparse_vecs = vectorizer.fit_transform(train_features)         
    # train model 
    bayes = ('mbayes',MultinomialNB())
    #svm = ('svc',SVC(kernel='linear'))
    class_pipeline = Pipeline([bayes])
    class_pipeline.fit(sparse_vecs,groundtruth)
    pickle.dump((vectorizer,class_pipeline),codecs.open(model_path,'wb'))
else:
    tupl = pickle.load(codecs.open(model_path,'rb'))
    class_pipeline = tupl[1]
    vectorizer = tupl[0]

test_reader = DataReader('testdata.zip',gt=False)

output = []
for mailname in test_reader.mailnames:
    mail = test_reader.read_content(mailname)
    tokenized_mail = word_tokenize(mail)
    # remove stopwords and stemming
    stemmed_mail_nostops = [ stemmer.stem_word(word) for word in tokenized_mail if word not in stopwords.words('english')]
    # remove characters of length one - such as parentheses
    stemmed_mail_nostops = [ word for word in stemmed_mail_nostops if len(word)>1]
    bow = {}
    for word in stemmed_mail_nostops:
        try:
            bow[word] += 1
        except KeyError:
            bow[word] = 1
    mail_vec = vectorizer.transform(bow)
    result = class_pipeline.predict(mail_vec)
    mail_title = mail[len('spam1-test/'):]
    output.append(mail_title + ';' + str(result))
with codecs.open('copperhead_testset_01','w') as out_file:
    out_file.writelines(output)

    
    
    

