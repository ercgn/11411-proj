#!/usr/bin/python
#
# answer.py
#
# Main driver for question answering robot.  
#
# Eric Gan
#   with
# Aaron Anderson
# Rachel Kobayashi
#
#

import nltk
import util.rdrpos
import random, sys
import util.nltk_helper as nhelp
from util.article_parser import MyHTMLParser
from answer.q_parser import QParser

DEBUG = 0

#HEURISTIC:
# The purpose of the heuristic is to put a weight to certain key words based
# on their importance. This heuristic ranks nouns and proper nouns higher than
# other parts of speeches, like verbs and adjectives. 
NOUN_SCORE = 2
VERB_SCORE = 1
ADJ_SCORE = 1


class Answer(object):
    def __init__(self, articlefd, questionfd):
        #When we initialize, we first parse the article file.
        Parser = MyHTMLParser()
        buf = articlefd.read()
        Parser.feed(buf)

        #variables
        articleTitle = Parser.grabTitle()
        articleTitleList = nltk.word_tokenize(articleTitle)

        self.titleList = filter(str.isalnum, articleTitleList) 
        self.sList = Parser.grabTextSentenceList()
        self.articlefd = articlefd
        self.questionfd = questionfd

        self.yesList = ["Yes.", "Absolutely!", "Positive!", "Yes sir.", 
                        "Of course!", "Uh-huh.", "Definitely.", "Affirmative.", 
                        "Obviously. You think it's raining nyan cats?"]
        self.noList = ["No.", "Negative.", "Absolutely not!", "No sir.", 
                        "Of course not!", "Nope.", "Not at all."]

        self.qType = None

    def bestAnswer(self, keyWordList):
        # This is the main algorithm for finding an answer in the article file
        # by counting the amount of times key words appear in the sentence, and
        # returning the sentence that has the maximum count. 
        maxMatch = 0
        bestSentence = None
        for sentence in self.sList:
            keyWordCount = 0
            stok = nltk.word_tokenize(sentence.lower())

            for i in xrange(len(keyWordList)):
                for j in xrange(len(stok)):
                    if nhelp.hasSameStem(keyWordList[i], stok[j]):
                        keyWordCount += 1
                        break
            if keyWordCount > maxMatch:
                maxMatch = keyWordCount
                bestSentence = sentence
        return bestSentence

    def genYes(self):
        i = random.randint(0, len(self.yesList)-1)
        return self.yesList[i]

    def genNo(self):
        i = random.randint(0, len(self.noList)-1)
        return self.noList[i]

    def printSentenceInfo(self, sentence):
        print "Printing word information of current sentence..."
        print nltk.word_tokenize(sentence)
        print rdrpos.pos_tag(sentence)

    def answerHowMany(self, keyWordList):
        return self.bestAnswer(keyWordList)

    def answerWho(self, keyWordList):
        return self.bestAnswer(keyWordList)

    def answerWhere(self, keyWordList):
        return self.bestAnswer(keyWordList)

    def answerWhen(self, keyWordList):
        return self.bestAnswer(keyWordList)

    def answerWhat(self, keyWordList):
        return self.bestAnswer(keyWordList)

    def answerYesNo(self, keyWordList, qtok):
        answer = None
        if self.bestAnswer(keyWordList) != None:
            if qtok.count("not") % 2:
                answer = self.genNo()
            else:
                answer = self.genYes()
        else:
            if qtok.count("not") % 2:
                answer = self.genYes()
            else:
                answer = self.genNo()
        return answer

    def answerMisc(self, keyWordList):
        return self.answerWhat(keyWordList)

    def driver(self):
        #read first question
        curQ = self.questionfd.readline()
        if curQ.strip() == "":
            print "There are no questions in the question file!"
            return
        
        while curQ != "":
            if curQ.strip() == "": break
            print "Q:", curQ
            answer = None

            qInfo = QParser(curQ)
            qtok = map(str.lower, qInfo.get_tokens())
            questionList = map(str.lower, 
                filter(lambda x: type(x) == str, qInfo.asking_what()))

            #E: Words in the article title should not be key words since
            #   the whole article is about the topic anyways. So I decided
            #   to remove them.
            keyWordGroup = qInfo.find_keywords()
            keyWordList, posTag = zip(*keyWordGroup)
            keyWordList = list(keyWordList)
            posTag = list(posTag)

            for word in self.titleList:
                if word in keyWordList:
                    posTag.pop(keyWordList.index(word))
                    keyWordList.remove(word)
                if word.lower() in keyWordList:
                    posTag.pop(keyWordList.index(word.lower()))
                    keyWordList.remove(word.lower()) 

            #TODO: Write synonym generator here (or put them in ans_q_parser?)

            # modify keyword List
            if DEBUG: print "Key Words (before): ", keyWordList, "\n" 

            #if we care about capitalization, comment this line
            keyWordList = map(str.lower, keyWordList)

            #if we don't want to stem key words, comment this line.
            keyWordList = list(set(map(nhelp.getStem, keyWordList)))

            if DEBUG: print "Key Words (after): ", keyWordList, "\n" 

            if "How many" in curQ or "how many" in curQ:
                self.qType = "How many"
                answer = self.answerHowMany(keyWordList)
            elif "who" in questionList:
                self.qType = "Who"
                answer = self.answerWho(keyWordList)
            elif "where" in questionList:
                self.qType = "Where"
                answer = self.answerWhere(keyWordList)
            elif "when" in questionList:
                self.qType = "When"
                answer = self.answerWhen(keyWordList)
            elif "what" in questionList:
                self.qType = "What"
                answer = self.answerWhat(keyWordList)
            elif "is" in questionList or "was" in questionList:
                self.qType = "Yes/No"
                answer = self.answerYesNo(keyWordList, qtok)
            else:
                self.qType = "Misc"
                answer = self.answerMisc(keyWordList)

            if DEBUG: print "'%s' question!" % (self.qType)

            print "A:", answer, "\n"

            curQ = self.questionfd.readline()


if __name__ == '__main__':

    def printUsage():
        print "Usage: python %s [articlefile] [quesitonfile]" % (sys.argv[0])
        print "Ex. python %s ../data/set2/a4.htm ../testQ/aries_easy.txt" % (sys.argv[0])

    if len(sys.argv) != 3:
        printUsage()
        exit(0)
        
    articlefd = open(sys.argv[1], "r")
    questionfd = open(sys.argv[2], "r")

    a = Answer(articlefd, questionfd)
    
    a.driver()
    
    articlefd.close()
    questionfd.close()
    
