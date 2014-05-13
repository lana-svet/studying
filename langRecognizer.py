from math import log
from collections import defaultdict

class LangRecognizer:
    DEFAULT_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    
    def __init__(self, N, alphabet = DEFAULT_ALPHABET):
        self._statBG = defaultdict(int)
        self._statRU = defaultdict(int)
        self._statUK = defaultdict(int)
        self._statMAC = defaultdict(int)
        self._stats = defaultdict(int)
        self._N = N
        self._alphabet = alphabet
        
    def learn(self, filename, lang):
        total = 0
        with open(filename, encoding="utf8") as f:
            for s in f:
                s = s.strip().upper()
                for i in range(int(len(s))- int((self._N-1))):
                    ngram = s[i:i+self._N]
                    if self._check_alphabetness(ngram):
                        self._stats[ngram] +=1
        total = sum(self._stats.values())
        for k, v in self._stats.items():
            self._stats[k] = log(v / total)
            
        if lang == "BG":
            self._statBG = self._stats
            self._stats = defaultdict(int)
        if lang == "RU":
            self._statRU = self._stats
            self._stats = defaultdict(int)
        if lang == "UK":
            self._statUK = self._stats
            self._stats = defaultdict(int)
        if lang == "MAC":
            self._statMAC = self._stats
            self._stats = defaultdict(int)
    
    def _check_alphabetness(self, ngram):
        for char in ngram:
            if char not in self._alphabet:
                return False
        return True
        
    def classify(self, filename):
        with open(filename, encoding="utf8") as f:
            for s in f:
                s = s.upper()
                log_sumBG = 0.0
                log_sumRU = 0.0
                log_sumUK = 0.0
                log_sumMAC = 0.0
                for i in range(len(s) - (self._N-1)):
                    ngram = s[i:i+self._N]
                    if ngram in self._statBG:
                        log_sumBG += self._statBG[ngram]
                        log_sumRU -= 20
                        log_sumUK -= 20
                        log_sumMAC -= 20
                    if ngram in self._statRU:
                        log_sumRU += self._statRU[ngram] 
                        log_sumBG -= 20
                        log_sumUK -= 20
                        log_sumMAC -= 20                       
                    if ngram in self._statUK:
                        log_sumUK += self._statUK[ngram]
                        log_sumRU -= 20
                        log_sumBG -= 20
                        log_sumMAC -= 20                        
                    if ngram in self._statMAC:
                        log_sumMAC += self._statMAC[ngram]
                        log_sumRU -= 20
                        log_sumUK -= 20
                        log_sumBG -= 20
        result = self._compare (log_sumBG, log_sumRU, log_sumUK, log_sumMAC)
        return result        
                    
    def _compare (self, log_sumBG, log_sumRU, log_sumUK, log_sumMAC):
        if max(log_sumBG, log_sumRU, log_sumUK, log_sumMAC) == log_sumBG:
            return ("BG")
        if max(log_sumBG, log_sumRU, log_sumUK, log_sumMAC) == log_sumRU:
            return ("RU")
        if max(log_sumBG, log_sumRU, log_sumUK, log_sumMAC) == log_sumUK:            
            return("UK")        
        if max(log_sumBG, log_sumRU, log_sumUK, log_sumMAC) == log_sumMAC:            
            return("MAC")  
                
                
if __name__ == "__main__":
    #ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    rec = LangRecognizer(N = 2)
    rec.learn("rusTrain.txt", "RU")
    rec.learn("bulgTrain.txt", "BG")
    rec.learn("ukrTrain.txt", "UK")
    rec.learn("macTrain.txt", "MAC")
    print(rec.classify("bulgTest.txt"))
    
    assert(rec.classify("rusTest.txt") == "RU")
    assert(rec.classify("bulgTest.txt") == "BG")
    assert(rec.classify("ukrTest.txt") == "UK")
    assert(rec.classify("macTest.txt") == "MAC")
    
    # чиселка для каждого языка - потом вычислять самую классную чиселку