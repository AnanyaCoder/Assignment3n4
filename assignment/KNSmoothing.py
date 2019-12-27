#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:04:27 2019

@author: ananya

Kneser Ney Smoothing + Interpolation
"""
import numpy as np
import pickle
#import sys
#import os
eps = np.finfo(float).eps
UNKProb = eps
#filePath = sys.argv

N = 4
d = 0.75
'''
if(filePath[2] == 'corpus1'):
    TrainedModelPath = 'corpus1_Model'
elif (filePath[2] == 'corpus3'):
    TrainedModelPath = 'corpus3_Model'
elif (filePath[2] == 'corpus4'):
    TrainedModelPath = 'corpus4_Model'
else:
    print("please enter correct trained corpus model")
    exit(0)
'''
TrainedModelPath = 'corpus4_Model'   

TrainedModel_N = 'corpus4_Model/Ngrams_1'
with open(TrainedModel_N,"rb") as fp:
    Ngrams_1 = pickle.load(fp)

TrainedModel_N = 'corpus4_Model/Ngrams_2'
with open(TrainedModel_N,"rb") as fp:
    Ngrams_2 = pickle.load(fp)

   
TrainedModel_N = 'corpus4_Model/Ngrams_3'
with open(TrainedModel_N,"rb") as fp:
    Ngrams_3 = pickle.load(fp)
    
TrainedModel_N = 'corpus4_Model/Ngrams_4'
with open(TrainedModel_N,"rb") as fp:
    Ngrams_4 = pickle.load(fp)


TrainedModel_N = 'corpus4_Model/Ngrams_5'
with open(TrainedModel_N,"rb") as fp:
    Ngrams_5 = pickle.load(fp)
    
TrainedModel_N = 'corpus4_Model/Ngrams_6'
with open(TrainedModel_N,"rb") as fp:
    Ngrams_6 = pickle.load(fp)

NGRAM = {1:Ngrams_1,2:Ngrams_2,3:Ngrams_3,4:Ngrams_4,5:Ngrams_5,6:Ngrams_6}
#NGRAM = {1:Ngrams_1,2:Ngrams_2,3:Ngrams_3,4:Ngrams_4}
     
#Get the count of the ngrams words in the ngram model
def getCount(N,ngrams):  
    ModelSentences = NGRAM[N]
    key = tuple(ngrams)
    if key in ModelSentences.keys():
        count = ModelSentences[tuple(ngrams)]
    else:
        count = UNKProb
    return count

#Get the count of the timeS startWords follow any other word in the ngrams model
def getCountofStartingWords(N,startWords): #startwords = w1w2w3
    count = 0  
    ModelSentences = NGRAM[N]
    for key in ModelSentences.keys():  #key = w1w2w3wk
        if(tuple(startWords) == key[:N-1]): #compare w1w2w3 == w1w2w3 by ignoring wk
            count += 1
    return count
   
def smoothing(numerator,denominator,total,N):   
    if N!=2:
        #Calculate Continuation Probability 
        PCN = smoothing(numerator,denominator[1:],total[1:],N-1)
    else:
        PCN = UNKProb
    
    #Calculate First Term
    firstTerm_numerator = (getCount(N,total))-d          #Count(w1,w2,w3,w4)
    firstTerm_denominator =  getCount(N-1,denominator) #Count(w1,w2,w3)
    if (firstTerm_denominator == 0):
        firstTerm_denominator = UNKProb 
        
    if (firstTerm_numerator > 0):       
        firstTerm = firstTerm_numerator / firstTerm_denominator
    else:
        firstTerm = 0
    
    #Calculate Lambda
    count_n_1gram_succeed_wk = getCountofStartingWords(N,denominator)
    lamda = (d * count_n_1gram_succeed_wk) / firstTerm_denominator
    
    
    PKN = firstTerm + (lamda * PCN)
    
    return PKN

'''
if (filePath[3] == 'corpus3'):
    TestCorpusPath = "corpus3Pickle/corpus3.txt_Output.pkl"
elif (filePath[3] == 'corpus4'):
    TestCorpusPath = "corpus4Pickle/corpus4.txt_Output.pkl"
else:
    print("please enter correct trained corpus model")
    exit(0)
'''
TestCorpusPath = "corpus4Pickle/corpus4.txt_Output.pkl"

outputFile = 'LM_Output.txt'
PerplexityFile = 'PexplexityFile'
Op = open(outputFile, "w")
pp = open(PerplexityFile, "w")
TotalPerplexity = 0
with open(TestCorpusPath,"rb") as A:
    corpusSentences = pickle.load(A)   
    for sentence in corpusSentences:
        if not (sentence):
            continue
            
        if '' in sentence:
            sentence.remove('')
        Probability = 0 #Reassigning 0 as initial probability
        sentence_length = len(sentence) #Length of the sentence        
        ngrams_of_sentence = zip(*[sentence[i:] for i in range(N)])
        for ngram in ngrams_of_sentence:
            line = list(ngram)
            P = smoothing(line[N-1],line[:N-1],line,N)     
            if P == 0:
                P = UNKProb
                
            Probability = Probability + np.log(P)  #log liklihood
        
        perplexity = np.exp(-1*Probability/float(sentence_length))
        print("Sentence:",sentence)
        print("LogLikelihood:", Probability)
        print("Perplexity:", perplexity)
                
        TotalPerplexity+= perplexity
        txt = " ".join(sentence) + ':Probability:'+str(Probability) + ' Perplexity:'+str(perplexity)
        Op.write(txt+'\n')
        
    
avgPerplexity = TotalPerplexity/float(len(corpusSentences))
print("Average Perplexity of %s is %d:" %(TestCorpusPath,avgPerplexity))
txt1 = TestCorpusPath + ':' + str(avgPerplexity)
pp.write(txt1+'\n')
