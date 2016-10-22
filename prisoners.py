#!/usr/bin/python
import copy
import random

class bot():
# strategy 0 = cooperate
# strategy 1 = defect

    def __init__(self, n, s):
        self.number   = n
        self.strategy = s       
        self.score = 0
        self.memory = []
        for i in range(10):
            b = []
            c = copy.deepcopy(b)
            self.memory.append(c)
        
    def get_strat(self,n):
        if self.strategy == 0:
            return self.always_cooperate()
        
        if self.strategy == 1:
            return self.always_default()
        
        if self.strategy == 2:
            return self.tit_for_tat(n)
            
        if self.strategy == 3:
            return self.random()
    
    def always_cooperate(self):
        return 0
        
    def always_default(self):
        return 1
    
    def tit_for_tat(self, n):
        if len(self.memory[n]) == 0:
            return 0
        elif self.memory[n][-1] == 0:
            return 0
        else:
            return 1
            
    def random(self):
        return random.randrange(0,2,1)
        

def scorer(b1, b2):
    if b1.get_strat(b2.number) == 0 and b2.get_strat(b1.number) == 0:
        b1.score += 1
        b2.score += 1
        b1.memory[b2.number].append(0)
        b2.memory[b1.number].append(0)
        
    if b1.get_strat(b2.number) == 1 and b2.get_strat(b1.number) == 0:
        b1.score += 2
        b1.memory[b2.number].append(0)
        b2.memory[b1.number].append(1)
    
    if b1.get_strat(b2.number) == 0 and b2.get_strat(b1.number) == 1:
        b2.score += 2       
        b1.memory[b2.number].append(1)
        b2.memory[b1.number].append(0)
        
    if b1.get_strat(b2.number) == 1 and b2.get_strat(b1.number) == 1:
        b1.memory[b2.number].append(1)
        b2.memory[b1.number].append(1)

def tournament(b):  
    for i in range(1000):
        for j in b:
            for k in b:
                if j.number != k.number:
                    scorer(j,k)    

botlist = []

x = bot(2,1)    
botlist.append(x)
x = bot(3,1)    
botlist.append(x)
x = bot(4,2)    
botlist.append(x)
x = bot(5,2)    
botlist.append(x)
x = bot(6,3)    
botlist.append(x)
x = bot(7,3)    
botlist.append(x)

tournament(botlist)

for aa in botlist:
    print "bot: {0} stategy: {1} score: {2}".format(aa.number, aa.strategy, aa.score)

