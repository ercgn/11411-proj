# -*- coding: utf-8 -*-
from util.RDR_POS.SCRDRlearner.Object import Object

def isAbbre(word):
    word = unicode(word, "utf-8")
    for i in xrange(len(word)):
        if isVnLowerChar(word[i]) or word[i] == "_":
            return False
    return True

VNUPPERCHARS = [u'Ă', u'Â', u'Đ', u'Ê', u'Ô', u'Ơ', u'Ư']
VNLOWERCHARS = [u'ă', u'â', u'đ', u'ê', u'ô', u'ơ', u'ư']

def isVnLowerChar(char):
    if char.islower() or char in VNLOWERCHARS:
        return True;
    return False;

def isVnUpperChar(char):
    if char.isupper() or char in VNUPPERCHARS:
        return True;
    return False;

def isVnProperNoun(word):
    word = unicode(word, "utf-8")
    if (isVnUpperChar(word[0])):
        if word.count("_") >= 4:
            return True
        index = word.find("_")
        while index > 0:
            if isVnLowerChar(word[index + 1]):
                return False;
            index = word.find("_", index + 1)
        return True;
    else:
        return False;    

def getWordTag(wordTag):
    """
    Split word and tag from word/tag pair
    Example: good/JJ -> word: good, tag: JJ
    """

    if wordTag == "///":
        return "/", "/"
    index = wordTag.rfind("/")
    word = wordTag[:index].strip()
    #tag = wordTag[index +1:].lower().strip()
    tag = wordTag[index +1:].strip()
    return word, tag

def getObject(startWordTags, index):
    """
    Get an object associated to a word of the position 'index'
    """
    
    word, tag = getWordTag(startWordTags[index])
    preWord1 = preTag1 = preWord2 = preTag2 = "" #preWord3 = preTag3 = ""
    nextWord1 = nextTag1 = nextWord2= nextTag2= "" #nextWord3 = nextTag3 = ""
    
    if index > 0:
        preWord1, preTag1 = getWordTag(startWordTags[index - 1])
    if index > 1:
        preWord2, preTag2 = getWordTag(startWordTags[index - 2])
    #if index > 2:
        #preWord3, preTag3 = getWordTag(startWordTags[index - 3])
        
    if index < len(startWordTags) - 1:
        nextWord1, nextTag1 = getWordTag(startWordTags[index + 1]) 
    if index < len(startWordTags) - 2:
        nextWord2, nextTag2 = getWordTag(startWordTags[index + 2]) 
    #if index < len(startWordTags) - 3:
        #nextWord3, nextTag3 = getWordTag(startWordTags[index + 3])
         
    #object = Object(word, tag, preWord3, preWord2, preWord1, nextWord1, nextWord2, nextWord3, preTag3, preTag2, preTag1, nextTag1, nextTag2,nextTag3)
    object = Object(word, tag, preWord2, preWord1, nextWord1, nextWord2, preTag2, preTag1, nextTag1, nextTag2)
    return object
 
def getObjectDictionary(startStateFile, correctFile):
    """
    Build object dictionary
    - Key: pair of start/initialized tag and correct tag (startTag/initialized, correctTag)
    - Value: list of corresponding objects
    """
    
    startLines = open(startStateFile, "r").readlines()
    correctLines = open(correctFile, "r").readlines()
    objects = {}
    
    j = 0
    for i in xrange(len(startLines)):
        start = startLines[i].strip()
        if len(start) == 0:
            continue
        
        while j < len(correctLines) and correctLines[j].strip() == "":
            j += 1
            
        if j >= len(correctLines):
            continue
        
        correct = correctLines[j].strip()
        j += 1

        startWordTags = start.split()
        correctWordTags = correct.split()
        
        for k in xrange(len(startWordTags)):
            startWord, startTag = getWordTag(startWordTags[k])
            correctWord, correctTag = getWordTag(correctWordTags[k])
            
            if startWord != correctWord:
                print "Data not equal. Start state file line %d and correct file line %d" % (i, j)
                continue
            
            if startTag not in objects.keys():
                objects[startTag] = {}
                objects[startTag][startTag] = []
                
            if correctTag not in objects[startTag].keys():
                objects[startTag][correctTag] = []
                
            objects[startTag][correctTag].append(getObject(startWordTags, k))
                                                
            """
            if (startTag, correctTag) not in objects.keys():
                objects[(startTag, correctTag)] = [getObject(startWordTags, correctTag, k)]
            else:
                objects[(startTag, correctTag)].append(getObject(startWordTags, correctTag, k))
            """
            
    return objects


def getRawTextFromFile(inputFile, outFile):
    """
    Create raw corpus 'outFile' from golden tagged corpus 'inputFile'
    """
    
    out = open(outFile, "w")
    sents = open(inputFile, "r").readlines()
    for sent in sents:
        wordTags = sent.strip().split()
        for wordTag in wordTags:
            word, tag = getWordTag(wordTag)
            out.write(word + " ")
        out.write("\n")
    out.close()
    
def readDictionary(input):
    """
    Read file to a dictionary data structure:
    Input file is a lexicon consisting lines of the word and the most frequent associated tag 
    """
    
    dictionary = {}
    lines = open(input, "r").readlines()
    for line in lines:
        wordtag = line.strip().split()
        dictionary[wordtag[0]] = wordtag[1]
    return dictionary


if __name__ == "__main__":
    #getRawTextFromFile("../Sample/WSJ2224.txt", "../Sample/WSJ2224.Raw")
    pass
