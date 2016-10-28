#!/usr/bin/python

# David Zuccaro
# 25/10/2016

import copy
import random

class bot():
# strategy 0 = cooperate
# strategy 1 = defect

    def __init__(self, n, s, ml=70):
        self.strategy_names = [ "always_cooperate"      , # 0
                                "always_default"        , # 1
                                "tit_for_tat"           , # 2
                                "random"                , # 3
                                "forgiver"              , # 4
                                "occasional_cheater"    , # 5
                                "analyser"              , # 6            
                                "faulty_analyser"       , # 7
                                "bad_guy"               , # 8
                                ]  
                                
        self.bot_id = n
        self.strategy = s       
        self.score = 0
        self.memory = []
        self.memory_length = ml
        self.memory_index = 0
        self.create_mem()
        self.strictness = 70.0
        self.accuracy = 100
        self.goodness = 50
        
    def remember(self, n, what_other_did):
        if len(self.memory[n]) < self.memory_length:
            self.memory[n].append(what_other_did)
        else:
            self.memory[n][self.memory_index] = what_other_did
            
        self.memory_index = (self.memory_index + 1) % self.memory_length
    
    def create_mem(self):
        b = []
        for i in range(20):            
            c = copy.deepcopy(b)
            self.memory.append(c)
    
    def init_mem(self):
        for i in self.memory:
            self.memory.remove(i)
        self.create_mem()            
        
    def get_strat(self, bot_bot_id):
        method = getattr(self, self.strategy_names[self.strategy])
        return method(bot_bot_id)
    
    def always_cooperate(self, bot_bot_id):
        return 0
        
    def always_default(self, bot_bot_id):
        return 1
    
    def tit_for_tat(self, bot_bot_id):
        if len(self.memory[bot_bot_id]) == 0:
            return 0
        elif self.memory[bot_bot_id][-1] == 0:
            if random.randrange(0,100,1) == 99:
                return 1 # a mistake
            else:
                return 0
        else:
            if random.randrange(0,100,1) == 99:
                return 0 # a mistake
            else:
                return 1
    
    def forgiver(self, bot_bot_id):
        if len(self.memory[bot_bot_id]) < 2:
            return 0
        elif self.memory[bot_bot_id][-1] == 1 and self.memory[bot_bot_id][-2] == 1:
            # has defected the last two times
            if random.randrange(0,10,1) == 9:
                return 0 # a mistake
            else:
                return 1
        else:
            if random.randrange(0,10,1) == 9:
                return 1 # a mistake
            else:
                return 0
    
    def occasional_cheater(self, bot_bot_id):
        if len(self.memory[bot_bot_id]) == 0:
            return 0
        elif self.memory[bot_bot_id][-1] == 0:
            if random.randrange(0,10,1) == 9:
                return 1
            else:
                return 0
        else:            
            return 1
            
    def analyser(self, bot_bot_id):
        if self.record(bot_bot_id) > 80.0:
            return 0
        else:
            return 1
    
    def faulty_analyser(self, bot_bot_id):
        
        rec_perc = self.record(bot_bot_id) 

        if rec_perc > self.strictness: 
            # opposing player has good record so cooperate
            if random.randrange(0,self.accuracy,1) == self.accuracy - 1:
                return 1 # a mistake
            else:
                return 0
        else:
            if random.randrange(0,self.accuracy,1) == self.accuracy - 1:
                return 0 # a mistake
            else:
                return 1
    
    def bad_guy(self, bot_bot_id):        
        if random.randrange(0,self.goodness,1) == self.goodness - 1:
            return 1
        else:        
            rec_perc = self.record(bot_bot_id) 

            if rec_perc > self.strictness: 
                # opposing player has good record so cooperate
                if random.randrange(0,self.accuracy,1) == self.accuracy - 1:
                    return 1 # a mistake
                else:
                    return 0
            else:
                if random.randrange(0,self.accuracy,1) == self.accuracy - 1:
                    return 0 # a mistake
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
                

