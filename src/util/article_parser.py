#!/usr/bin/python
#
# article_parser.py
#
# Class with relevant functions to parse HTML article files
# Extracts data based on the header tags
# Places setnences into a list
# Creates a dictionary with subjects (based on header info)
#
# Eric Gan
#   with 
# Aaron Anderson
# Rachel Kobayashi
#
#

#TODO:
#-Handle h3 tags (subtopics of topics)
#-Remodel this parser to handle UNICODE instead of STRINGS (BIG BIG Difference)
#-Replace double-quotations with double-single quotations
#-Replace all whitespace characters (\n, \t etc) with spaces.
#-Find a way to strip a word to its morphological roots.

from HTMLParser import HTMLParser
import nltk_helper
import nltk
import nltk.data

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        
        #This is to be modified depending on the type of data we want to fetch
        self.tagsToRead = ['p', 'ul', 'blockquote', 'dl', 'ol']
        
        #Other initialized variables
        self.tagList = []
        
        self.articleName = ""
        self.articleText = ""
        self.curTopic = None
        self.curTopicBuf = ""
        self.topicDict = dict()

    def handle_starttag(self, tag, attrs):
        if tag == "br": return #skip br tags
        self.tagList.append(tag)
        
        # Add the data to the topic dictionary before fetching new category
        # Then reset the buffer.
        if tag == "h2":
            if self.curTopic == None:
                self.topicDict[self.articleName.strip()] = self.curTopicBuf
            elif self.curTopicBuf != "":
                self.topicDict[self.curTopic.strip()] = self.curTopicBuf
            self.curTopicBuf = ""
        
    def handle_endtag(self, tag):
        if tag in self.tagsToRead:
            self.articleText += " "
            self.curTopicBuf += " "
        popTag = self.tagList.pop()
        if popTag != tag:
            raise Exception("Error! Tag mismatch '%s' and '%s'! Aborting..." % (tag, popTag))
    
    def handle_data(self, data):
        if "title" in self.tagList:
            self.articleName += data
        if "h2" in self.tagList:
            self.curTopic = data
        
        for tag in self.tagsToRead:
            if tag in self.tagList:
                self.articleText += data
                self.curTopicBuf += data
    
    #Call this function to grab the article text.
    def grabText(self):
        return self.articleText.decode("utf-8")

    def grabTextSentenceList(self):
        sentList = nltk_helper.parseTextToSentences(self.articleText)
        toRemove = []
        for i in xrange(len(sentList)):
            if "(disambiguation)" in sentList[i]:
                toRemove.append(sentList[i])
            sentList[i] = sentList[i].replace("[citation\xc2\xa0needed] ", "")
            sentList[i] = sentList[i].replace("[page\xc2\xa0needed] ", "")
        for sent in toRemove:
            sentList.remove(sent)
        return sentList

    def grabTokList(self):
        return nltk.word_tokenize(self.grabText())
    
    #Returns the dictionary mapping of topics to texts
    def grabTopicDict(self):
        return self.topicDict

    def grabTopicSentenceDict(self):
        sentDict = dict()
        for key in self.topicDict:
            sentDict[key] = nltk_helper.parseTextToSentences(self.topicDict[key])
            toRemove = []
            for i in xrange(len(sentDict[key])):
                if "(disambiguation)" in sentDict[key][i]:
                    toRemove.append(sentDict[key][i])
                sentDict[key][i] = sentDict[key][i].replace("[citation\xc2\xa0needed] ", "")
                sentDict[key][i] = sentDict[key][i].replace("[page\xc2\xa0needed] ", "")
            for sent in toRemove:
                sentDict[key].remove(sent)
        return sentDict
    
    #Returns a list of topics (assumed to be h2-tagged) for the article
    def grabTopicList(self):
        topicList = []
        for key in self.topicDict:
            topicList.append(key)
        return topicList
    
    def grabTitle(self):
        return self.articleName
    
    
    
    
    
