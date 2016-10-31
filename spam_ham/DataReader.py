#!/usr/bin/python3
# -*- coding: utf-8 -*-

import codecs
import csv
from IPython import embed
import zipfile
import numpy as np

# DataReader
class DataReader:
    prefix = 'data/'
    mailnames = None
    groundtruth_dict = None 


    
    def __init__(self,zipname):

        zipf = zipfile.ZipFile(zipname)
        filenames = zipf.namelist()
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
        gt_dict = {}
        with codecs.open(self.prefix+groundtruth_path) as csvfile:
                gtreader = csv.reader(csvfile, delimiter=';')
                for row in gtreader:
                    gt_dict[row[0]] = row[1]
        # Groundtruth vector loaded
        self.groundtruth_dict = np.asarray(gt_dict)


    def read_content(self,zipf,filename):
        filename = self.prefix+filename
        codecs.open(filename)


    def evaluate(self,result_dict):
        
    

            

if __name__ == "__main__":
    main = DataReader('zipdata.zip')
    embed()
