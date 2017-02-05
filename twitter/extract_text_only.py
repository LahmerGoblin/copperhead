#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import codecs
import zipfile
from IPython import embed
from json.decoder import JSONDecodeError

count = 10
filename = '0_23fb84484fe54e8680ae3871d7abdcb9'
if len(sys.argv)>1:
    if sys.argv[1] == 'test':
        filename = ''

groundtruth = {}   
with codecs.open(filename+'.labels','r') as readfile:
    for row in readfile:
        line = readfile.readline()
        try:
            groundtruth[line.split(';')[0]] = line.split(';')[1][:-1]
        except IndexError:
            pass
tweets = {}
with codecs.open(filename,'r') as readfile:
    for row in readfile:
        tweet = readfile.readline()
        try:
            json_tweet = json.loads(tweet)
            tweets[json_tweet['id']] = (json_tweet['text'],groundtruth[str(json_tweet['id'])])
        except JSONDecodeError:
            print(json_tweet)
            pass

json.dump(tweets,codecs.open('text_only.json','w'))
        

