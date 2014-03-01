import os, sys

import rdrpos
from combinations import Combine

class ConstructQuestions:
    def formatQuestion(self, question):
        question = question.strip();
        # remove trailing period
        puncTag = rdrpos.pos_tag(question[-1]);
        if puncTag[0] == '.':
            question = question[0:len(question)-1];
        question += "?";
        return question;

    def make(self,sentence):
        s_tokens = sentence.strip().split();
        POS = rdrpos.pos_tag(sentence.strip() );
        question = "";
        changeIDX = False;
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

def parseSentences():
    questions = ConstructQuestions()
    c = Combine();
    args = sys.argv[1:];
    argc = len(args);
    if argc < 1:
        print "ERROR: input arguments\n";
        exit();
    inputFile = args[0];
    inFH = open(inputFile);
    for line in inFH:
        if line != "\n":
            outQ = questions.make(line);
            c.dates(line);
            print outQ;
    inFH.close();
    return;

if __name__ == "__main__":
    parseSentences();
    pass
