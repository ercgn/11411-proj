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
# TODO: Make a specialized <li> list set for articles that have lists.

import nltk, copy
import util.rdrpos
import util.qutil as qutil
import random, sys
import util.nltk_helper as nhelp
from util.article_parser import MyHTMLParser
from answer.q_parser import QParser

#Various flags. 0 = False. 1 = True
DEBUG = 0
VERBOSE = 0 #More print statements
USE_HEURISTIC = 1 #Keep at 1, as the non-heuristic code is mostly deprecated.

#HEURISTIC:
# The purpose of the heuristic is to put a weight to certain key words based
# on their importance. This heuristic ranks nouns and proper nouns higher than
# other parts of speeches, like verbs and adjectives.
CUSTOM_SCORE = 7
NUM_SCORE = 5
NOUN_SCORE = 5
VERB_SCORE = 3
ADJ_SCORE = 3
SYN_SCORE = 1

class Answer(object):
    def __init__(self, articlefd, questionfd):
        #When we initialize, we first parse the article file.
        Parser = MyHTMLParser()
        buf = articlefd.read()
        Parser.feed(buf)
        
        #variables
        articleTitle = Parser.grabTitle()
        articleTitleList = nltk.word_tokenize(articleTitle)

        self.titleList = map(str.lower,filter(str.isalnum, articleTitleList))
        self.sList = Parser.grabTextSentenceList()
        self.articlefd = articlefd
        self.questionfd = questionfd

        self.yesList = ["Yes.", "Absolutely!", "Positive!", "Yes sir.", 
                        "Of course!", "Uh-huh.", "Definitely.", "Affirmative.", 
                        "Most definitely, yo!"]
        self.noList = ["No.", "Negative.", "Absolutely not!", "No sir.", 
                        "Of course not!", "Nope.", "Not at all.", "Naw, yo!"]
        
        #Preposition list (primarily for answering where questions)
        self.prepList = ["behind", "below", "beneath", "between",
                         "inside", "outside", "underneath"]
        #In the english language, numbers between 1-11 are written out.
        self.numList = ["one", "two", "three", "four", "five", "six", "seven",
                        "eight", "nine", "ten", "eleven"]
        
        self.qType = None
        self.keyWordList = None
        self.qtok = None
        self.posTag = None
        self.findSynonyms = []

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

    def bestAnswer2(self, keyWordList):
        #Includes the heuristic
        maxScore = 0
        bestSentence = None
        for sentence in self.sList:
            curScore = 0
            stok = nltk.word_tokenize(sentence.lower())
            for i in xrange(len(keyWordList)):
                tag = self.posTag[i]
                for j in xrange(len(stok)):
                    if nhelp.hasSameStem(keyWordList[i], stok[j]):
                        if qutil.is_noun(tag):
                            curScore += NOUN_SCORE
                        elif qutil.is_adj(tag):
                            curScore += ADJ_SCORE
                        elif qutil.is_verb(tag):
                            curScore += VERB_SCORE
                        elif qutil.is_syn(tag):
                            curScore += SYN_SCORE
                        elif qutil.is_num(tag):
                            curScore += NUM_SCORE
                        elif qutil.is_custom(tag):
                            curScore += CUSTOM_SCORE
                        else:
                            print "ERROR: No matching tag. for %s. Please tell Eric" % (tag)
                        #E: If we want to count multiple occurances of words in
                        # the sentence, remove this break line (might be a
                        # good idea in this function)
                        # Edit: nevermind. It still hyperinflates sentences that
                        # use synonyms of words extensively.
                        break
            #E: added this line to make the score proportional to the length
            # of the sentence. Adds fairness.
            if DEBUG and VERBOSE and curScore != 0:
                print sentence
                print curScore
            if curScore > maxScore:
                maxScore = curScore
                bestSentence = sentence
        if DEBUG: print "MaxScore:", maxScore
        if maxScore <= 2:
            #insignificant match: controls misfires with synonyms
            return None
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
        #Increase the numeric score
        pos = ["JJS" for i in xrange(len(self.numList))]
        keyWordList += self.numList
        self.posTag += pos
        answer = None
        if USE_HEURISTIC:
            answer = self.bestAnswer2(keyWordList)
        else:
            answer = self.bestAnswer(keyWordList)
        return answer

    def answerWho(self, keyWordList):
        if USE_HEURISTIC:
            return self.bestAnswer2(keyWordList)
        else:
            return self.bestAnswer(keyWordList)

    def answerWhere(self, keyWordList):
        # Add more key words:
        for word in keyWordList:
            if nhelp.hasSameStem("locate", word):
                pos = ["CST" for i in xrange(len(self.prepList))]
                keyWordList += self.prepList
                self.posTag += pos
                break
        if USE_HEURISTIC:
            return self.bestAnswer2(keyWordList)
        else:
            return self.bestAnswer(keyWordList)

    def answerWhen(self, keyWordList):
        if USE_HEURISTIC:
            return self.bestAnswer2(keyWordList)
        else:
            return self.bestAnswer(keyWordList)

    def answerWhat(self, keyWordList):
        if USE_HEURISTIC:
            return self.bestAnswer2(keyWordList)
        else:
            return self.bestAnswer(keyWordList)

    def answerYesNo(self, keyWordList):
        answer = None
        if USE_HEURISTIC:
            answer = self.bestAnswer2(keyWordList)
        else:
            answer = self.bestAnswer(keyWordList) 
        if answer != None:
            if self.qtok.count("not") % 2:
                answer = self.genNo()
            else:
                answer = self.genYes()
        else:
            if self.qtok.count("not") % 2:
                answer = self.genYes()
            else:
                answer = self.genNo()
        return answer

    def answerMisc(self, keyWordList):
        return self.answerWhat(keyWordList)
    
    def removeDuplicate(self, keyWordGroup):
        #improve this: complexity is O(n^2)
        kwGroupCpy = copy.deepcopy(keyWordGroup)
        toRemove = []
        for i in xrange(len(keyWordGroup)):
            word1 = keyWordGroup[i][0]
            tag1 = keyWordGroup[i][1]
            for j in xrange(i+1, len(keyWordGroup)):
                word2 = keyWordGroup[j][0]
                tag2 = keyWordGroup[j][1]
                if word1 == word2:
                    if qutil.is_syn(tag1):
                        if keyWordGroup[i] not in toRemove:
                            toRemove.append(keyWordGroup[i])
                    else:
                        if keyWordGroup[j] not in toRemove:
                            toRemove.append(keyWordGroup[j])
        for item in toRemove:
            keyWordGroup.remove(item)
        return keyWordGroup
    
    def driver(self):
        #read first question
        curQ = self.questionfd.readline()
        if curQ.strip() == "":
            print "There are no questions in the question file!"
            return
        
        while curQ != "":
            curQ = curQ.strip()
            if curQ == "": break
            print "Q:", curQ
            answer = None

            qInfo = QParser(curQ)
            self.qtok = map(str.lower, qInfo.get_tokens())
            questionList = map(str.lower, 
                filter(lambda x: type(x) == str, qInfo.asking_what()))

            #E: Words in the article title should not be key words since
            #   the whole article is about the topic anyways. So I decided
            #   to remove them.
            keyWordGroup = qInfo.find_keywords()
            keyWordGroup = map(lambda x: (x[0].lower(), x[1]), keyWordGroup)
            keyWordGroup = filter(lambda x: x[0] not in self.titleList,
                                keyWordGroup)
            
            # Synonym Generator code
            kwGroupCpy = copy.deepcopy(keyWordGroup)
            for pair in kwGroupCpy:
                word = pair[0]
                tag = "SYN" #pair[1] <<if we want to preseve tag, use this.
                #add finding synonyms for specific parts of speech
                synonyms = nhelp.getSynonyms(word)
                synonyms = map(lambda x: (x, tag), synonyms)
                keyWordGroup += synonyms
            keyWordGroup = self.removeDuplicate(keyWordGroup)
            
            keyWordList, posTag = zip(*keyWordGroup)
            keyWordList = list(keyWordList)
            posTag = list(posTag)

            
            # modify keyword List
            if DEBUG: 
                print keyWordList
                print posTag

            #E: if we care about capitalization, comment this line
            keyWordList = map(str.lower, keyWordList)

            #E: if we don't want to stem key words, comment this line.
            #Note: These are aliasing.
            self.keyWordList = keyWordList
            self.posTag = posTag

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
            elif "how" == questionList[0]:
                answer = self.answerMisc(keyWordList)
            elif ("is" in questionList
                or "was" in questionList
                or "did" in questionList):
                self.qType = "Yes/No"
                answer = self.answerYesNo(keyWordList)
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
        print "Demo: python %s DEMO" % (sys.argv[0])
        
    if len(sys.argv) == 1:
        printUsage()
        exit(0)
    
    if (sys.argv[1] == "DEMO"):
        print "Running Demo..."
        articlePath = ["../data/set2/a4.htm",
                   "../data/set2/a5.htm",
                   "../data/set1/a10.htm",
                   "../data/set3/a2.htm",
                   "../data/set3/a7.htm"]
        questionPath = ["../testQ/aries_easy.txt",
                    "../testQ/cancer_mixed.txt",
                    "../testQ/johnterry_easy.txt",
                    "../testQ/chinese_mixed.txt",
                    "../testQ/python_mixed.txt"]
        
        for i in xrange(len(articlePath)):
            articleFile = articlePath[i]
            questionFile = questionPath[i]
            print "Article path:", articleFile
            print "Question path:", questionFile
            articlefd = open(articleFile, "r")
            questionfd = open(questionFile, "r")
            a = Answer(articlefd, questionfd)
            a.driver()
            articlefd.close()
            questionfd.close()
            
        print "Done with Demo!"
        exit(0)
    
    if len(sys.argv) != 3:
        printUsage()
        exit(0)
        
    articlefd = open(sys.argv[1], "r")
    questionfd = open(sys.argv[2], "r")

    a = Answer(articlefd, questionfd)
    
    a.driver()
    
    articlefd.close()
    questionfd.close()
    
