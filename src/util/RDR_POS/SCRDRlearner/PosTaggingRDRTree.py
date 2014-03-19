# -*- coding: utf-8 -*-
from Node import Node
from Object import FWObject
from RDRTree import RDRTree
from util.RDR_POS.Utility.Utils import getObjectDictionary, getObject, getWordTag

#"""
#Creating rules corresponding with each object of 7-word window
#"""
#def generateRules(object):
#    rules = []
#    
#    #1. Rule CURWD - current word
#    rule1 = "object.word == \"" + object.word + "\""
#        
#    #2. Rule WD1AFT - NEXT WORD
#    rule2 = "object.nextWord1 == \"" + object.nextWord1 + "\""
#    
#    #3. Rule WD2AFT - WORD 2 AFTER
#    rule3 = "object.nextWord2 == \"" + object.nextWord2 + "\""
#
#    #4. Rule WD3AFT - WORD 3 AFTER
#    #rule4 = "object.nextWord3 == \"" + object.nextWord3 + "\""
#    
#    #5. Rule WD1BEF - PREVIOUS WORD
#    rule5 = "object.prevWord1 == \"" + object.prevWord1 + "\""
#    
#    #6. Rule WD2BEF - WORD 2 BEFORE
#    rule6 = "object.prevWord2 == \"" + object.prevWord2 + "\""
#
#    #7. Rule WD3BEF - WORD 3 BEFORE
#    #rule7 = "object.prevWord3 == \"" + object.prevWord3 + "\""
#    
#    #8 Rule NEXT1OR2WD - ONE OF 2 NEXT WORDS
#    rule8_1 = rule2 + " or object.nextWord2 == \"" + object.nextWord1 + "\""
#    rule8_2 = "object.nextWord1 == \"" + object.nextWord2 + "\"" + " or " + rule3
#    
#    #9. Rule PREV1OR2WD - ONE OF 2 PREVIOUS WORDS
#    rule9_1 = rule5 + " or object.prevWord2 == \"" + object.prevWord1 + "\"" 
#    rule9_2 = "object.prevWord1 == \"" + object.prevWord2 + "\"" + " or " + rule6 
#    
#    #10. Rule RBIGRAM - CURRENT WORD AND NEXT WORD
#    rule10 = rule1 + " and " + rule2
#    
#    #11. Rule LBIGRAM - CURRENT WORD AND PREVIOUS WORD
#    rule11 = rule1 + " and " + rule5
#    
#    #12. Rule NEXTBIGRAM - 2 NEXT WORDS
#    rule12 = rule2 + " and " + rule3
#    
#    #13. Rule PREVBIGRAM - 2 PREVIOUS WORDS
#    rule13 = rule5 + " and " + rule6
#    
#    #14. Rule WDAND2AFT - CURRENT WORD AND WORD 2 AFTER
#    rule14 = rule1 + " and " + rule3
#    
#    #15. Rule WDAND2BEF - CURRENT WORD AND WORD 2 BEFORE
#    rule15 = rule1 + " and " + rule6
#    
#    #16. Rule TAG1AFT - NEXT TAG
#    rule16 = "object.nextTag1 == \"" + object.nextTag1 + "\""
#     
#    #17. Rule TAG2AFT - TAG 2 AFTER
#    rule17 = "object.nextTag2 == \"" + object.nextTag2 + "\""
#    
#    #18. Rule TAG3AFT - TAG 3 AFTER
#    #rule18 = "object.nextTag3 == \"" + object.nextTag3 + "\""
#    
#    #19. Rule TAG1BEF - PREVIOUS TAG
#    rule19 = "object.prevTag1 == \"" + object.prevTag1 + "\""
#     
#    #20. Rule TAG2BEF - TAG 2 BEFORE
#    rule20 = "object.prevTag2 == \"" + object.prevTag2 + "\""
#    
#    #21. Rule TAG3BEF - TAG 3 BEFORE
#    #rule21 = "object.prevTag3 == \"" + object.prevTag3 + "\""
#    
#    #22. Rule TAG1OR2AFT - ONE OF 2 NEXT TAGS
#    rule22_1 = rule16 + " or object.nextTag2 == \"" + object.nextTag1 + "\""
#    rule22_2 = "object.nextTag1 == \"" + object.nextTag2 + "\"" + " or " + rule17
#    rule22 = rule22_1 + " or " + rule22_2
#    
#    #23. Rule TAG1OR2OR3AFT - ONE OF 3 NEXT TAGS
#    #rule23_1 = rule22_1 + " or object.nextTag3 == \"" + object.nextTag1 + "\""
#    #rule23_2 = rule22_2 + " or object.nextTag3 == \"" + object.nextTag2 + "\""
#    #rule23_3 = "object.nextTag1 == \"" + object.nextTag3 +"\" or object.nextTag2 == \"" + object.nextTag3 + "\"" + " or " + rule18
#    #rule23 = rule23_1 + " or " + rule23_2 + " or " + rule23_3
#    
#    #24. Rule TAG1OR2BEF - ONE OF 2 PREVIOUS TAGS
#    rule24_1 = rule19 + " or object.prevTag2 == \"" + object.prevTag1 + "\""
#    rule24_2 = "object.prevTag1 == \"" + object.prevTag2 + "\"" + " or " + rule20
#    rule24 = rule24_1 + " or " + rule24_2
#    
#    #25. Rule TAG1OR2OR3BEF - ONE OF 3 PREVIOUS TAGS
#    #rule25_1 = rule24_1 + " or object.prevTag3 == \"" + object.prevTag1 + "\""
#    #rule25_2 = rule24_2 + " or object.prevTag3 == \"" + object.prevTag2 + "\""
#    #rule25_3 = "object.prevTag1 == \"" + object.prevTag3 +"\" or object.prevTag2 == \"" + object.prevTag3 + "\"" + " or " + rule21
#    
#    #26. Rule TAG1AND2AFT - NEXT TAG AND TAG 2 NEXT
#    rule26 = rule16 + " and " + rule17
#    
#    #27. Rule TAG1AND2BEF - PREVIOUS TAG AND TAG 2 AFTER
#    rule27 = rule19 + " and " + rule20
#    
#    #28. Rule SURROUNDTAG
#    rule28 = rule16 + " and " + rule19
#    
#    #29. Rule WDANDNEXTTAG - CURRENT WORD AND NEXT TAG
#    rule29 = rule1 + " and " + rule16
#    
#    #30. Rule WDANDTAG2AFT - CURRENT WORD AND TAG 2 AFTER
#    rule30 = rule1 + " and " + rule17
#    
#    #31. Rule WDANDTAG3AFTER - CURRENT WORD AND TAG 3 AFTER
#    #rule31 = rule1 + " and " + rule18
#    
#    #32. Rule WDANDPREVTAG - CURRENT WORD AND PREVIOUS TAG
#    rule32 = rule1 + " and " + rule19
#    
#    #33. Rule WDANDTAG2BEF - CURRENT WORD AND TAG 2 BEFORE
#    rule33 = rule1 + " and " + rule20
#    
#    #34. Rule WDANDTAG3BEF - CURRENT WORD AND TAG 3 BEFORE
#    #rule34 = rule1 + " and " + rule21
#    
#    #35. Rule WDAND2TAGAFT - CURRENT WORD AND 2 TAGS AFTER
#    rule35 = rule1 + " and " + rule26
#    
#    #36. Rule WDAND2TAGBEF - CURRENT WORD AND 2 TAGS BEFORE
#    rule36 = rule1 + " and " + rule27
#    
##    rule37 = "(" + rule5 + ")" + " or " + "(" +  rule30 + ")"
##    rule38 = "(" + rule3 + ")" + " or " + "(" +  rule5 + ")" + " or " + "(" +  rule9 + ")" + " or " + "(" +  rule13 + ")" + " or " + "(" +  rule24 + ")" + " or " + "(" +  rule27 + ")" + " or " + "(" +  rule28 + ")"
##    rule39 = "(" + rule5 + ")" + " or " + "(" +  rule19 + ")" + " or " + "(" +  rule24 + ")"
##    rule40 = "(" + rule5 + ")" + " or " + "(" +   rule9 + ")" + " or " + "(" +  rule10 + ")" + " or " + "(" +  rule36 + ")"
##    rule41 = "(" + rule10 + ")" + " or " + "(" +  rule14 + ")"
##    rule42 = "(" + rule6 + ")" + " or " + "(" +  rule7 + ")" + " or " + "(" +  rule9 + ")" + " or " + "(" +  rule25 + ")" + " or " + "(" +  rule32 + ")"
##    rule43 = "(" + rule32 + ")" + " or " + "(" +  rule33 + ")"
##    rule44 = "(" + rule5 + ")" + " or " + "(" +  rule7 + ")" + " or " + "(" +  rule11 + ")" + " or " + "(" +  rule24  + ")" + " or " + "(" +  rule28 + ")" + " or " + "(" +  rule33 + ")"
##    rule45 =  "(" + rule4 + ")" + " or " + "(" +  rule5 + ")" + " or " + "(" +  rule6 + ")" + " or " + "(" +  rule7 + ")"
##    rule46 = "(" + rule5 + ")" + " or " + "(" +  rule11 + ")"
##    rule47 = "(" + rule1 + ")" + " or " + "(" +  rule4 + ")" + " or " + "(" +  rule11 + ")"
##    rule48 = "(" + rule1 + ")" + " or " + "(" +  rule5 + ")" + " or " + "(" +  rule9 + ")" + " or " + "(" +  rule26 + ")" + " or " + "(" +  rule33 + ")"
##    rule49 = "(" + rule1 + ")" + " or " + "(" +  rule3 + ")" + " or " + "(" +  rule34 + ")"
##    rule50 = "(" + rule1 + ")" + " or " + "(" +  rule2 + ")" + " or " + "(" +  rule5 + ")" + " or " + "(" +  rule6 + ")" + " or " + "(" +  rule9 + ")" + " or " + "(" +  rule26 + ")" + " or " + "(" +  rule28 + ")"
##    rule51 = "(" + rule5 + ")" + " or " + "(" +  rule19 + ")"
##    rule52 = "(" + rule5 + ")" + " or " + "(" +  rule9 + ")" + " or " + "(" +  rule10 + ")" + " or " + "(" +  rule32 + ")"
##    rule53 = "(" + rule11 + ")" + " or " + "(" +  rule24 + ")" + " or " + "(" +  rule32 + ")"
##    rule54 = "(" + rule5 + ")" + " or " + "(" +  rule19 + ")" + " or " + "(" +  rule28  + ")"
##    rule55 = "(" + rule3 + ")" + " or " + "(" +  rule5 + ")" + " or " + "(" +  rule13 + ")" + " or " + "(" +  rule19 + ")" + " or " + "(" +  rule27 + ")" + " or " + "(" +  rule28 + ")"
##    
#    
#    rules.append(rule1)
#    rules.append(rule2)
#    rules.append(rule3)
#    #rules.append(rule4)
#    rules.append(rule5)
#    rules.append(rule6)
#    #rules.append(rule7)
#    rules.append(rule8_1)
#    rules.append(rule8_2)
#    rules.append(rule9_1)
#    rules.append(rule9_2)
#    rules.append(rule10)
#    rules.append(rule11)
#    rules.append(rule12)
#    rules.append(rule13)
#    rules.append(rule14)
#    rules.append(rule15)
#    rules.append(rule16)
#    rules.append(rule17)
#   # rules.append(rule18)
#    rules.append(rule19)
#    rules.append(rule20)
#    #rules.append(rule21)
#    rules.append(rule22_1)
#    rules.append(rule22_2)
#    #rules.append(rule23_1)
#    #rules.append(rule23_2)
#    #rules.append(rule23_3)
#    rules.append(rule24_1)
#    rules.append(rule24_2)
#    #rules.append(rule25_1)
#    #rules.append(rule25_2)
#    #rules.append(rule25_3)
#    rules.append(rule26)
#    rules.append(rule27)
#    rules.append(rule28)
#    rules.append(rule29)
#    rules.append(rule30)
#    #rules.append(rule31)
#    rules.append(rule32)
#    rules.append(rule33)
#    #rules.append(rule34)
#    rules.append(rule35)
#    rules.append(rule36)
##    rules.append(rule37)
##    rules.append(rule38)
##    rules.append(rule39)
##    rules.append(rule40)
##    rules.append(rule41)
##    rules.append(rule42)
##    rules.append(rule43)
##    rules.append(rule44)
##    rules.append(rule45)
##    rules.append(rule46)
##    rules.append(rule47)
##    rules.append(rule48)
##    rules.append(rule49)
##    rules.append(rule50)
##    rules.append(rule51)
##    rules.append(rule52)
##    rules.append(rule53)
##    rules.append(rule54)
##    rules.append(rule55)
##    
#    rules = set(rules)
#    return rules

