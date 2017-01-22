#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import codecs
import re

from IPython import embed

train_files ='filenames_trainset.json'
train_dirs ='dirames_trainset.json'
test_files ='filenames_testset.json'
test_dirs ='dirames_testset.json'

# load separated connections generated by process_json.py
json_files = []

for i,name in enumerate([train_files,test_files, train_dirs,test_dirs]):
    json_files.append(json.load(codecs.open(name,'r')))

# merge files
filenames = []
dirnames = []
for files in json_files[:2]:
    for k in files.keys():
        filenames.extend(files[k])
for dirs in json_files[2:]:
    for k in dirs.keys():
        dirnames.extend(dirs[k])

for filename in filenames:
    print(filename + ';f')
for dirname in dirnames:
    print(dirname + ';d')
    
