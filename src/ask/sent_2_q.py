#!/usr/bin/python
#
# gen_sent2q.py
#
# Given a sentence, this class can be used to turn the sentence into a question
#
# Rachel Kobayashi
#   with
# Aaron Anderson
# Eric Gan
#
#

import util.rdrpos as rdrpos
import nltk
from util.combinations import Combine
from util.qutil import *

# "easy" cases to replace:
#   dates -> when
#   numbers -> how many [noun] [verb phrase]?
#   names / proper nouns

class ConstructQuestion:
    def __init__(self):
        self.c = Combine();

    # TODO: change order so the question flows more naturally
    def formatQuestion(self, question):
        question = question.strip();
        # remove trailing period
        puncTag = rdrpos.pos_tag(question[-1]);
        if puncTag[0] == '.':
            question = question[0:len(question)-1];
        question += "?";
        return question;


    # creates question by replacing the first date
    # replaces with "what" or "what date" instead of "when" 
    # because that seems to work better grammatically most of the time
    def qFromDate(self,tok,POS, origN):
        if "#DATE" in set(POS):
            idx = POS.index("#DATE");
            if idx < len(tok)-1 and POS[idx+1] == "IN":
                tok[idx] = "when";
            elif idx > 0 and is_verb(POS[idx-1]):
                    tok[idx] = "what";
            else:
                tok[idx] = "what date";
            return self.c.sentJoin(tok);
        else:
            return "";

    # creates a question by replacing the first noun with "what"
    def qFromNoun(self,tok,POS):
        for i,tag in enumerate(POS):
            if is_noun(tag):
                tok[i] = "what";
                return self.c.sentJoin(tok);
        return "";

    def make(self,sentence):
        combi = self.c

        toks = nltk.word_tokenize(sentence.strip());
        POS = rdrpos.pos_tag(sentence.strip());
        N = len(toks);

        # find date locations and replace them in the given, toks, POS
        combi.dates(toks, POS);

        # check for context based on timing (might require change of verb)
        timeFlag = combi.ID.isTimeDep(toks,0);
        print timeFlag;

#        print toks;
#        print POS;
        question = self.qFromDate(toks,POS,N);
        if question != "":
            question = self.formatQuestion(question);        
            return question;
        question = self.qFromNoun(toks,POS);
        if question != "":
            question = self.formatQuestion(question);
            return question;
        return question;