"""
Creating rules corresponding with each object of 5-word window
"""
def generateRules(object):
    
    rules = []
    
    #1. Rule CURWD - current word
    rule1 = "object.word == \"" + object.word + "\""
            
    #2. Rule WD1AFT - NEXT WORD
    rule2 = "object.nextWord1 == \"" + object.nextWord1 + "\""
        
    #3. Rule WD2AFT - WORD 2 AFTER
    rule3 = "object.nextWord2 == \"" + object.nextWord2 + "\""
    
    #4. Rule WD1BEF - PREVIOUS WORD
    rule4 = "object.prevWord1 == \"" + object.prevWord1 + "\""
        
    #5. Rule WD2BEF - WORD 2 BEFORE
    rule5 = "object.prevWord2 == \"" + object.prevWord2 + "\""
        
    #6. Rule RBIGRAM - CURRENT WORD AND NEXT WORD
    rule6 = rule1 + " and " + rule2
    
    #7. Rule LBIGRAM - CURRENT WORD AND PREVIOUS WORD
    rule7 = rule4 + " and " + rule1
    
    #8. CURRENT WORD AND NEXT WORD AND NEXT 2 WORD
    rule8 = rule6 + " and " + rule3
    
    #9. CURRENT WORD AND PREVIOUS WORD AND PREVIOUS 2 WORD
    rule9 = rule5 + " and " + rule7 
    
    #10. previous word & current word & next word
    rule10 = rule4 + " and " + rule6
    
    #11. previous word & next word
    rule11 = rule4 + " and " + rule2
    
    
    #12. Rule TAG1AFT - NEXT TAG
    rule12 = "object.nextTag1 == \"" + object.nextTag1 + "\""
     
    #13. Rule TAG2AFT - TAG 2 AFTER
    rule13 = "object.nextTag2 == \"" + object.nextTag2 + "\""
    
    #19. Rule TAG1BEF - PREVIOUS TAG
    rule14 = "object.prevTag1 == \"" + object.prevTag1 + "\""
     
    #15. Rule TAG2BEF - TAG 2 BEFORE
    rule15 = "object.prevTag2 == \"" + object.prevTag2 + "\""
    
    #16. next tag and next 2 tag
    rule16 = rule12 + " and " + rule13
    
    #17. previous 2 tag and previous tag
    rule17 = rule15 + " and " + rule14
    
    #18. Surrounding tag
    rule18 = rule14 + " and " + rule12
    
    #19. current word and next 2 word.
    rule19 = rule1 + " and " + rule3
    
    #20. previous 2 word and current word
    rule20 = rule5 + " and " + rule1
    
    
    #21. CURRENT WORD AND NEXT TAG
    rule21 = rule1 + " and " + rule12
    
    #22. CURRENT WORD AND PREVIOUS tag
    rule22 = rule14 + " and " + rule1
    
    #23. CURRENT WORD AND NEXT WORD tag and NEXT 2 tag
    rule23 = rule21 + " and " + rule13
    
    #24. CURRENT WORD AND PREVIOUS WORD AND PREVIOUS 2 tag
    rule24 = rule15 + " and " + rule22 
    
    #25. previous tag & current word & next tag
    rule25 = rule14 + " and " + rule21
    
    #26. current word and 2 next tags.
    rule26 = rule1 + " and " + rule16
    
    #27. 2 previous tags and current word
    rule27 = rule17 + " and " + rule1
    
    rules.append(rule1)
    rules.append(rule2)
    rules.append(rule3)
    rules.append(rule4)
    rules.append(rule5)
    rules.append(rule6)
    rules.append(rule7)
    rules.append(rule8)
    rules.append(rule9)
    rules.append(rule10)
    rules.append(rule11)
    rules.append(rule12)
    rules.append(rule13)
    rules.append(rule14)
    rules.append(rule15)
    rules.append(rule16)
    rules.append(rule17)
    rules.append(rule18)
    rules.append(rule19)
    rules.append(rule20)
    rules.append(rule21)
    rules.append(rule22)
    rules.append(rule23)
    rules.append(rule24)
    rules.append(rule25)
    rules.append(rule26)
    rules.append(rule27)
   
    rules = set(rules)
    return rules


