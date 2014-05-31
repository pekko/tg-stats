#!/usr/bin/env python3.3
# coding: utf-8

from analyze import get_msgs

from collections import defaultdict
import itertools
import random
import re

class TgMarkov(object):
    START='\x01'
    STOP='\x02'

    def __init__(self, msgs):
        self.table = {}
        self.user_table = defaultdict(list)

        prev = None
        for m in msgs:
            if prev:
                self.user_table[m['name']].append(prev)
            prev = m['name']

        namefunc = lambda x: x['name']
        msgs = sorted(msgs, key=namefunc)
        for (k,g) in itertools.groupby(msgs, namefunc):
            self.table[k] = self.init_chain(g)
        
    def init_chain(self, msgs):
        chain = defaultdict(list)
        
        for m in msgs:
            text = m['msg'].replace('.', self.STOP)
            
            words = re.split('([\s\.,!\?])', text)
            words = (w.strip() for w in words)
            words = [w for w in words if w != '']
            
            chain[self.START].append(words[0])
            for i in range(len(words)-1):
                chain[words[i]].append(words[i+1])
            chain[words[-1]].append(self.STOP)

        return chain

    def run(self, length=10, user=None):
        if user == None:
            user = random.choice(list(self.table.keys()))

        s = ""
        for i in range(length):
            user = random.choice(self.user_table[user])
            chain = self.table[user]
            word = self.START

            s += "%s:" % (user)
            while word != self.STOP:
                word = random.choice(chain[word])
                if len(word) > 1:
                    s += ' '
                s += word
            s += "\n"
        return s

def main():
    msgs = get_msgs('output')
    markov = TgMarkov(msgs)
    print(markov.run(10))


if __name__ == '__main__':
    main()