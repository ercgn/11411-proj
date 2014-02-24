#TODO:
#-Handle h3 tags (subtopics of topics)
#-Remodel this parser to handle UNICODE instead of STRINGS (BIG BIG Difference)

from HTMLParser import HTMLParser

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
        self.tagList.append(tag)
        
        # Add the data to the topic dictionary before fetching new category
        # Then reset the buffer.
        if tag == "h2":
            if self.curTopic == None:
                self.topicDict[self.articleName] = self.curTopicBuf
            elif self.curTopicBuf != "":
                self.topicDict[self.curTopic] = self.curTopicBuf
            self.curTopicBuf = ""
        
    def handle_endtag(self, tag):
        if self.tagList.pop() != tag:
            raise "Error! Tag mismatch! Aborting..."
    
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
        return self.articleText
    
    #Returns the dictionary mapping of topics to texts
    def grabTopicDict(self):
        return self.topicDict
    
    #Returns a list of topics (assumed to be h2-tagged) for the article
    def grabTopicList(self):
        topicList = []
        for key in self.topicDict:
            topicList.append(key)
        return topicList
    
    def grabTitle(self):
        return self.articleName
    
    
    
    
    