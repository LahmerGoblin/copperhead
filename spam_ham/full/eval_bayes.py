#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import codecs
import pickle
import sys

import numpy as np

from FullReader import FullReader
from IPython import embed

k = 5
persist_path = None
if len(sys.argv)>1:
    persist_path = sys.argv[1]
else:
    print('Argument required')
    sys.exit(1)
    
#persist_path_tfidf = 'eval_' + str(k) + '_svm_tfidf_preextracted.pickle'
#persist_path_svm = 'eval_' + str(k) + '_svm_preextracted.pickle'
#persist_path_bayes = 'eval_' + str(k) + '_bayes_preextracted.pickle'
res_sets = pickle.load(codecs.open(persist_path,'rb'))

reader = FullReader('training_full.zip')

balanced_accuracies = []
for res_set in res_sets:
    gt_keys = list(res_set.keys())
    gt_keys = [ k[len('spam2-train/'):] for k in gt_keys]

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

        if int(reader.groundtruth_dict[gt_key])== int(res_set['spam2-train/'+gt_key][0]):
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

