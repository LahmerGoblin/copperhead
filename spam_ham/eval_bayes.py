#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import codecs
import pickle

import numpy as np

from DataReader import DataReader
from IPython import embed

k = 5
persist_path = 'eval_' + str(k) + '_bayes_preextracted.pickle'
res_sets = pickle.load(codecs.open(persist_path,'rb'))

reader = DataReader('trainingsdata.zip')

balanced_accuracies = []
for res_set in res_sets:
    gt_keys = list(res_set.keys())
    gt_keys = [ k[len('spam1-train/'):] for k in gt_keys]

    count_correct_spam = 0
    count_correct_ham = 0
    count_spam_gt = 0
    count_ham_gt = 0
    for gt_key in gt_keys:
        truth = int(reader.groundtruth_dict[gt_key])
        
        if truth == 1:
            count_spam_gt += 1
        else:
            count_ham_gt += 1

        if int(reader.groundtruth_dict[gt_key])== int(res_set['spam1-train/'+gt_key][0]):
            if truth == 1:
                count_correct_spam +=1
            else:
                count_correct_ham += 1
    print(count_spam_gt)
    print(count_correct_spam)
    print(count_ham_gt)
    print(count_correct_ham)
    b_acc = np.mean([ count_correct_spam/float(count_spam_gt),count_correct_ham/float(count_ham_gt) ])
    
    balanced_accuracies.append(b_acc)

embed()

