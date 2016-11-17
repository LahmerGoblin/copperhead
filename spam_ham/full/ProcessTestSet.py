#!/usr/bin/python3
# -*- coding: utf-8 -*-

from FullReader import FullReader
import FullFeatures

from nltk.tokenize import word_tokenize            
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

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
stemmer = PorterStemmer() 
model_path = 'svm_tfidf__bigrams_classpipe.pickle'
out_path = 'out_svm_tfidf__bigrams.pickle';
if not os.path.isfile(model_path):

    train_reader = FullReader('training_full.zip')
    
    train_features = []
    groundtruth = []
    for mailname in train_reader.mailnames:
        mail = train_reader.read_content(mailname)
        # extract header
        print('Performing Feature Extraction '+ mailname)
        tokenized_mail = [ m.split(' ') for m in mail[1][0]]

        # build dict
        bow = {}
        for word in itertools.chain(*tokenized_mail):
            try:
                bow[word] += 1
            except KeyError:
                bow[word] = 1
        # get rid of prefix 


        bigrams = [FullFeatures.ngrams(line) for line in tokenized_mail]

        for bigram in itertools.chain(*bigrams):
            # convert bigram
            bistring = bigram[0]+bigram[1]
            try:
                bow[bistring] += 1
            except KeyError:
                bow[bistring] = 1

        tokenized_mail = word_tokenize(''.join(mail[1][1]))
        # remove stopwords and stemming
        stemmed_mail_nostops = [ stemmer.stem_word(word) for word in tokenized_mail if word not in stopwords.words('english')]
        # remove characters of length one - such as parentheses
        stemmed_mail_nostops = [ word for word in stemmed_mail_nostops if len(word)>1]

        for word in stemmed_mail_nostops:
            try:
                bow[word] += 1
            except KeyError:
                bow[word] = 1
        # add bigrams as additional feature
        n_grams = FullFeatures.ngrams(stemmed_mail_nostops,n=2)
        n_grams = [ n_gram[0].join(n_gram[1]) for n_gram in n_grams]
        for word in n_grams:
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
    #bayes = ('mbayes',MultinomialNB())
    svm = ('svc',SVC(kernel='linear'))
    tfidf = ('tfidf',TfidfTransformer())
    #randfor = ('random_forest',RandomForestClassifier())
    print('Training model')
    class_pipeline = Pipeline([tfidf,svm])
    class_pipeline.fit(sparse_vecs,groundtruth)
    pickle.dump((vectorizer,class_pipeline),codecs.open(model_path,'wb'))
else:
    tupl = pickle.load(codecs.open(model_path,'rb'))
    class_pipeline = tupl[1]
    vectorizer = tupl[0]

test_reader = FullReader('testingfull.zip',gt=False)

output = []
if os.path.isfile(out_path):
    output = pickle.load(codecs.open(out_path,'rb'))
else:
    for mailname in test_reader.mailnames:
        mail = test_reader.read_content(mailname)
        tokenized_mail = [ m.split(' ') for m in mail[1][0]]

        # build dict
        bow = {}
        for word in itertools.chain(*tokenized_mail):
            try:
                bow[word] += 1
            except KeyError:
                bow[word] = 1
        # get rid of prefix 


        bigrams = [FullFeatures.ngrams(line) for line in tokenized_mail]

        for bigram in itertools.chain(*bigrams):
            # convert bigram
            bistring = bigram[0]+bigram[1]
            try:
                bow[bistring] += 1
            except KeyError:
                bow[bistring] = 1

        tokenized_mail = word_tokenize(''.join(mail[1][1]))
        # remove stopwords and stemming
        stemmed_mail_nostops = [ stemmer.stem_word(word) for word in tokenized_mail if word not in stopwords.words('english')]
        # remove characters of length one - such as parentheses
        stemmed_mail_nostops = [ word for word in stemmed_mail_nostops if len(word)>1]

        for word in stemmed_mail_nostops:
            try:
                bow[word] += 1
            except KeyError:
                bow[word] = 1
        # add bigrams as additional feature
        n_grams = FullFeatures.ngrams(stemmed_mail_nostops,n=2)
        n_grams = [ n_gram[0].join(n_gram[1]) for n_gram in n_grams]
        for word in n_grams:
            try:
                bow[word] += 1
            except KeyError:
                bow[word] = 1

        mail_vec = vectorizer.transform(bow)
        result = int(class_pipeline.predict(mail_vec))
        mail_title = mailname[len('spam3-test/'):]
    
        output.append(mail_title + ';' + str(result))
    pickle.dump(output,codecs.open(out_path,'wb'))
output = [ out+'\n' for out in output] 
with codecs.open('copperhead_testset_01_full_svm_tfidf_bigrams.csv','wb','utf-8') as out_file:
    out_file.writelines(output)

    
    
    

