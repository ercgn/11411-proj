#!/usr/bin/python
#
# ans_q_parser.py
#
# Class which provides functionality to take a question about a document,
# phrased in English, and extract relevant parts for string matching or other
# methods of location within the document. Stores information about the question
# possibly used for constructin answer?
#
# Example usage:
# from ans_q_parser import QParser
# qInfo = QParser("What things did Aaron break today?");
# key_tokens = qInfo.find_keywords();
# print key_tokens
#
#
# Aaron Anderson
#   with
# Rachel Kobayashi
# Eric Gan
#
#


import nltk
import util.rdrpos as rdrpos
from util.qutil import *
from util.set_defs import Identity
import util.nltk_helper as nhelp

# Module Constants
# hidden if we only immport the class from this module?

WH_PRONOUN='WP'     # Tag for wh-pronouns such as who, what, which
WH_ADVERB='WRB'     # Tag for wh-adverbs such as where, when

# Extract key components of a question based on natural language understanding
# and return them as a list of tokens
#   q_str:  A string containing a fluent, well-structured English question,
#           such as "What country has the highest average elevation?"
# 


# NEW NOTES:
# I just turned this into a class beacuse I thought it might be helpful
# considering we have multiple questions and we want the same parsing
# this would allow us to save information about the current question
# but then move on when we're finished with answering it
# things to consider:
#   does this add unnessary overhaed?
#   does this actually make things simpler? 

class QParser(object):
    def __init__(self, question):
        # E: Let's create a list of generic verbs that we don't want to include
        # This can be expanded.

        self.ignoredWords = set(["are", "did", "does", "do", "is", "was", "many"])

        self.qstr = question
        self.qtok = nltk.word_tokenize(question)
        self.qpos = rdrpos.pos_tag(question)
        self.qset = zip(self.qtok, self.qpos)

    def print_question(self):
        print "\n", self.qstr
        print self.qtok
        print self.qpos, "\n"

    def asking_what(self):
        idSets = Identity()
        qwords = []
        for idx, tok in enumerate(self.qtok):
            if idSets.isQuestionWord(tok):
                qwords += (tok,idx)
        self.qust = qwords
        return qwords

    def get_tokens(self):
        return self.qtok

    def find_keywords(self):

        # Tokenize the question and tag with part of speech
        pos_list = self.qset
        #    q_tokens = nltk.word_tokenize(q_str)
        #    pos_list = nltk.pos_tag(q_tokens)

    
        # build a dictionary mapping POS tags to a list of words with that tag
        pos_dict = {}

        for pair in pos_list:
            # pair[0] is the word, pair[1] is the associated tag
            if pair[1] in pos_dict:
                pos_dict[pair[1]] += [pair[0]]
            else:
                pos_dict[pair[1]] = [pair[0]]

        # TODO: refine this part
        # Extract relevant parts (key tokens) of the question
        # For now, return all nouns and verbs
        # R: for now, this seems pretty suficient in terms of nouns
        #    the verbs are a bit shakey though, leaving ambiguityA

        verbs = [x for x in pos_list if is_verb(x[1])]
        nouns = [x for x in pos_list if is_noun(x[1])]
        adjs = [x for x in pos_list if is_adj(x[1])]
        nums = [x for x in pos_list if is_num(x[1])]

        # Remove insignificant verbs
        toRemove = []
        for word in self.ignoredWords:
            for tup in verbs:
                if word == tup[0]: 
                    toRemove.append(tup)
        for tup in toRemove:
            verbs.remove(tup)

        #Add synonyms: only to verbs (maybe adjectives?)
        allSynonyms = []
        # for tup in verbs:
        #     allSynonyms += map(
        #         lambda x: (x, tup[1]), nhelp.getSynonyms(tup[0]))

        # #Add synonyms: to adjs too!
        # for tup in adjs:
        #     allSynonyms += map(
        #         lambda x: (x, tup[1]), nhelp.getSynonyms(tup[0]))


        # Simple but slow duplicate-remover. 

        key_tokens = verbs + nouns + adjs + nums + allSynonyms
        key_tokens = list(set(key_tokens))

        # Remove insignificant words
        toRemove = []
        for word in self.ignoredWords:
            for tup in key_tokens:
                if word.lower() == tup[0].lower(): 
                    toRemove.append(tup)
        for tup in toRemove:
            key_tokens.remove(tup)

        self.verbs = verbs
        self.nouns = nouns
        self.adjs = adjs
        self.keyTok = key_tokens

#    if WH_PRONOUN in pos_dict:
#        # get the word following the wh-pronoun
#        ref_noun = \
#            pos_list[ pos_list.index((pos_dict[WH_PRONOUN][0],WH_PRONOUN)) + 1 ] 
#        key_tokens += [ref_noun]
    
        return key_tokens

# For testing. Will not run unless we directly call 
# python ans_q_parser.py
if __name__ == '__main__':
    qInfo = QParser("What things did Aaron break today?")
    key_tokens = qInfo.find_keywords()
    test = qInfo.asking_what()
    print key_tokens
    print test
