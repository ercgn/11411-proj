#!/usr/bin/python
#
# gen_ sent2q.py
#
# Given a sentence, this file will turn in into a question. 
#
# Rachel Kobayashi
#   with
# Aaron Anderson
# Eric Gan
#
#

import rdrpos,nltk
from combinations import Combine
from qutil import *

# "easy" cases to replace:
#   dates -> when
#   numbers -> how many [noun] [verb phrase]?
#   names / proper nouns

class ConstructQuestion:

    def formatQuestion(self, question):
        question = question.strip();
        # remove trailing period
        puncTag = rdrpos.pos_tag(question[-1]);
        if puncTag[0] == '.':
            question = question[0:len(question)-1];
        question += "?";
        return question;

    def make(self,sentence):
        c = Combine();
        print "MAKE2::",sentence;
        s_tokens = nltk.word_tokenize(sentence.strip());
        POS = rdrpos.pos_tag(sentence.strip());
        question = "";
        changeIDX = False;
        locations =  c.ID.findDates(s_tokens, POS);
        c.dates(s_tokens, POS, locations);
        print s_tokens;
        print POS;
#        question = self.formatQuestion(question);
        return question;

