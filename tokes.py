punction= ['?', '!', '.', ',', ':', ':', "'"]

tokens = 0        # in paragraph
words = 0         # in sentence
sentences = 0     # in paragraph
sentence = 0      # on the whole
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
            else:
                tokes.append(tokplus[i])
        
        for token in tokenall:             # create dictionaries paragraphs_sentences, paragraphs_tokens, sentences_tokens
            tokens += 1 
            words += 1    
            for char in token:
                if char == ',':
                    words += 1
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

b = 0   # номер предложения                    
for i in tokes:                             # создали словарь вида номер предложения - все слова внутри
    sen_words.setdefault(b, []).append(i)
    if i == '.':
        b += 1
print(par_sen)

idn = 1
tok = 1
ln = 0

root = ET.Element('Analyzed document')
for i in range(1, len(par_sen)+ 1):
    paragraph = ET.SubElement(root,'paragraph')
    paragraph.set('id', str(i))
    paragraph.set('sentences', str(par_sen[i]))
    for m in range(1, par_sen[i] + 1):
        sentence = ET.SubElement(paragraph,'sentence')
        sentence.set('id', str(idn))
        sentence.set('tokens',str(sen_tok[idn]))
        for t in range(tok, sen_tok[idn] + 1):
            if tokes[t] in punction:
                ln -= 1
            token = ET.SubElement(sentence,'token')
            token.set('Value', str(tokes[t]))
            token.set('End', str(ln + len(tokes[t]) - 1))  
            token.set('Start', str(ln))  
            token.set('Type','Word:English')            
            ln = ln + len(tokes[t]) + 1             
        idn += 1 
        tok += int(sen_tok[idn])            
tree = ET.ElementTree(root)
tree.write('foo.xml', 'utf-8', 'w')