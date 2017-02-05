#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import codecs
import zipfile
from IPython import embed
from datetime import datetime
from json.decoder import JSONDecodeError

filename = '0_23fb84484fe54e8680ae3871d7abdcb9'
outname = 'metadata_features_train.json'
if len(sys.argv)>1:
    if sys.argv[1] == 'test':
        filename = ''
        outname = 'metadata_features_test.json'

groundtruth = {}   
with codecs.open(filename+'.labels','r') as readfile:
    for row in readfile:
        line = readfile.readline()
        try:
            groundtruth[line.split(';')[0]] = line.split(';')[1][:-1]
        except IndexError:
            pass
extracted_tweets = {}
with codecs.open(filename,'r') as readfile:
    for row in readfile:
        tweet_row = readfile.readline()
        try:
            tweet = json.loads(tweet_row)

            id = tweet['id']
            tweet.pop('text')
            # now extract features on the fly
            extracted_features = {}
            try:
                for url in tweet['entities']['urls']:
                    extracted_features[url['expanded_url']] = 1
            except KeyError:
                pass
            
            try:
                extracted_features['source'] = tweet['source']
            except KeyError:
                pass

            try:
                extracted_features['timestamp_tweet'] = float(tweet['timestamp_ms'])/1000.0
            except KeyError:
                pass

            try:
                for hashtag in tweet['entities']['hashtags']:
                    extracted_features[hashtag['text']] = 1
            except KeyError:
                pass
            try:
                for mention in tweet['entities']['user_mentions']:
                    extracted_features[mention['id_str']] = 1
            except KeyError:
                pass

            try:
                #normalize these
                extracted_features['friends_count'] = int(tweet['friends_count'])
            except KeyError:
                extracted_features['friends_count'] = 0

            try:
                #normalize these
                extracted_features['followers_count'] = tweet['followers_count']
            except KeyError:
                pass

            try:
                #normalize these
                extracted_features['retweet_count'] = tweet['retweet_count']
            except KeyError:
                pass

            date = datetime.strptime(tweet['user']['created_at'],'%a %b %d %X %z %Y')
            extracted_features['user_created_at'] = date.timestamp()
            extracted_features['user_time_zone'] = tweet['user']['time_zone']
            extracted_features['user_verified'] = tweet['user']['verified']
            #normalize
            extracted_features['name_len'] = len(tweet['user']['name'])
            extracted_features['user_id'] = tweet['user']['id']
            extracted_features['profile_sidebar_fill_color'] = tweet['user']['profile_sidebar_fill_color']
            extracted_features['profile_text_color'] = tweet['user']['profile_text_color']
            extracted_features['default_profile_image']  = tweet['user']['default_profile_image']

            
            #if tweet['is_quote_status']:
            #    pass
            #    #'quoted_status': { 'id','source'
            #if tweet['retweeted']:
            #    pass
            extracted_tweets[id] = extracted_features
            #'retweeted'
            ## erstmal nicht
            ##if geo_enabled:
            ##'coordinates' ? (preprocessing)
            #
            #'country_code'
            #'in_reply_to_status_id'
        except JSONDecodeError:
            print(tweet_row)

    
json.dump((extracted_tweets,groundtruth),codecs.open(outname,'w'))
    

