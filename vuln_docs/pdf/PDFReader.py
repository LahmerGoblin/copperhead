#!/usr/bin/python3
# -*- coding: utf-8 -*-

import codecs
import csv
from IPython import embed
import zipfile
import numpy as np
import re
import random
import copy
import subprocess

# Important in order to read 
import io

class PDFReader:
    # Filenames of all Mails. content can be obtained
    # via read_content method
    docnames = None
    # groundtruth
    groundtruth_dict = None 
    # zipfile containing data.
    # shouldn't be accessed from outside DataReader
    zipf = None

    k_folds = None

    gt = False
    
    def __init__(self,zipname,gt=True):
        self.zipf = zipfile.ZipFile(zipname)
        filenames = self.zipf.namelist()
        gt_filename = None
        self.gt = gt
        # groundtruth_filename
        mail_names = []
        for f in filenames:
            if f.endswith('labels'):
                gt_filename = f
                continue
            if f.endswith('/'):
                continue
            mail_names.append(f)
        self.docnames = mail_names
        if gt:
            self.read_groundtruth(gt_filename)

    def read_groundtruth(self,groundtruth_path):
        ''' reads groundtruth file into a dictionary. keys are filenames,values either 1 (spam) or 0 (ham)
        '''
        gt_dict = {}
        rex_row = re.compile('^(.*);(.*);.*$')
        with self.zipf.open(groundtruth_path,'r') as csvfile:
            for row in csvfile:
                match = rex_row.match(row.decode('UTF-8'))
                if match is not None:
                    gt_dict[match.group(1)] = match.group(2)
        # Groundtruth vector loaded
        self.groundtruth_dict = gt_dict

        # Attention: Assumes that zipfile exists zipped as well as unzipped
    def read_content(self,filename):
        filename = filename
        content = None
        if self.gt :
            content = subprocess.check_output('strings training/' + filename, shell=True)
        else:
            content = subprocess.check_output('strings testing/' + filename, shell=True)
        return content
            

    def k_fold(self,k=5,rand=False):
        data = self.docnames
        if rand:
            data = copy.deepcopy(self.docnames)
            random.shuffle(data)

        r = len(data)%k
        #print(r)
        # get rid of tail
        tail_count = len(data) - r
        data = data[:tail_count]
        # acquire full text
        #for i,d in enumerate(data):
        #    data[i] = (d,self.read_content(d))
        length = int(len(data)/k)
        #print(length)
        folds = []
        for i in range(0,k):
            x = int(i*length)
            y = int(i*length+length)
            print(str(x) + ':' + str(y))
            folds.append(data[x:y])
        
        self.k_folds = folds
        return folds
    
        # should also work if result_dic does not contain all the keys
    def evaluate(self,result_dict):
        ham_dist = 0
        for key in result_dict:
            if result_dict[key] == self.groundtruth_dict[key]:
                pass
            else:
                ham_dist =+ 1
        return ham_dist

    def precision(self,result_dict):
        tp = 0
        tp_fp = 0
        for key in result_dict:
            if result_dict[key] == 1:
                tp_fp += 1
                if result_dict[key] == self.groundtruth_dict[key]:
                    tp +=1
        return tp/float(tp_fp)
            
    def recall(self,result_dict):
        tp = 0
        p = 0
        for key in result_dict:
            if self.groundtruth_dict[key] == 1 :
                p +=1
            if self.groundtruth_dict[key] == 1 and result_dict[key] == 1:
                tp +=1
        return tp/float(p)
        
if __name__ == "__main__":
    main = PDFReader('trainingsheader.zip')
    file0 = main.read_content(main.docnames[0])
    #main.k_fold()
    embed()
    
