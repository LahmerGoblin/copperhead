#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Collection of features for content-driven spam detection

def n_grams(tokenized_string,n=4):
    ''' outputs ngrams of given string with n being the size of a sliding window moving over tokenized_string. '''
    n_grams = []

    return zip(*[tokenized_string[i:] for i in range(0,n)])
