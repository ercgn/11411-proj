# -*- coding: utf-8 -*-
#import re

def InitTagger4Sentence(FREQDICT, sentence):
    """
    Dictionary-based initial tagger for a particular language.
    Labeling a sentence.
    """
    
    words = sentence.strip().split()
    taggedSen = ''
    for word in words:
        if word in FREQDICT:
            taggedSen += word + "/" + FREQDICT[word] + " "
        else:
            """
            # Deal with unknown words (out-of-dictionary words): 
            # Providing several heuristics to deal those cases for your own language.
            #...................................
            """
            taggedSen += word + "/" + FREQDICT["DefaultTag"] + " "
                                                 
    return taggedSen.strip()

def InitTagger4Corpus(FREQDICT, input, output):
    """
    Dictionary-based initial tagger for a particular language.
    Labeling a corpus...
    """
    
    lines = open(input, "r").readlines()
    fileOut = open(output, "w")
    for line in lines:
        fileOut.write(InitTagger4Sentence(FREQDICT, line) + "\n")
    fileOut.close     
        
if __name__ == "__main__":
    pass
