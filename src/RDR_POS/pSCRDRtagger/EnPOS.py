# -*- coding: utf-8 -*-

# RDRPOSTagger
# A Ripple Down Rules-based Part-Of-Speech Tagging Toolkit
# http://rdrpostagger.sourceforge.net
# Copyright © 2013 by Dat Quoc Nguyen, Dai Quoc Nguyen, Dang Duc Pham, and Son Bao Pham

# Modified by:
# Rachel Kobayashi
# Aaron Anderson
#   with 
# Eric Gan
#
# An alternative Part of Speech Tagger
# only functions in class a necessary for using the POS. 
# other functions allow testing this specific file. 
#
# example useage:
# r = EnRDRTree();
# r.constructTreeFromRulesFile(model);
# DICT = readDictionary(lexicon);
# tagList = r.tagRawCorpus(DICT, line.strip())
#
# model is the path to the model: ../Trained/EN.RDR
# lexicon is the path to the dictionary: ../Trained/EN.DICT  (or EN.DICT)
# and line is the given string to be analysized. 

import os,sys,time

#Set Python & directory paths
#os.chdir("../")
sys.setrecursionlimit(100000)
sys.path.append(os.path.abspath(""))
#os.chdir("./pSCRDRtagger")

from RDR_POS.SCRDRlearner.PosTaggingRDRTree import PosTaggingRDRTree
from RDR_POS.Utility.Utils import getWordTag, getRawTextFromFile, readDictionary
from RDR_POS.SCRDRlearner.Object import FWObject
from RDR_POS.InitialTagger.EnInitialTagger import EnInitTagger4Corpus, EnInitTagger4Sentence


class EnRDRTree(PosTaggingRDRTree):
    """
    RDRPOSTagger for English
    """
    def __init__(self):
        self.root = None
    
    def tagRawSentence(self, DICT, rawLine):
        line = EnInitTagger4Sentence(DICT, rawLine)
        sen = ''
        startWordTags = line.split()
        for i in xrange(len(startWordTags)):
            fwObject = FWObject.getFWObject(startWordTags, i)
            word, tag = getWordTag(startWordTags[i])
            node = self.findFiredNode(fwObject)
            sen += node.conclusion + " "
        return sen.strip()
    
    def tagRawCorpus(self, DICT, inputStr):
        outStr = "";
        outStr += self.tagRawSentence(DICT, inputStr) + "\n";
        outList = outStr.split();
        #        print ""
        print outList;
        return outList;

## wrapper functions to test  and run the file as a test.
# useage: 
#   python EnPOS.py PATH-TO-TRAINED-MODEL PATH-TO-DICTIONARY PATH-TO-INPUT-CORPUS PATH-TO-OUTPUT-FILE
# 
# for instance:
#   python EnPOS.py ../Trained/EN.RDR ../Trained/EN.DICT ../testTagger.txt out.txt
"""
def findPOS(model, lexicon, inFile, outFile):
    r = EnRDRTree();
    r.constructTreeFromRulesFile(model);
    DICT = readDictionary(lexicon);
    inFH = open(inFile);
    outStr = "";
    for line in inFH:
        outStr += "["
        outStr += ", ".join(r.tagRawCorpus(DICT, line.strip()));
        outStr +=  "]\n";        
    inFH.close();
    outFH = open(outFile, 'w');
    outFH.write(outStr);
    return;

def runEnRDRPOSTagger():
    args = sys.argv[1:];
    argc = len(args);
    if argc < 3:
        print "ERROR: input\n";
    else:
        trainedModel = args[0];
        lexiconPath = args[1];
        inputFile = args[2];
        if argc >=3:
            outputFile = args[3];
        else:
            outputFile = "out.txt";
            #        DICT = readDictionary(lexiconPath);
        findPOS(trainedModel, lexiconPath, inputFile, outputFile);
        print "Done!"; 
       
if __name__ == "__main__":
    runEnRDRPOSTagger()
    pass

"""
