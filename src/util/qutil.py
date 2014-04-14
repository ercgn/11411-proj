#!/usr/bin/python
#
# util.py
#
# Class the contains general utility functions 
# used across all functions
#
# Rachel Kobayashi
# Aaron Anderson
#   with
# Eric Gan
#
# E: Can we merge this file wtih perhaps ntlk_helper.py? 
#    Or merge nltk_helper.py with this file? It's pretty much
#    the same thing. 

from collections import deque;
from copy import deepcopy;

import set_defs as sd
import util.rdrpos as rdrpos;

import nltk;

# constants
#DATE_TAG = "#DATE";

# Minimum number of tokens required in a sentence to turn it into a question
MIN_SENTENCE_LENGTH = 10

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

def is_propN(tag):
    return (tag == "NNP");

# E: Custom Tags used for the answering driver.
def is_syn(tag):
    return (tag == "SYN")

def is_custom(tag):
    return (tag == "CST")

def is_high_priority(tag):
    return (tag == "HGH")

# outputs the lowercase version of a word
# if the word tag does not depend on capitalization
# also automatically changes adverbs to lowercase
# in the case of "However, Finally",etc
def wordToLower(word):
    tagU = rdrpos.pos_tag(word);
    tagl = rdrpos.pos_tag(word.lower());
    if tagU == tagl:
        return word.lower();
    if tagU == "RB" or tagl == "RB":
        return word.lower();
    return word;

# takes an input as returns as a list
# if the input is already a list, will return input
# otherwise, will turn into a list, so we can do consistent
# appending / joining
def makeList(inputPhrase):
    if isinstance(inputPhrase, list):
        return inputPhrase;
    else:
        return [inputPhrase];

# Returns True if the string s can reasonably be described as a sentence
# There are many metrics to decide whether a string is a sentence;
# including length, containing a verb, end punctuation, etc.  The function
# will only return True if each implemented criteria is satisfied.
def isSentence(s):
    # Get the tokens of the sentence.  It's possible there are none,
    # in which case this is definitely not a sentence.
    toks = nltk.word_tokenize(s)
    if len(toks) == 0:
        return False
    
    # Generate the POS tags for the words in the sentence
    tags = rdrpos.pos_tag(s)
    
    # Check for existence of verb
    hasVerb = reduce(lambda x,y: x or y, map(is_verb, tags))
    
    # Check for a reasonable length
    isMinLength = (len(toks) > MIN_SENTENCE_LENGTH)
    
    # Check for correct end punctuation
    i = sd.Identity()
    hasEndPunct = i.isEndPhrasePunc(toks[-1])
    
    # Must have all criteria to be deemed a reasonable sentence
    return hasVerb and isMinLength and hasEndPunct

