#!/usr/bin/python
#
# sent2q.py
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
        print "MAKE::",sentence;
        s_tokens = nltk.word_tokenize(sentence.strip());
        print s_tokens, len(s_tokens);
        # currently assumes the punctuation is separated by a space
        POS = rdrpos.pos_tag(sentence.strip());
        print POS, len(POS);
        question = "";
        changeIDX = False;
#        question = self.formatQuestion(question);
        return question;
"""
        for idx in range(1, len(POS)):
            prevTkn = POS[idx -1];
            token = POS[idx];        
            if prevTkn[:2] == "NN" and token[:1] == "V":
#                print prevTkn;
#                print s_tokens[idx-1], "\n";
                changeIDX = idx-1;
        for idx in range(0, len(s_tokens)):
            if changeIDX and changeIDX == idx:
                if idx == 0:
                    question += "What ";
                else: 
                    question += "what ";
            else:
                question += s_tokens[idx] + " ";    
        question = self.formatQuestion(question);
        return question;
"""
