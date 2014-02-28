OBJECT_ATTS = "../SCRDRlearner/ObjectAttributes.txt"

class Object:
    """
    Define Object class from a file containing list of attributes
    Object class represents a case which can be classified by SCRDR
    """

    attributes = [i.strip() for i in open(OBJECT_ATTS, "r").readlines()]
    code = "def __init__(self"
    for att in attributes:
        code = code + ", " + att + " = None"
    code = code + "):\n"
    for att in attributes:
        code = code + "    self." + att + "=" + att + "\n"
                
    exec (code)
    
    def toStr(self):
        res = "("
        for att in Object.attributes:
            boo = eval("isinstance(self. " + att + ", str)")
            if not boo:
                res = res + str(eval("self." + att))
            else:
                res = res + "\"" + str(eval("self." + att)) + "\""
                
            if att != Object.attributes[len(Object.attributes) - 1]:
                res = res + ","
        res += ")"
        return res

def getWordTag(wordTag):
    if wordTag == "///":
        return "/", "/"
    index = wordTag.rfind("/")
    word = wordTag[:index].strip()
    tag = wordTag[index +1:].strip()
    return word, tag


class FWObject:
    """
    RDRPOSTaggerv1.1: new implementation scheme
    Define five-word window Object class
    FWObject class represents a case which can be classified by SCRDR Tree
    """
    
    def __init__(self, check = False):
        self.context = [None, None, None, None, None, None, None, None, None, None]
        if(check == True):
            i = 0
            while (i < 10):
                self.context[i] = "<W>"
                self.context[i+1] = "<T>"
                i = i + 2
                
    def toStr(self):
        str = ""
        i = 0
        while (i < 10):
            word = self.context[i]
            tag = self.context[i + 1]
            if word == None:
                word = "None"
            if tag == None:
                tag = "None"
            str = str + word + "/" + tag + " "
            i = i + 2
        return str
    
    @staticmethod
    def getFWObject(startWordTags, index):
        object = FWObject(True)
        word, tag = getWordTag(startWordTags[index])
        object.context[4] = word
        object.context[5] = tag
        
        if index > 0:
            preWord1, preTag1 = getWordTag(startWordTags[index - 1])
            object.context[2] = preWord1
            object.context[3] = preTag1
            
        if index > 1:
            preWord2, preTag2 = getWordTag(startWordTags[index - 2])
            object.context[0] = preWord2
            object.context[1] = preTag2
        
        if index < len(startWordTags) - 1:
            nextWord1, nextTag1 = getWordTag(startWordTags[index + 1]) 
            object.context[6] = nextWord1
            object.context[7] = nextTag1
            
        if index < len(startWordTags) - 2:
            nextWord2, nextTag2 = getWordTag(startWordTags[index + 2])
            object.context[8] = nextWord2
            object.context[9] = nextTag2 
           
        return object
    
    def isSatisfied(self, fwObject):
        for i in xrange(10):
            key = self.context[i]
            if (key != None):
                if key != fwObject.context[i]:
                    return False
        return True