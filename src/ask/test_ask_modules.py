#
# gen_makeQuestions.py
#
# module to test the question creation parser. 
#




import os, sys

from sent_2_q import ConstructQuestion
from util.combinations import Combine

def parseSentences():
    args = sys.argv[1:];
    argc = len(args);
    if argc < 1:
        print "ERROR: input arguments\n";
        exit();
    inputFile = args[0];
    inFH = open(inputFile);
    for line in inFH:
        if line != "\n":
            questions = ConstructQuestion(line);
            outQ = questions.out;
            print line, outQ, "\n";
    inFH.close();
    return;

if __name__ == "__main__":
    parseSentences();
    pass
