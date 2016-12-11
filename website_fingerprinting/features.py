#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import exp
# expects two strings and return the cosad-value for those two
"""
Compute the Optimal String Alignment distance between two given
strings (a and b)
"""
def osad(a, b):
    d = {}
    lenstr1 = len(a)
    lenstr2 = len(b)
    for i in range(-1,lenstr1+1):
        d[(i,-1)] = i+1
    for j in range(-1,lenstr2+1):
        d[(-1,j)] = j+1
 
    for i in range(lenstr1):
        for j in range(lenstr2):
            if a[i] == b[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min(
                           d[(i-1,j)] + 1, # deletion
                           d[(i,j-1)] + 1, # insertion
                           d[(i-1,j-1)] + cost, # substitution
                          )
            if i and j and a[i]==b[j-1] and a[i-1] == b[j]:
                d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition
 
    return d[lenstr1-1,lenstr2-1]

def n_osad(a,b):
    denominator = a
    if len(b) < len(a):
        denominator = b
    return n_osac(a,b)/denominator
    

def mykernel(a,b):
    #re_a =''.join(list(a))
    #re_b = ''.join(list(b))
    # a and b supposed to be vectors of string
    return exp(-n_osad(a,b)**2)
    