class ecosystem():  
    def __init__(self):
        self.bot_id = 0
        self.botlist = []        
        for i in range(5):
            self.add_bot(7) 
        for i in range(5):
            self.add_bot(8)               
        self.year = 0
    
    def add_bot(self,t):
        self.botlist.append(bot(self.bot_id, t))        
        self.bot_id += 1
        
    def scorer(self, b1, b2):
        # need to pass which bot we are playing against to get the strategy.
        if b1.get_strat(self.botlist.index(b2)) == 0 and b2.get_strat(self.botlist.index(b1)) == 0:
            b1.score += 1
            b2.score += 1
            b1.remember(self.botlist.index(b2), 0)
            b2.remember(self.botlist.index(b1), 0)
            
        if b1.get_strat(self.botlist.index(b2)) == 1 and b2.get_strat(self.botlist.index(b1)) == 0:
            b1.score += 3
            b1.remember(self.botlist.index(b2),  0)
            b2.remember(self.botlist.index(b1), 1)
        
        if b1.get_strat(self.botlist.index(b2)) == 1 and b2.get_strat(self.botlist.index(b1)) == 0:
            b2.score += 3       
            b1.remember(self.botlist.index(b2), 1)
            b2.remember(self.botlist.index(b1), 0)
            
        if b1.get_strat(self.botlist.index(b2)) == 1 and b2.get_strat(self.botlist.index(b1)) == 1:
            b1.remember(self.botlist.index(b2), 1)
            b2.remember(self.botlist.index(b1), 1)
        
    def evolve(self, n):
        
        while(True):
            for i in range(n):
                for j in self.botlist:
                    for k in self.botlist:
                        if j != k:
                            self.scorer(j,k) 
            self.year += 1
            self.output()
            self.grow()
            self.clear_mem()
            self.clear_score()
            
    def clear_mem(self):
        for i in self.botlist:
            i.init_mem()
    
    def clear_score(self):
        for i in self.botlist:
            i.score = 0

    def grow(self):
        # replicate winner
        # delete looser
        looser_bot = self.botlist[0]
        winner_bot = self.botlist[0]
        for x in self.botlist:
            if x.score < looser_bot.score:
                looser_bot = x
            
            if x.score > winner_bot.score:
                winner_bot = x            
        
        born_bot = copy.deepcopy(winner_bot)
        self.bot_id += 1
        born_bot.bot_id = self.bot_id
        if born_bot.memory_length <= 1:
            born_bot.memory_length += random.randrange(0,2,1)
        elif born_bot.memory_length > 1:
            born_bot.memory_length += random.randrange(-1,2,1)               
        
        born_bot.strictness += random.randrange(-5,6,1)               
        born_bot.accuracy += random.randrange(-1,2,1) 
        born_bot.goodness += random.randrange(-1,2,1) 
        self.botlist.append(born_bot)
    
        self.botlist.remove(looser_bot)
       
    def output(self):
        
        tot_mem      = 0
        tot_leniency = 0
        av_mem       = 0
        av_leniency  = 0
        
        for i in self.botlist:
            tot_mem      += i.memory_length
            tot_leniency += i.strictness
        
        av_mem      = float(tot_mem)      / float(len(self.botlist))
        av_leniency = float(tot_leniency) / float(len(self.botlist))
        print " ***** Year {0} ***** ".format(self.year)
        print "avcut {0} avmem {1}".format(av_leniency, av_mem)
        
        
        for aa in sorted(self.botlist, key=lambda bot: bot.score, reverse=True):
            
            print "bot: {0:4} memory {3:4} cuttoff {4:4} bad {6:5} error {5:5} stategy: {1:20} score: {2}".format(aa.bot_id, aa.strategy_names[aa.strategy], aa.score, aa.memory_length, aa.strictness, aa.accuracy, aa.goodness)

myeco = ecosystem()

myeco.evolve(100)
