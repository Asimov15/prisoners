#!/usr/bin/python
import copy
import random

class bot():
# strategy 0 = cooperate
# strategy 1 = defect

    def __init__(self, n, s):
        self.strategy_names = [ "always_cooperate"      , # 0
                                "always_default"        , # 1
                                "tit_for_tat"           , # 2
                                "random"                , # 3
                                "forgiver"              , # 4
                                "occasional_cheater"    , # 5
                                "analyser"]               # 6
        self.number   = n
        self.strategy = s       
        self.score = 0
        self.memory = []
        for i in range(20):
            b = []
            c = copy.deepcopy(b)
            self.memory.append(c)
        
    def get_strat(self, bot_number):
        method = getattr(self, self.strategy_names[self.strategy])
        return method(bot_number)
    
    def always_cooperate(self, bot_number):
        return 0
        
    def always_default(self, bot_number):
        return 1
    
    def tit_for_tat(self, bot_number):
        if len(self.memory[bot_number]) == 0:
            return 0
        elif self.memory[bot_number][-1] == 0:
            return 0
        else:
            return 1
    
    def forgiver(self, bot_number):
        if len(self.memory[bot_number]) < 2:
            return 0
        elif self.memory[bot_number][-1] == 1 and self.memory[bot_number][-2] == 1:
            return 1
        else:
            return 0
    
    def occasional_cheater(self, bot_number):
        if len(self.memory[bot_number]) == 0:
            return 0
        elif self.memory[bot_number][-1] == 0:
            if random.randrange(0,10,1) == 9:
                return 1
            else:
                return 0
        else:            
            return 1
    def analyser(self, bot_number):
        if self.record(bot_number) > 80.0:
            return 0
        else:
            return 1
            
    def random(self,n):
        return random.randrange(0,2,1)
    
    def record(self, b):
        count = 0
        coop  = 0
        perc = 0.0
        for x in self.memory[b]:
            count += 1
            if x == 0:
                coop += 1
        
        if count > 5:
            return 100 * float(coop) / float(count)
        else:
            return 100            
                

class tournament():  
    def __init__(self):
        self.botlist = []
        x = bot(0,2)    
        self.botlist.append(x)
        x = bot(1,1)
        self.botlist.append(x)
        x = bot(2,2)
        self.botlist.append(x)
        x = bot(3,6)
        self.botlist.append(x)
        x = bot(4,4)
        self.botlist.append(x)
        x = bot(5,4)
        self.botlist.append(x)
        x = bot(6,5)
        self.botlist.append(x)
        x = bot(7,5)
        self.botlist.append(x)
        x = bot(8,5)
        self.botlist.append(x)
        x = bot(9,5)
        self.botlist.append(x)
        x = bot(10,1)
        self.botlist.append(x)
        x = bot(11,5)
        self.botlist.append(x)
        x = bot(12,6)
        self.botlist.append(x)
        x = bot(13,6)
        self.botlist.append(x)
        x = bot(14,6)
        self.botlist.append(x)
    
    def conduct(self, n):    
        for i in range(n):
            for j in self.botlist:
                for k in self.botlist:
                    if j.number != k.number:
                        self.scorer(j,k)    
    
    def scorer(self, b1, b2):
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

    def output(self):
        for aa in sorted(self.botlist, key=lambda bot: bot.score, reverse=True):
            print "bot: {0:2} stategy: {1:20} score: {2}".format(aa.number, aa.strategy_names[aa.strategy], aa.score)

mytorny = tournament()

mytorny.conduct(200)

mytorny.output()
