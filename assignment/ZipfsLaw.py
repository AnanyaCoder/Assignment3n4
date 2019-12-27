#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Author : Ananya Mukherjee
Task   : Zipf graph for corpus1.txt and corpus2.txt, give analysis for 10001 to 11000
ranked words for each corpus in report.
"""

import pandas as pd
import numpy as np
import pickle
from operator import itemgetter
import matplotlib.pyplot as plt
import os

words = []
counts = []
ranks = []
frequency = {}
def getFrequency(tokenizedFile):    
    with open(tokenizedFile,"rb") as fp:
        List = pickle.load(fp)
        for line in List:
            #print(line)
            for word in line:
               # print(word)
                count = frequency.get(word,0)
                frequency[word] = count+1

      

#for corpus1 
corpus1 = 'corpus1Pickle'
#for corpus2
corpus2 = 'corpus2Pickle'
path = corpus2
tokenizedFile = ''
for r,d,f in os.walk(path):
    for file in f:
        print(file)
        tokenizedFile = path+'/'+file
        getFrequency(tokenizedFile)


for rank,key in enumerate(reversed(sorted(frequency.items(), key = itemgetter(1)))):

    if rank > 10000 and rank < 11000:
        words.append(key[0])
        counts.append(key[1])
        ranks.append(rank)
                    
                    
plt.xlabel('rank of words')
plt.ylabel('frquency of words')
plt.plot(words,counts)
plt.show()

    
    
        
    
        