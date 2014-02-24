import nltk
import sys
from parser import MyHTMLParser

def driver(articlefd, testfd):
    
    if testfd == "":
        print "Warning: Test file not implemented yet!"
    
    Parser = MyHTMLParser()
    buf = articlefd.readline()
    while buf != "":
        Parser.feed(buf)
        buf = articlefd.readline()
    
    print Parser.grabText()

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
