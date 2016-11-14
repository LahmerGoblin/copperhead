#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

# Collection of features for header-driven spam detection

def ngrams(tokenized_string,n=2):
    ''' outputs ngrams of given string with n being the size of a sliding window moving over tokenized_string. '''
    n_grams = []

    return zip(*[tokenized_string[i:] for i in range(0,n)])

#header_line is always a raw string from a header file
# feat_mat is a dictionary where a feature is appended in case
# it could be extracte from header_line

#From Quintana@telecentro.com.ar  Sat Apr 21 09:47:48 2007
def regex_col(header_line,feat_mat):
    regex =re.compile('From (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['regex_col'] = match.group(1)
        return True
    return False

#Return-Path: <Quintana@telecentro.com.ar>
def return_path(header_line,feat_mat):
    regex =re.compile('Return-Path: (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['return_path'] = match.group(1)
        return True
    return False


#From: "Julio Alcolea" <Quintana@telecentro.com.ar>
def from_col(header_line,feat_mat):
    regex =re.compile('From: (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['from_col'] = match.group(1)
        return True
    return False


#Reply-To: "Santiago Almazan" <Quintana@telecentro.com.ar>
def replyto_col(header_line,feat_mat):
    regex =re.compile('Reply-To: (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['replyto_col'] = match.group(1)
        return True
    return False
    
#To: the00@plg.uwaterloo.ca
def to_col(header_line,feat_mat):
    regex =re.compile('To: (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['to_col'] = match.group(1)
        return True
    return False

def delivered_to(header_line,feat_mat):
    regex =re.compile('Delivered-To: (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['delivered_to'] = match.group(1)
        return True
    return False

# ===================================================
#Date: Sat, 21 Apr 2007 07:37:24 -0600
def date(header_line,feat_mat):
    # TODO: parse further
    regex =re.compile('Date: (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['subject'] = match.group(1)
        return True
    return False

#Subject: pruebe su destreza manual
def subj(header_line,feat_mat):
    regex =re.compile('Subject: (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['subject'] = match.group(1)
        return True
    return False


#X-Mailer: AOL 8.0 for Windows US sub 816
def xmailer(header_line,feat_mat):
    regex =re.compile('X-Mailer: (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['xmailer'] = match.group(1)
        return True
    return False

#MIME-Version: 1.0
def mime_ver(header_line,feat_mat):
    regex =re.compile('X-Mailer: (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['mime_ver'] = match.group(1)
        return True
    return False
#X-Spam-Status: No, score=1.4 required=5.0 tests=BAYES_50, HTML_10_20,
#        HTML_MESSAGE autolearn=no version=3.1.8

    
#Content-Type: multipart/alternative;
def cont_type(header_line,feat_mat):
    regex =re.compile('Content-Type: (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['mime_ver'] = match.group(1)
        return True
    return False

#Message-ID: <%RNDUCCHAR2025@ciudad.com.ar>
def message_id(header_line,feat_mat):
    regex =re.compile('Message-ID: (.*)$')
    match = regex.match(header_line)
    if match is not None:
        feat_mat['message_id'] = match.group(1)
        return True
    return False

#Received: from plg2.math.uwaterloo.ca (plg2.math.uwaterloo.ca [129.97.186.80])
#        by speedy.uwaterloo.ca (8.12.8/8.12.5) with ESMTP id l3LDll0I027698
#        for <theplg@speedy.uwaterloo.ca>; Sat, 21 Apr 2007 09:47:47 -0400
#Received: from pool-70-18-193-191.ny325.east.verizon.net (pool-70-18-193-191.ny325.east.verizon.net [70.18.193.191])
#        by plg2.math.uwaterloo.ca (8.13.8/8.13.8) with SMTP id l3LDknOS022196
#        for <the00@plg.uwaterloo.ca>; Sat, 21 Apr 2007 09:47:17 -0400 (EDT)
#Received: from 159.156.151.192 by 70.18.193.191; Sat, 21 Apr 2007 15:42:24 +0200
#important: multline feature
def received_chain(header_line,feat_mat):
    pass
