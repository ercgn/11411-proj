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


import nltk, rdrpos
from qutil import *;
from set_defs import Identity;

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

class QParser:
    def __init__(self, question):
        self.qstr = question;
        self.qtok = nltk.word_tokenize(question);
        self.qpos = rdrpos.pos_tag(question);
        self.qset = zip(self.qtok, self.qpos);

    def print_question(self):
        print "\n", self.qstr;
        print self.qtok;
        print self.qpos, "\n";

    def asking_what(self):
        idSets = Identity();
        qwords = [];
        for idx, tok in enumerate(qtok):
            if idSets.isQuestionWord(tok):
                qwords += (tok,idx);
        self.qust = qwords;
        return qwords;

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
        #    the verbs are a bit shakey though, leaving ambiguity
        verbs = [x[0] for x in pos_list if is_verb(x[1])]
        nouns = [x[0] for x in pos_list if is_noun(x[1])]
        

        key_tokens = verbs + nouns
        self.verbs = verbs;
        self.nouns = nouns;
        self.keyTok = key_tokens;

#    if WH_PRONOUN in pos_dict:
#        # get the word following the wh-pronoun
#        ref_noun = \
#            pos_list[ pos_list.index((pos_dict[WH_PRONOUN][0],WH_PRONOUN)) + 1 ] 
#        key_tokens += [ref_noun]
    
        return key_tokens
