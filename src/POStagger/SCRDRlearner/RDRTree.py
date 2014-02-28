# -*- coding: utf-8 -*-
from Node import Node
from Object import FWObject

class RDRTree:
    """
    Single Classification Ripple Down Rules tree for POS Tagging
    """
    
    def __init__(self, root = None):
        self.root = root
        
    def buildTreeFromRulesFile (self, rulesFileName):
        """
        rdrpostaggerv1: Build tree from file containing rules
        """
 
        print "Build tree from rule-file..."
        rulesFile = open(rulesFileName, "r")
        lines = rulesFile.readlines()
        rootCondition = lines[0].split(":", 1)[0].strip()
        rootConclusion = lines[0].split(":", 1)[1].strip()
        self.root = Node (rootCondition, rootConclusion, None, None, None, [], 0)
        
        currentNode = self.root
        currentDepth = 0
        
        i = 0
        for i in xrange(1, len(lines)):
            line = lines[i]
            #count depth of node
            depth = 0           
            for c in line:
                if c == '\t':
                    depth = depth + 1
                else:
                    break

            line = line.strip()
            if len(line) == 0:
                continue
                
            temp = line.find("cc")
            if temp == 0:   
                #cornerstoneCase = None
                #exec ("cornerstoneCase = Object" + line.split(":", 1)[1].strip())
                #currentNode.appendCornerstoneCase(cornerstoneCase)
                continue
                
            conditionConclusion = line.split(" : ", 1)
            condition = conditionConclusion[0].strip()
            conclusion = conditionConclusion[1].strip()
            
            if depth == currentDepth:
                node = Node(condition, conclusion, currentNode, None, None, [], depth)
                if not currentNode.addElseChild(node):
                    print "Error rules file in line: %d!" % i
                else:
                    currentNode = node
                
            elif depth > currentDepth:
                node = Node(condition, conclusion, currentNode, None, None, [], depth)
                if not currentNode.addExceptChild(node):
                    print "Error rules file in line: %d!" % (i + 1)
                else:               
                    currentNode = node
                    currentDepth = depth
            else:
                #Find the node of which the new node is else-child
                fatherNode = self.findDepthNode(currentNode, depth)
                node = Node(condition, conclusion, fatherNode, None, None, [], depth)
                if not fatherNode.addElseChild(node):
                    print "Error rules file in line: %d!" % (i + 1)
                else:
                    currentNode = node
                    currentDepth = depth
                    
    def findDepthNode(self, node, depth):
        while node.depth != depth:
            node = node.father
        return node                
                
    def classify(self, object):
        self.root.check(object)
        
    def writeToFile(self, outFile):
        out = open(outFile, "w")
        self.root.writeToFile(out, 0)
        out.close()
    
    def writeToFileWithoutSeenCases(self, outFile):
        out = open(outFile, "w")
        self.root.writeToFileWithoutSeenCases(out, 0)
        out.close()
        
    
    def constructTreeFromRulesFile(self, rulesFileP):
        '''
        #-----------------------------------------------------------
        # rdrpostaggerv1.1: New implementation scheme: using FWObject
        # Build tree from file containing rules
        #-----------------------------------------------------------
        '''
        
        self.root = Node(FWObject(False), "NN", None, None, None, [], 0)
        
        currentNode = self.root
        currentDepth = 0
        
        rulesFile = open(rulesFileP, "r")
        lines = rulesFile.readlines()
        
        for i in xrange(1, len(lines)):
            line = lines[i]
            depth = 0           
            for c in line:
                if c == '\t':
                    depth = depth + 1
                else:
                    break

            line = line.strip()
            if len(line) == 0:
                continue
                
            temp = line.find("cc")
            if temp == 0:   
                continue
            
            condition = getCondition(line.split(" : ", 1)[0].strip())
            conclusion = getConclusion(line.split(" : ", 1)[1].strip())
            node = Node(condition, conclusion, None, None, None, [], depth)
            #print line
            #print condition.toStr(), conclusion
            if depth > currentDepth:
                currentNode.exceptChild = node
            elif depth == currentDepth:
                currentNode.elseChild = node
            else:
                while currentNode.depth != depth:
                    currentNode = currentNode.father;
                currentNode.elseChild = node
            
            node.father = currentNode;
            
            currentNode = node;
            currentDepth = depth;
    
    def findFiredNode(self, fwObject):
        currentNode = self.root
        firedNode = None
        while True:
            if(currentNode.condition.isSatisfied(fwObject)):
                firedNode = currentNode
                if currentNode.exceptChild == None:
                    break
                else:
                    currentNode = currentNode.exceptChild
            else:
                if currentNode.elseChild == None:
                    break
                else:
                    currentNode = currentNode.elseChild
        return firedNode

def getConclusion(strConclusion):
    if strConclusion.find('""') > 0:
        if strConclusion.find("Word") > 0:
            return "<W>"
        else:
            return "<T>"
    return strConclusion[strConclusion.find("\"") + 1 : len(strConclusion) - 1]
       
def getCondition(strCondition):
    condition = FWObject(False)
    for rule in strCondition.split(" and "):
        rule = rule.strip()
        key = rule[rule.find(".") + 1 : rule.find(" ")]
        value = getConclusion(rule)
        #print rule, key, value     
        if key == "prevWord2": 
            condition.context[0] = value
        elif key == "prevTag2":
            condition.context[1] = value
        elif key == "prevWord1":
            condition.context[2] = value
        elif key == "prevTag1":
            condition.context[3] = value
        elif key == "word":
            condition.context[4] = value
        elif key == "tag":
            condition.context[5] = value
        elif key == "nextWord1":
            condition.context[6] = value
        elif key == "nextTag1":
            condition.context[7] = value
        elif key == "nextWord2":
            condition.context[8] = value
        else:
            condition.context[9] = value
    #print condition.toStr()
    return condition
    
if __name__ == "__main__":
    pass
