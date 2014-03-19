#
# gen_makeQuestions.py
#
# module to test the question creation parser. 
#




import os, sys

from sent2q import ConstructQuestion
from util.combinations import Combine

def parseSentences():
    questions = ConstructQuestion()
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
            print line, outQ, "\n";
    inFH.close();
    return;

if __name__ == "__main__":
    parseSentences();
    pass
