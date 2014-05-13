#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree as ET

punction= ['?', '!', '.', ',', ':', ';', '"', '(', ')']
punct_name = {'?':'what', '!':'exclamation mark', '.':'full stop', ',':'comma', ':':'colon', ';':'semi', '"':'quote', '(':'open bracket', ')':'close bracket'}

tokens = 0        # counting tokens in paragraph
words = 0         # counting tokens in sentence
sentences = 0     # counting sentences in paragraph
sentence = 0      # for sentence if in the text
paragraphs = 0    
par_sen = {}
par_tok = {}
sen_tok = {}
sen_words = {}
tokes = []

with open('probe.txt', encoding = "utf8") as fd:   
    for line in fd:
        tokenall = line.split(" ")         # tokens with '\n' symbols 
        tokplus = line.strip().split(' ')  # tokens without '\n' symbols
        
        for i in range(len(tokplus)):      # make list of words and punctuations
            punct = len(tokplus[i]) - 1
            if len(tokplus[i]) == 0:
                continue           
            if tokplus[i][-1] in punction:
                tokes.append(tokplus[i][0:punct])
                tokes.append(tokplus[i][-1])
            if tokplus[i][0] in punction:
                tokes.append(tokplus[i][1:])
                tokes.append(tokplus[i][0])                
            if tokplus[i][-1] not in punction and tokplus[i][0] not in punction:
                tokes.append(tokplus[i])
        
        for token in tokenall:             # create dictionaries paragraphs_sentences, paragraphs_tokens, sentences_tokens
            tokens += 1 
            words += 1    
                        
            for char in token:
                if char in punction:
                    words += 1
                    tokens += 1
                if char == ".":
                    sentence += 1
                    sentences += 1
                    sen_tok[sentence] = words
                    words = 0                       
                if char == "\n":
                    paragraphs += 1
                    par_tok[paragraphs] = tokens
                    par_sen[paragraphs] = sentences
                    sentences = 0
                    tokens = 0 

b = 0                                       # counter for sentence number                   
for i in tokes:                             # making dictionary of type "sentence number - the word of the sentence"
    sen_words.setdefault(b, []).append(i)
    if i == '.':
        b += 1

        
# writing xml to file

idn = 1   # sentence counter
tok = 1   # tokens counter
ln = 0    # for start and end

root = ET.Element('analyzed_document')
for i in range(1, len(par_sen)+ 1):
    paragraph = ET.SubElement(root,'paragraph')
    paragraph.set('id', str(i))
    paragraph.set('sentences', str(par_sen[i]))
    paragraph.set('tokens', str(par_tok[i]))   
    for m in range(1, par_sen[i] + 1):
        sentence = ET.SubElement(paragraph,'sentence')
        sentence.set('id', str(idn))
        sentence.set('tokens',str(sen_tok[idn]))
        for t in sen_words[idn-1]:
            token = ET.SubElement(sentence,'token')
            token.set('Value', str(t))
            if t in punction:
                ln -= 1
                token.set('Type','Punction: ' + str(punct_name[t]))
            if t not in punction:               
                token.set('Type','Word:English')                            
            token.set('Start', str(ln))            
            token.set('End', str(ln + len(t) - 1))               
            ln = ln + len(t) + 1             
        tok += int(sen_tok[idn])         
        idn += 1 

tree = ET.ElementTree(root)
tree.write('foo.xml', encoding = "utf-8", pretty_print=True, xml_declaration=True)
