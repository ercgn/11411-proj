#!/usr/bin/python
#
# qx_parse
#
# Module which provides functionality to take a question about a document,
# phrased in English, and extract relevant parts for string matching or other
# methods of location within the document.
#
# Example usage:
# import qx_parse
# key_tokens = qx_parse.parse_question("What things did Aaron break today?")
# print key_tokens
#
# Eric Gan
# Rachel Kobayashi
# Aaron Anderson
#
# 

import nltk

# Module Constants

WH_PRONOUN='WP'     # Tag for wh-pronouns such as who, what, which
WH_ADVERB='WRB'     # Tag for wh-adverbs such as where, when

# Extract key components of a question based on natural language understanding
# and return them as a list of tokens
#   q_str:  A string containing a fluent, well-structured English question,
#           such as "What country has the highest average elevation?"
# 
def parse_question(q_str):
    
    # Tokenize the question and tag with part of speech
    q_tokens = nltk.word_tokenize(q_str)
    pos_list = nltk.pos_tag(q_tokens)
    
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
    verbs = [x[0] for x in pos_list if is_verb(x[1])]
    nouns = [x[0] for x in pos_list if is_noun(x[1])]
    key_tokens = verbs + nouns
    
#    if WH_PRONOUN in pos_dict:
#        # get the word following the wh-pronoun
#        ref_noun = \
#            pos_list[ pos_list.index((pos_dict[WH_PRONOUN][0],WH_PRONOUN)) + 1 ] 
#        key_tokens += [ref_noun]
    
    return key_tokens

# Checks if a POS tag refers to a verb
def is_verb(tag):
    return (tag[:1] == 'V')

# Checks if a POS tag refers to a noun
def is_noun(tag):
    return (tag[:1] == 'N')

