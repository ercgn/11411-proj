#!/usr/bin/python
#
# util.py
#
# Class the contains general utility functions 
# used across all functions
#
# Rachel Kobayashi
#   with
# Aaron Anderson
# Eric Gan
#
# E: Can we merge this file wtih perhaps ntlk_helper.py? 
#    Or merge nltk_helper.py with this file? It's pretty much
#    the same thing. 

from collections import deque;
from copy import deepcopy;

# outputs the first n items in queue into a string;
def q2str(queue, n):
    copyQ = deepcopy(queue);
    tags = [];
    if len(queue) >= n:
        for count in range(0,n):
            tag = copyQ.popleft()
            tags.append(tag)
    outStr = " ".join(tags)
    return outStr;

# Checks if a POS tag refers to a verb
def is_verb(tag):
    return (tag[:1] == 'V')

# Checks if a POS tag refers to a noun
def is_noun(tag):
    return (tag[:1] == 'N')

def is_adj(tag):
    return (tag[:2] == "JJ")

def is_num(tag):
    return (tag[:2] == "CD")
