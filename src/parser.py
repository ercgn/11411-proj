from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        
        #This is to be modified depending on the type of data we want to fetch
        self.tagsToRead = ['p', 'ul', 'blockquote', 'dl', 'ol']
        
        #Other initialized variables
        self.tagList = []
        self.articleText = ""

    def handle_starttag(self, tag, attrs):
        self.tagList.append(tag)
        
    def handle_endtag(self, tag):
        if self.tagList.pop() != tag:
            raise "Error! Tag mismatch! Aborting..."
    
    def handle_data(self, data):
        for tag in self.tagsToRead:
            if tag in self.tagList:
                self.articleText += data
    
    #Call this function to grab the article text.
    def grabText(self):
        return self.articleText
    
    