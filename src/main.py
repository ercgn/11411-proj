import nltk
import sys
from parser import MyHTMLParser
import nltk_helper

def driver(articlefd, testfd):
    
    if testfd == "":
        print "Warning: Test file not implemented yet!"
    
    Parser = MyHTMLParser()
    buf = articlefd.readline()
    while buf != "":
        Parser.feed(buf)
        buf = articlefd.readline()
    
    #print "List of topics:"
    #print Parser.grabTopicList()
    #
    #print "Topic Dict"
    #print Parser.grabTopicSentenceDict()
    #
    #print "Article List"
    sList = Parser.grabTextSentenceList()
    
    #To be changed
    keyWordList = ["academy", "award", "awards", "win", "won"]
   
    word = "happiness"
    print nltk_helper.getStem(word)

    maxMatch = 0
    bestSentence = ""
    for sentence in sList:
        keyWordCount = 0
        for word in keyWordList:
            if word in set(sentence.lower().split(" ")):
                keyWordCount += 1
        if keyWordCount > maxMatch:
            maxMatch = keyWordCount
            bestSentence = sentence
    
    print bestSentence
    

if __name__ == '__main__':
    
    #CURRENT USAGE: "python main.py [articleFile]"
    #This block of code will need to change if we modify the usage. 
    if len(sys.argv) != 2:
        print "    Usage:",
        print "python %s [articleFile]" % (sys.argv[0])
        print "    Ex. python %s ../data/set4/a1.htm" % (sys.argv[0])
        exit(0)
    
    ARTICLE_FILE = sys.argv[1]
    articlefd = open(ARTICLE_FILE, "r")
    testfd = "" #To be modified
    
    driver(articlefd, testfd)
    
    articlefd.close()
