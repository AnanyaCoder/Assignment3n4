# -*- coding: utf-8 -*-
"""
Author : Ananya Mukherjee
Task   : Basic Tokenization

Input Parameter: Corpus Name

a. Word tokenizer
b. Punt tokenizer (-,,. etc)
c. Email tokenizer
d. Url tokenizer
e. Number/Currency tokenizer
f. Name tokenizer , i.e. John M.
g. Hastag tokenizer
h. Mention tokenizer (@john)

Output Files : <filename>_Output.txt

"""
import pandas as pd
import numpy as np
import re
import sys
import pickle
import os

filePath = sys.argv
#******************************************************************************
def AfterFirstSplit(List,regex): #email #url #hashtag, #mention #name #numbercurrency 
    newtoken = []
    for token in List:
        if re.search(regex,token):
            tokens = re.split(regex,token)
            for t in tokens:
                newtoken.append(str.strip(t))
        else:
            newtoken.append(str.strip(token))
    return newtoken


#Function for tokenizing based on space assuming that the sentence is tokenized atleast once before.
def WordTokenizer(List):
    newtoken = []
    for token in List:
        if re.search('\s',token) and not(re.search(name_tokenizer,token)):
            tokens = re.split('\s',token)
            for t in tokens:
                newtoken.append(str.strip(t))
        else:
            newtoken.append(str.strip(token))
    return newtoken


#Read a given document and perform tokenization linewise. 
#Write the output into an output text file.
def getTokensforDocument(Document):
    outputfile = 'corpus2Pickle/' + Document+'_Output.pkl'
    TextOutput = 'corpus2OutputText/' + Document+'_Output.txt'
    fp = open(outputfile, "wb")
    Op = open(TextOutput, "w")
    with open(Document,"rb") as fileobj:
    #with open(Document,"rb") as fileobj: #for corpus3,4
        
        output = []
        for line in fileobj:
            try:
                line = line.decode('utf-8')
            except:
                continue
    #check for all the regex whichever is first available, start splitting from ther.
            Newtoken = []
            for i in range(len(pattern)):
                if re.search(pattern[i],line):
                    List = re.split(pattern[i],line)
                    for j in range(len(pattern))[i+1:]:
                        Newtoken = AfterFirstSplit(List,pattern[j])
                        List = Newtoken
                    
                    Newtoken = WordTokenizer(List)
                    lastword = Newtoken.pop()
                    if re.search('.$',lastword):
                        b = lastword.rstrip('.')
                        Newtoken.append(b)
                        Newtoken.append('.')
                    break
            
            if not Newtoken:      #split based on only space as it failed the previous tests.
                if re.search('\s',line):
                    List = re.split('\s',line)
                    lastword = List.pop()
                    if re.search('.$',lastword):
                        b = lastword.rstrip('.')
                        List.append(b)
                        List.append('.')
                    Newtoken = List
                
            if '' in Newtoken:
                Newtoken.remove('') 
            
            output.append(Newtoken)
            #Storing as tokenized sentences 
            txt = " ".join(Newtoken)
            Op.write(txt+'\n')
            
            print(Newtoken,'\n')
    #Storing the list format of tokens in pickle file
    pickle.dump(output,fp)
            
                     
            
 
    
#******************************************************************************
#Assgining all the regular expressions for various tokenizing categories.
#******************************************************************************
word_tokenizer = "([\w']+)"
punt_tokenizer = "([,;!-\"\''\'\(\)=%^*&<>|])"
eos = "([.:?][\s\n])"
email_tokenizer = "([\w._-]+@[[\w-]+\.+[\w-]+)"
url_tokenizer = "(https?:\/\/www.[\w_-]+.[\w\/]+)"
number_currency_tokenizer = '(\s[$₹£€¥]?[\d]+.?[\d]+)'
name_tokenizer = "([A-Z][\w]+\s[A-Z]\.)" #'Ananya M.'
hashtag_mention_tokenizer = "(\s[#@][\w_]+\s)"  
#******************************************************************************
#Creating a list of all the regular expressions
#******************************************************************************
pattern = [url_tokenizer,email_tokenizer,hashtag_mention_tokenizer,name_tokenizer,number_currency_tokenizer,punt_tokenizer,eos]
#******************************************************************************


if (filePath[1] == 'corpus1' or filePath[1] == 'corpus2'):
    path = filePath[1]+'Folder'
    for r,d,f in os.walk(path):
        for file in f:
            #print(file)
            getTokensforDocument(file)
elif (filePath[1] == 'corpus3' or filePath[1] == 'corpus4'):
    path = filePath[1]+'.txt'
    getTokensforDocument(path)
else:
    print("Kindly enter any one argument in correct format! \ncorpus1 \ncorpus2 \ncorpus3 \ncorpus4")


        
#getTokensforDocument("corpus4.txt")

