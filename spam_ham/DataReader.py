#!/usr/bin/python3
# -*- coding: utf-8 -*-

import codecs
import csv
from IPython import embed
import zipfile
import numpy as np
import re

# DataReader
class DataReader:
    # Filenames of all Mails. content can be obtained
    # via read_content method
    mailnames = None
    # groundtruth
    groundtruth_dict = None 
    # zipfile containing data.
    # shouldn't be accessed from outside DataReader
    zipf = None

    k_folds = None

    
    def __init__(self,zipname):

        self.zipf = zipfile.ZipFile(zipname)
        filenames = self.zipf.namelist()
        gt_filename = None
        # groundtruth_filename
        mail_names = []
        for f in filenames:
            if f.endswith('labels'):
                gt_filename = f
                continue
            if f.endswith('/'):
                continue
            mail_names.append(f)

        self.mailnames = mail_names
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


    def read_content(self,filename,string=True):
        filename = filename
        content = []
        with self.zipf.open(filename,'r') as readfile:
            for row in readfile:
                # index hack gets rid of lineterminators
                content.append(row.decode('UTF-8','replace')[0:-2])

        if string:
            # return only one string, no list of rows
            new_content = ''
            for row in content:
                new_content += row
            content = new_content    
        return content

    def k_fold(self,k=5):
        l = len(self.mailnames)/k
        full_text = []
        for mailname in self.mailnames:
            full_text.append(self.read_content(mailname))
        self.k_folds = [list(zip(self.mailnames[i:int(i+l)],full_text[i:int(i+l)])) for i in range(0, k) if (i+l)<len(self.mailnames)]

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
    main = DataReader('trainingsdata.zip')
    file0 = main.read_content(main.mailnames[0])
    main.k_fold()
    embed()
    
