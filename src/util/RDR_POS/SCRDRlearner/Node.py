def tabStr(length):
    s = ""
    for i in xrange(length):
        s += "\t"
    return s

class Node:
    """
    Class representing a node of SCRDR tree
    """

    def __init__(self, condition, conclusion, father = None, exceptChild = None, elseChild = None, cornerstoneCases = [], depth = 0):
        """
        rule: python code - rule of the node
        conclusion: python code - conclusion of the node if the rule is satisfied
        father: Node - father of the node
        exceptChild, elseChild: Node - two children of the node
        cornerstoneCases: list of instances of Object class which are the cornerstone cases of the node
        depth: depth of node in tree
        """
        self.condition = condition
        self.conclusion = conclusion
        self.exceptChild = exceptChild
        self.elseChild = elseChild
        self.cornerstoneCases = cornerstoneCases
        self.father = father 
        self.depth = depth
        
    def satisfied(self, object):
        return eval(self.condition)
    
    def executeConclusion(self, object):
        exec(self.conclusion)        
        
    def appendCornerstoneCase(self, object):
        self.cornerstoneCases.append(object)
        
    def check(self, object):
        if self.satisfied(object):
            self.executeConclusion(object)
            if self.exceptChild != None:
                self.exceptChild.check(object)
        else:
            if self.elseChild != None:
                self.elseChild.check(object)
                
    def checkDepth(self, object, length):
        if self.depth <= length:
            if self.satisfied(object):
                self.executeConclusion(object)
                if self.exceptChild != None:
                    self.exceptChild.checkDepth(object, length)
            else:
                if self.elseChild != None:
                    self.elseChild.checkDepth(object, length)
                           
    """
    Find the node which the current node is exception of
    """
    def findRealFather(self):
        node = self
        fatherNode = node.father
        while True and fatherNode != None:
            if fatherNode.exceptChild == node:
                break
            node = fatherNode 
            fatherNode = node.father
        return fatherNode
    
    """
    Add a else-node to the current node
    Check if new rule fire the cornerstone cases of the real father node 
        - real father is the node which the current node is exception of
    """        
    def addElseChild(self, node):
        fatherNode = self.findRealFather()
        for object in fatherNode.cornerstoneCases:
            if node.satisfied(object):
                print "Error while adding new else node: the new rule fire the cornerstonecases of exception-father node"
                print "Condition: %s" % node.condition
                print "Object: %s" % object.toStr()
                self.findRealFather().cornerstoneCases.remove(object)
        self.elseChild = node
        return True
        
    """
    Add a exception-node to the current node
    Check if new rule fire the cornerstone cases of the father node 
    """        
    def addExceptChild(self, node):
        for object in self.cornerstoneCases:
            if node.satisfied(object):
                print "Error while adding new except node: the new rule fire the cornerstonecases of exception-father node"
                print "Condition: %s" % node.condition
                print "Object: %s" % object.toStr()
                self.cornerstoneCases.remove(object)
        self.exceptChild = node
        return True
    
    """
    Write to file
    """
    def writeToFile(self, out, depth):
        space = tabStr(depth)        
        out.write(space + self.condition + " : " + self.conclusion + "\n")
        for case in self.cornerstoneCases:
            out.write(" " + space + "cc: " + case.toStr() + "\n")
        if self.exceptChild != None:
            self.exceptChild.writeToFile(out, depth + 1)
        if self.elseChild != None:
            self.elseChild.writeToFile(out, depth)
    
    """
    Write to file without seen/cornerstone cases
    """
    def writeToFileWithoutSeenCases(self, out, depth):
        space = tabStr(depth)        
        out.write(space + self.condition + " : " + self.conclusion + "\n")
        if self.exceptChild != None:
            self.exceptChild.writeToFileWithoutSeenCases(out, depth + 1)
        if self.elseChild != None:
            self.elseChild.writeToFileWithoutSeenCases(out, depth)
            
    
    
