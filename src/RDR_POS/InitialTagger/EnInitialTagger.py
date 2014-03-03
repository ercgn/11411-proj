# -*- coding: utf-8 -*-
import re
from RDR_POS.Utility.Utils import readDictionary

def EnInitTagger4Sentence(FREQDICT, sentence):
    """
    Initial tagger for English sentence
    """
    
    words = sentence.strip().split()
    taggedSen = ''
    for word in words:
        lowerW = word.lower()
        if word in FREQDICT:
            taggedSen += word + "/" + FREQDICT[word] + " "
        elif lowerW in FREQDICT:
            taggedSen += word + "/" + FREQDICT[lowerW] + " "
        else:
            if (re.search(r"([0-9]+-)|(-[0-9]+)", word) != None):
                taggedSen += word + "/JJ "
            elif (re.search(r"[0-9]+", word) != None):
                taggedSen += word + "/CD "
            elif (re.search(r'(.*ness$)|(.*ment$)|(.*ship$)|(^[Ee]x-.*)|(^[Ss]elf-.*)', word) != None):
                taggedSen += word + "/NN "
            elif (re.search(r'.*s$', word) != None and word[0].islower()):
                taggedSen += word + "/NNS "
            elif (word[0].isupper()):
                taggedSen += word + "/NNP "
            elif(re.search(r'(^[Ii]nter.*)|(^[nN]on.*)|(^[Dd]is.*)|(^[Aa]nti.*)', word) != None):
                taggedSen += word + "/JJ "
            elif (re.search(r'.*ing$', word) != None and word.find("-") < 0):
                taggedSen += word + "/VBG "
            elif (re.search(r'.*ed$', word) != None and word.find("-") < 0):
                taggedSen += word + "/VBN "
            elif (re.search(r'(.*ful$)|(.*ous$)|(.*ble$)|(.*ic$)|(.*ive$)|(.*est$)|(.*able$)|(.*al$)', word) != None
                  or word.find("-") > -1):
                taggedSen += word + "/JJ "
            elif(re.search(r'.*ly$', word) != None ):
                taggedSen += word + "/RB "
            else:
                taggedSen += word + "/NN "                                        
    return taggedSen.strip()

def EnInitTagger4Corpus(FREQDICT, input, output):
    """
    Initial tagger for English corpus
    """
    lines = open(input, "r").readlines()
    fileOut = open(output, "w")
    for line in lines:
        fileOut.write(EnInitTagger4Sentence(FREQDICT, line) + "\n")
    fileOut.close     

if __name__ == "__main__":
    #FREQDICT = readDictionary("../Dicts/EN.DICT")
    #EnInitTagger4Corpus(FREQDICT, "../Sample/En/rawTest", "../Sample/En/rawTest.INIT")
    pass
