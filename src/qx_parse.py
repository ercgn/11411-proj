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

# still need to figure out how to integrate the other parser:
# see comment thread: 
# http://stackoverflow.com/questions/279237/import-a-module-from-a-relative-path 
# other POS class in src/POStagger/pSCRDRtagger/EnPOS.py
# probably necessary since the nltk identitfies "Did" as a noun... 

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
    # R: for now, this seems pretty suficient in terms of nouns
    #    the verbs are a bit shakey though, leaving ambiguity
    verbs = [x[0] for x in pos_list if is_verb(x[1])]
    nouns = [x[0] for x in pos_list if is_noun(x[1])]

## combine words that are next to each other in the question 
## (probably a phrase)
#    nouns = combWords(nouns, q_tokens);
##
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

# Combines entries in 
def combWords(words, question):
    Q = len(question);
    combined = [];
    x = 0;
    while x < len(words):
        idx = question.index(words[x]);
        phrase = "";
        if idx < Q-1:
            y = 0;
            while x + y < len(words) and question[idx + y] == words[x + y]:
#                print idx + y,x + y;
                phrase += words[x + y] + " ";
                y+=1;
            combined.append(phrase.strip());
            x += y;
        else:
            combined.append(words[x]);
            x += 1;
    return combined;
