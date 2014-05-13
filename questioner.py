# -*- coding: utf-8 -*-

class Questioner(object):

    BE = ['ARE', 'IS', 'AM']
    LETTERS = ['O', 'S', 'X', 'Z', 'H']   # буквы, для которых мн. ч. -es
    
    def __init__(self, s):
        self.s = s
    
    
    def _make_verb(self, s):  # находим глагол
        s = s.upper()
        for word in s.split():
            if word[-1] == '*':
                verb = word[:-1]
        return(verb)
    
    
    def request(self, s):
        verb = self._make_verb(s)   
        parts = s.upper().partition(verb)
        if verb in self.BE:  
            return("{0} {1}{2}?".format(verb, parts[0], parts[2][2:]))
        else:
            if self._third_person(verb):
                if verb[-3] not in self.LETTERS:
                    return("DOES {0}{1} {2}?".format(parts[0], verb[0:len(verb) - 1], parts[2][2:]))
                else:
                    return("DOES {0}{1} {2}?".format(parts[0],verb[0:len(verb) - 2], parts[2][2:]))
            else: 
                return("DO {0}{1} {2}?".format(parts[0], verb, parts[2][2:]))
            
            
    def _third_person(self, v):
        if v.endswith('S') and v[-2:] != 'SS':
            return True
        else:
            return False
            

if __name__ == "__main__":
    s = "Dog likes* Filya"
    q = Questioner(s)
    print(q.request(s))
    assert q.request("ALEX IS* TALL") == "IS ALEX TALL?"
    assert q.request("THEY ARE* HAPPY") == "ARE THEY HAPPY?"
     #РЅР° 5 Р±Р°Р»Р»РѕРІ
    assert q.request("KATE GOES* TO SCHOOL") == "DOES KATE GO TO SCHOOL?"
    assert q.request("WINTER USUALLY COMES* LATE") == "DOES WINTER USUALLY COME LATE?"
    assert q.request("STUDENTS OFTEN COME* LATE") == "DO STUDENTS OFTEN COME LATE?"
    assert q.request("I HAVE* A CAR") == "DO I HAVE A CAR?"
    assert q.request("THE LIBRARY POSSESSES* BOOKS") == "DOES THE LIBRARY POSSESS BOOKS?"
    assert q.request("I MISS* MY DOG") == "DO I MISS MY DOG?"
    assert q.request("THEY FIX* EVERYTHING") == "DO THEY FIX EVERYTHING?"