"""
Generate all rules not in ruleNotIn rules set from an objects set, and count number of matching objects for each rule
"""
def countMatching(objects, ruleNotIn):
    counts = {}
    matchedObjects = {}
    for object in objects:
        rules = generateRules(object)
        for rule in rules:
            if rule in ruleNotIn:
                continue
            
            counts[rule] = counts.setdefault(rule, 0) + 1
            matchedObjects.setdefault(rule, []).append(object)
    return counts, matchedObjects

"""
Check whether an object satisfy a rule or not
"""
def satisfy(object, rule):
    return eval(rule)

"""
Check if a rule fire cornerstone-cases/seen-cases or not
"""
def fire(rule, cornerstoneCases):
    for object in cornerstoneCases:
        if satisfy(object, rule):
            return True
        
    return False


"""
Generate all rules from an object set
"""
def generateRulesFromObjectsSet(objects):
    res = []
    for object in objects:
        rules = generateRules(object)
        res += rules
    return res

class PosTaggingRDRTree(RDRTree):
    def __init__(self, improveThreshold = 1, matchThreshold = 1):
        self.improveThreshold = improveThreshold
        self.matchThreshold = matchThreshold
        
    
    def findMostImproveRuleForTag(self, startTag, correctTag, correctCounts, wrongObjects):
        """
        Find the best rule changing tag of object from initializedTag to correctTag
        The rule is found based on list of correct objects which have correct tag is the initialzied tag
            and list of wrong objects which need to be changed its tags to correctTag
        """
        
        impCounts, affectedObjects = countMatching(wrongObjects, [])
        
        maxImp = -1000000
        bestRule = ""
        for rule in impCounts:
            temp = impCounts[rule]
            if rule in correctCounts:
                temp -= correctCounts[rule]
                
            if temp > maxImp:
                maxImp = temp
                bestRule = rule
                
        if maxImp == -1000000:
            affectedObjects[bestRule] = []
                
        return bestRule, maxImp, affectedObjects[bestRule]
    
    def findMostEfficientRule(self, startTag, objects, correctCounts):
        """
        Find the rule having best improvement
        improvement = A - B 
        A is the number of objects which satisfy the rule and its tag is changed correctly by the rule 
        B is number of objects which satisfy the rule but obtaining the wrong tag by the rule
        """
    
        maxImp = -1000000
        rule = ""
        correctTag = ""
        cornerstoneCases = []
        
        """
        print "Generating rules of correct objects"
        correctCounts = {}
        for object in objects[startTag]:
            rules = generateRules(object)
            for rule in rules:
                correctCounts[rule] = correctCounts.setdefault(rule, 0) + 1
        print "Total rules: %d" % len(correctCounts)
        """
        for tag in objects:
            if tag == startTag:
                continue
            if len(objects[tag]) <= maxImp or len(objects[tag]) < self.improveThreshold:
                continue
            
            ruleTemp, imp, affectedObjects = self.findMostImproveRuleForTag(startTag, correctTag, correctCounts, objects[tag])
            if imp >= self.improveThreshold and imp > maxImp:
                maxImp = imp
                rule = ruleTemp
                correctTag = tag
                cornerstoneCases = affectedObjects
            
        needToCorrectObjects = {}
        errorRaisingObjects = []
        if maxImp > -1000000:    
            for tag in objects:
                if tag != correctTag:
                    for object in objects[tag]:
                        if satisfy(object, rule):
                            needToCorrectObjects.setdefault(tag, []).append(object)
                            if tag == startTag:
                                errorRaisingObjects.append(object)
                
        return rule, correctTag, maxImp, cornerstoneCases, needToCorrectObjects, errorRaisingObjects

    
    def findMostMatchingRule(self, matchingCounts):
        """
        Find the rule most matching the given objects set.
        This rule must not fire the given cornerstone-Cases/seen-cases. 
        """
    
        correctTag = ""
        bestRule = ""
        maxCount = -1000000
        
        for tag in matchingCounts:
            for rule in matchingCounts[tag]:
                if matchingCounts[tag][rule] >= self.matchThreshold and matchingCounts[tag][rule] > maxCount:
                    maxCount = matchingCounts[tag][rule]
                    bestRule = rule
                    correctTag = tag
                
        return bestRule, correctTag 
    
    def buildRDRTreeForObjectsSet(self, objects, root):
        cornerstoneCaseRules = generateRulesFromObjectsSet(root.cornerstoneCases)
        
        matchingCounts = {}
        matchingObjects = {}
        for tag in objects:
            matchingCounts[tag], matchingObjects[tag] = countMatching(objects[tag], cornerstoneCaseRules)
        
        total = 0
        for tag in objects:
            total += len(objects[tag])
                        
        currentNode = root
        elseChild = False
        while True:       
            rule, correctTag = self.findMostMatchingRule(matchingCounts)
                            
            if rule == "":
                break
            
            cornerstoneCases = matchingObjects[correctTag][rule]
            
            needToCorrectObjects = {}        
            for tag in objects:
                if rule in matchingObjects[tag]:
                    if tag != correctTag:
                        needToCorrectObjects[tag] = matchingObjects[tag][rule]
                    for object in matchingObjects[tag][rule]:
                        rules = generateRules(object)
                        for rule1 in rules:
                            if rule1 not in matchingCounts[tag]:
                                continue
                            matchingCounts[tag][rule1] -= 1
                    
            node = Node(rule, "object.conclusion = \"" + correctTag + "\"", currentNode, None, None, cornerstoneCases)
            
            if not elseChild:
                currentNode.exceptChild = node
                elseChild = True
            else:
                currentNode.elseChild = node
            
            currentNode = node
            self.buildRDRTreeForObjectsSet(needToCorrectObjects, currentNode)
        
    def buildTreeFromCorpus(self, startStateFile, correctFile):
        """
        Build RDR Tree to classify tags of each word by comparing initialized corpus and golden corpus.
        """
            
        self.root = Node("True", "object.conclusion = \"NN\"", None, None, None, [], 0)
        print "Reading corpus..."
        print 'Threshold: ', self.improveThreshold, '-', self.matchThreshold
        objects = getObjectDictionary(startStateFile, correctFile)
                        
        currentNode = self.root
        for startTag in objects:
            print "\n*******\nBuilding rules for start tag: %s" % startTag
            print "Number of correct tag : %d" % len(objects[startTag])
            print "Correct tag for start tag:", objects[startTag].keys()

            total = 0
            for correctTag in objects[startTag]:
                total += len(objects[startTag][correctTag])
                s = correctTag
                for i in xrange (10 - len(correctTag)):
                    s += " "
                #print "%s: %d" % (s, len(objects[startTag][correctTag]))
            print "Total objects with start Tag: %d" % total
            
            correctCounts = {}
            for object in objects[startTag][startTag]:
                rules = generateRules(object)
                for rule in rules:
                    correctCounts[rule] = correctCounts.setdefault(rule, 0) + 1
            
            node = Node("object.tag == \"" + startTag + "\"", "object.conclusion = \"" + startTag + "\"", self.root, None, None, [], 1)
            
            if self.root.exceptChild == None:
                self.root.exceptChild = node
            else:
                currentNode.elseChild = node

            currentNode = node
            objectSet = objects[startTag]
            
            elseChild = False            
            currentNode1 = currentNode
            while True:
                rule, correctTag, imp, cornerstoneCases, needToCorrectObjects, errorRaisingObjects = self.findMostEfficientRule(startTag, objectSet, correctCounts)
                if imp < self.improveThreshold:
                    break
            
                node = Node(rule, "object.conclusion = \"" + correctTag + "\"", currentNode, None, None, cornerstoneCases, 2)
                    
                if not elseChild:
                    currentNode1.exceptChild = node
                    elseChild = True
                else:
                    currentNode1.elseChild = node
                    
                currentNode1 = node
                
                for object in cornerstoneCases:
                    objectSet[correctTag].remove(object)
                    
                for tag in needToCorrectObjects:
                    for object in needToCorrectObjects[tag]:
                        objectSet[tag].remove(object)
                        
                for object in errorRaisingObjects:
                    rules = generateRules(object)
                    for rule in rules:
                        correctCounts[rule] -= 1
                        
                self.buildRDRTreeForObjectsSet(needToCorrectObjects, currentNode1)
    
    def classifyInDepth(self, object, depth):
        """
        Classify an object due to the exception-level depth 
        """
        self.root.checkDepth(object, depth)
        
    def countNodes(self, node, depth):
        """
        Calculate the number of nodes/rules in the tree.
        """
        
        count = 1
        if node == None:
            return 0
        else:
            if self.findDepth(node) > depth:
                return 0
        if node.exceptChild != None:
            count += self.countNodes(node.exceptChild, depth)
        if node.elseChild != None:
            count += self.countNodes(node.elseChild, depth)
        return count
    
    def findDepth(self, node):
        """
        Find the depth of a node in tree
        """
        count = 1
        while(True and node != None):
            node = node.findRealFather()
            if (node == self.root):
                break
            else:
                count = count + 1
        return count
    
    def tagCorpus_old(self, inputFile, outFile):
        '''
        Tag  initialized corpus...
        '''
        
        lines = open(inputFile, "r").readlines()
        out = open(outFile, "w")
        for line in lines:
            wordTags = line.split()
            startWordTags = line.replace("“", "''").replace("”", "''").replace("\"", "''").split()
            for i in xrange(len(startWordTags)):
                object = getObject(startWordTags, i)
                word, tag = getWordTag(wordTags[i])
                self.classify(object)
                out.write(word + "/" + object.conclusion + " ")
            out.write("\n")
        out.close()

                  
    def tagCorpusInDepth_old(self, inputFile, outFile, depth):
        '''
        Tag initialized corpus due to the depth of exception level...
        ''' 
        
        lines = open(inputFile, "r").readlines()
        out = open(outFile, "w")        
        for line in lines:
            wordTags = line.split()
            startWordTags = line.replace("“", "''").replace("”", "''").replace("\"", "''").split()
            for i in xrange(len(startWordTags)):
                object = getObject(startWordTags, i)
                word, tag = getWordTag(wordTags[i])
                self.classifyInDepth(object, depth)
                out.write(word + "/" + object.conclusion + " ")
            out.write("\n")
        out.close()

    
    def tagInitializedCorpus_new(self, inputFile, outFile):
        '''
        Tag  initialized corpus according to new implementation scheme
        '''
        
        lines = open(inputFile, "r").readlines()
        out = open(outFile, "w")
        for line in lines:
            wordTags = line.split()
            startWordTags = line.replace("“", "''").replace("”", "''").replace("\"", "''").split()
            for i in xrange(len(startWordTags)):
                fwObject = FWObject.getFWObject(startWordTags, i)
                word, tag = getWordTag(wordTags[i])
                node = self.findFiredNode(fwObject)
                out.write(word + "/" + node.conclusion + " ")
            out.write("\n")
        out.close()
