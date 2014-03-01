import os, sys

from copy import deepcopy
import rdrpos;

class ConstructQuestions:

    def make(self,sentence):

        s_tokens = sentence.strip().split();
        POS = rdrpos.pos_tag(sentence.split());
        print s_tokens;
        print POS, "\n";
        question = "";
        
        for idx in range(1, len(POS)):
            prevTkn = POS[idx -1];
            token = POS[idx];        
            if prevTkn[:2] == "NN" and token[:1] == "V":
#                print prevTkn;
#                print s_tokens[idx-1], "\n";
                changeIDX = idx-1;
        for idx in range(0, len(s_tokens)):
            if changeIDX == idx:
                if idx == 0:
                    question += "What ";
                else: 
                    question += "what ";
            else:
                question += s_tokens[idx] + " ";
            
        question = question.strip();
        question += "?";
        return question;

def parseSentences():
    questions = ConstructQuestions()
    args = sys.argv[1:];
    argc = len(args);
    if argc < 1:
        print "ERROR: input arguments\n";
        exit();
    inputFile = args[0];
    inFH = open(inputFile);
    for line in inFH:
        if line != "\n":
#            outQ = questions.make(line);
            POS = rdrpos.pos_tag(line);
            print POS;
    inFH.close();
    return;

if __name__ == "__main__":
    parseSentences();
    pass
