import os, sys
os.chdir("../")
sys.setrecursionlimit(100000)
sys.path.append(os.path.abspath(""))
os.chdir("./Utility")
from Utility.Utils import getWordTag

def compare(taggedCorpus, goldenCorpus):
    """
    To calculate the the performance on POS tagging
    """
    outputTokens = open(taggedCorpus, "r").read().split()
    standardTokens = open(goldenCorpus, "r").read().split()
    if len(outputTokens) != len(standardTokens):
        print "The numbers of tokens are not equal!"
        return 0
    numwords = 0
    count = 0
    for i in xrange(len(outputTokens)):
        numwords += 1
        word1, tag1 = getWordTag(outputTokens[i])
        word2, tag2 = getWordTag(standardTokens[i])        
        if word1 != word2:
            print "Data not equal in position", i
            print outputTokens[i], standardTokens[i-1], standardTokens[i], standardTokens[i+1]
            return 0
        if tag1.lower() == tag2.lower():
            count += 1
        #else:
        #   print outputTokens[i-1], outputTokens[i], outputTokens[i+1], "<=>", standardTokens[i-1], standardTokens[i], standardTokens[i+1]
    return count * 100 / float(len(outputTokens))

if __name__ == "__main__":
    print compare(sys.argv[1:][0], sys.argv[1:][1]), "%"
    pass
    