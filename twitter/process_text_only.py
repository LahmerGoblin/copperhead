#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import codecs
import zipfile
from IPython import embed
# Cross Validation
from sklearn.model_selection import train_test_split

import re


text_tweets = json.load(codecs.open('text_only.json','r'))

class Features:
    # matches one url only - don't mind
    #http_matcher = re.compile('^.*(http://[^[:blank:]]+).*$')
    def __init__(self):
        pass

    def hash_tags(self,text):
        # returns list of hashtags in string
        hash_tags = []
        for t in text.split():
            if t[0] == '#':
                hash_tags.append(t)
        return hash_tags
                
    def user_mentions(self,text):
        # returns list of user mentions in string
        mentions = []
        for t in text.split():
            if t[0] == '#':
                mentions.append(t)
        return mentions

    def url(self,text):
        # returns [list of] url in text
        # possibly split in shorturl provider and hash?
        ## what about more than one url in tweet? Unlikely
        ##match = http_matcher.match(text)
        urls = []
        for t in text.split():
            if 'http://' in t:
                urls.append(t)
        return urls
    def chain_ex(self,text):
        hash_tags = self.hash_tags(text)
        mentions = self.user_mentions(text)
        urls = self.url(text)
        return (hash_tags,mentions,urls)
        
    
feature_extractor = Features()

extracted_features = {}
for tweet in text_tweets.keys():
    truth = text_tweets[tweet][1]
    text = text_tweets[tweet][0]
    extracted_features[tweet] = (feature_extractor.chain_ex(text),truth)
    
    
# review Feature Extraction
# save features to json file
json.dump(extracted_features,codecs.open('text_only_features.json','w'))

