#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 17:13:37 2019

@author: Ananya Mukherjee
Task : Write a code to create an N-Gram Model (N is parameter)
"""
import pandas as pd
import numpy as np
import pickle
import os 

N = 6

sos = '<s>'  #Start of sentence
eos = '</s>' #End of sentence

Dict_N = {}  #dictionary containing frequencies of all N grams
Dict_N_1 = {} #dictionary containing frequencies of all N-1 grams


def generate_ngrams(tokens, n):
    
    ngrams = zip(*[tokens[i:] for i in range(n)])
    #r = [" ".join(ngram) for ngram in ngrams]
    ngrams_1 = zip(*[tokens[i:] for i in range(n-1)])
    for ngram in ngrams:
        count = Dict_N.get(ngram,0)
        Dict_N[ngram] = count + 1
    
    for ngram_1 in ngrams_1:
        count1 = Dict_N_1.get(ngram_1,0)
        Dict_N_1[ngram_1] = count1 + 1  
    


'''
tokenizedFile = "corpus3copy.txt_Output.txt"
with open(tokenizedFile,"rb") as fp:
    List = pickle.load(fp)
    for line in List:
        #Remove spaces if any
        if '' in line:
            line.remove('')
        #insert start of sentence
        line.insert(0,sos)
        #insert end of sentence
        line.append(eos)
        print(line)
        generate_ngrams(line, N)
'''

#for corpus1 
corpus1 = 'corpus1Pickle'
#for corpus2
corpus2 = 'corpus2Pickle'
corpus3 = 'corpus3Pickle'
corpus4 = 'corpus4Pickle'
path = corpus4
tokenizedFile = ''
fileno = 0
for r,d,f in os.walk(path):
    for file in f:
        fileno +=1 
        print(file)
        tokenizedFile = path+'/'+file
        with open(tokenizedFile,"rb") as fp:
            List = pickle.load(fp)
            for line in List:
                #Remove spaces if any
                if '' in line:
                    line.remove('')
                #insert start of sentence
                line.insert(0,sos)
                #insert end of sentence
                line.append(eos)
                #print(line)
                generate_ngrams(line, N)
                
            

NgramsFile = 'Ngrams_'+str(N)
with open(NgramsFile,"wb") as fp:
    pickle.dump(Dict_N,fp)
N_1 = N-1
NgramsFile = 'Ngrams_'+str(N_1)
with open(NgramsFile,"wb") as fp:
    pickle.dump(Dict_N_1,fp)




        
