#!/usr/bin/env python3.3
# coding: utf-8

import random

def is_vowel(char):
    return char.lower() in 'aeiouyåäö'
def is_cons(char):
    return char.lower() in 'qwrtpsdfghjklzxcvbnm'

def filter_pos(func, target):
    return (i for (i,v) in enumerate(map(func, target)) if v)

def swap_filtered(text, func):
    pos = list(filter_pos(func, text))
    (pos1, pos2) = random.sample(pos, 2)
    if pos1 > pos2:
        (pos1, pos2) = (pos2, pos1)
    return text[:pos1] + text[pos2] + text[pos1+1:pos2] + text[pos1] + text[pos2+1:]

def alter_little(text, *, seed=None):
    random.seed(seed)
    for i in range(random.randint(1,3)):
        if random.randint(0,1) == 0:
            text = swap_filtered(text, is_vowel)
        else:
            text = swap_filtered(text, is_cons)
    random.seed(None)
    return text

def main():
    s = "Pekko Lipsanen"
    print(alter_little(s).title())


if __name__ == '__main__':
    main()