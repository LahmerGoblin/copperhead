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
        gt_dict = {}
        rex_row = re.compile('^(.*);(.*);.*$')
        with self.zipf.open(groundtruth_path,'r') as csvfile:
            for row in csvfile:
                match = rex_row.match(row.decode('UTF-8'))
                if match is not None:
                    gt_dict[match.group(1)] = match.group(2)
        # Groundtruth vector loaded
        self.groundtruth_dict = gt_dict


    def read_content(self,filename):
        filename = filename
        content = []
        with self.zipf.open(filename,'r') as readfile:
            for row in readfile:
                # index hack gets rid of lineterminators
                content.append(row.decode('UTF-8')[0:-2])

        return content

    def evaluate(self,result_dict):
        ham_dist = 0
        for key in result_dict:
            if result_dict[key] == self.groundtruth_dict[key]:
                pass
            else:
                ham_dist =+ 1
        return ham_dist
        
    

            

if __name__ == "__main__":
    main = DataReader('trainingsdata.zip')
    file0 = main.read_content(main.mailnames[0])
    embed()
    
