#
# sent_2_q.py
#
# Given a sentence, this class can be used to turn the sentence into a question
#   tries a variety of methods and returns after one has been successful
#
# Rachel Kobayashi
#   with
# Aaron Anderson
# Eric Gan
#
#

import util.rdrpos as rdrpos
import nltk, string
from util.combinations import Combine
from util.qutil import *

# cases to replace:
#   dates -> when
#   if -> why question with the if section as the clause
#   noun / proper noun / pronoun replacement
#   names / proper nouns

class ConstructQuestion(object):
    def __init__(self, sentence):
        self.c = Combine();
        self.tokens = nltk.word_tokenize(sentence.strip());
        self.tags = rdrpos.pos_tag(sentence.strip());
         # check if capitaliaztion is necessary and otherwise remove.
        self.nltkTags = nltk.pos_tag(self.tokens);
        if (self.nltkTags[0] != self.tags[0]) and \
           self.c.ID.isReplacablePronoun(self.tokens[0]):
            self.tokens[0] = self.tokens[0].lower();
        # returned question / question word
        self.out = "";
        self.qWord = None;
        self.N = len(self.tokens);
        self.make(sentence);

    # Split the tokens and tags into phrases based on commas
    # or other ending punc such as ;.?
    # cannot just join and use split because the question word that has
    # been replaced might be more than one word
    # might be irrelevant depending on the sentence handed in
    # hence the early check for , 
    def splitComma(self):
        tok = self.tokens;
        pos = self.tags;
        # not necessary to split indicated by -1 ouput
        if ',' not in set(tok):
            return tok,pos, (-1,0);
        tokCommaList, tagCommaList, idxs = self.splitCommaBare(tok, pos, True);
        # list of indicdes that indicate splitted phrase in the original
        idxs.append(len(tok)); 
        (qIdx, qWord) = self.qWord;
        # find the index of the comma phrase that contains the question word
        for idx in range(len(idxs)-1):
            if idxs[idx] <= qIdx and qIdx < idxs[idx+1]: 
                return (tokCommaList, tagCommaList, (idx, idxs[idx]));
        return tokCommaList, tagCommaList, (0,0);

    # splitCommaBare - split the input into list of components 
    # based on comma / end punctuation placement
    # takes in the tok, associated pos tags, and
    # idxFlag which indicates whether or not the output should include
    # a list of where the original lists were split
    def splitCommaBare(self, tok, pos, idxFlag):
        if ',' not in set(tok) or (len(tok) != len(pos)):
            if idxFlag: return tok, pos, False;
            else: return tok,pos;
        saveTag = [];
        saveTok = [];
        newTok = [];
        newTag = [];
        idxs = [];
        incpEnd = False;
        idxs.append(0);
        for i,word in enumerate(tok):
            # not comma, part of same phrase
            if not self.c.ID.isEndPhrasePunc(word):
                saveTok.append(word);
                saveTag.append(pos[i]);
                incpEnd = True;
            # comma / end punction, add section to ouput list
            # reset temp save
            else:                
                idxs.append(i+1);
                saveTok.append(word);
                saveTag.append(pos[i]);
                newTok.append(saveTok);
                newTag.append(saveTag);
                saveTok = [];
                saveTag = [];
                incpEnd = False;
        # if the original input did not have final end punction
        # ensures we get the last of the input included
        if incpEnd:
            newTok.append(saveTok);
            newTag.append(saveTag);
        if idxFlag:
            return newTok,newTag, idxs;
        else:
            return newTok,newTag;

    # Arranges a question when the question word is preceeded by a verb
    def verbPreArr(self, tok, qIdx):
        qTok = [];
        beginning = tok[qIdx:];
        qTok += makeList(beginning);
#        qTok += [tok[qIdx-1]];
        if qIdx-1 > 0:
            tok[0] = wordToLower(tok[0]);
            qTok += tok[0:qIdx-1];
        return qTok;
    
    # Arranges a question when the question word is followed by a verb
    def verbPostArr(self, tok, qIdx, pos):
        qTok = [];
        qPart = tok[qIdx:];
        beginning = tok[:qIdx];
        beginTag = pos[:qIdx];
        # check if the beginning of the sentence has a verb
        # (indicates a somewhat complete thought, 
        # probably not necessary in question)
        hasVerb = reduce(lambda x,y: x or y, map(is_verb, beginTag));
        if isinstance(qPart,list):
            qTok += [qPart[0]];
            if not hasVerb and beginTag[-1] != "IN":
                if beginTag[0] == "DT" and isinstance(beginning,list):
                    qTok += beginning[1:];
                else:
                    qTok += beginning;            
            end = qPart[1:];
            qTok += makeList(end);
        else:
            qTok += [qPart];
        # does not copy the first word if what is the second word
        # my socks are black today > my what are black today >
        # what are black today
        if qIdx ==  1:
            tok[0] = wordToLower(tok[0]);
            qTok += tok[0:qIdx];
        return qTok;

    # checks the comma delineated sections for a given pos tag
    # uses the key "NOUN" to indicate any noun and
    # "VERB" to indicate any verb (avoids function pointers)
    # returns the index into the comma list of the first find
    # as well as the found item (a list);
    def findTag(self,newTokList,newTagList, tagCode):
        saveIdx = [];
        found = False;
        for i, phrase in enumerate(newTagList):
            for tag in phrase:
                # found condition, save phrase
                if (tagCode == "NOUN" and is_noun(tag)) or\
                   (tagCode == "VERB" and is_verb(tag)) or\
                   (tag == tagCode):
                    found = True;
            if found:
                saveIdx.append(i);
            found = False;
        # no find, return None
        if saveIdx == []:
            return None;
        # something found, return last find (closest to verb);
        else:            
            return saveIdx[-1],makeList(newTokList[saveIdx[-1]]);

    # rearrangeBV - rearrange a sentence when a being verb is present
    # so that the question reads [verb] [beinning] [end] ?
    # (Forms yes questions without adding / changing word tokens)
    def rearrangeBV(self,vbIdx):
        if vbIdx < 0:
            return False;
        pos = self.tags;
        tok = self.tokens;        
        self.rmEndPunc(tok);
        verb = tok[vbIdx];
        preVerb = [];
        postVerb = [];
        qTok = [];
        saveIdx = None;
        newTok = None;
        # start of sentence
        if vbIdx > 0:
            preVerb = makeList(tok[:vbIdx]);
            preVerb[0] = wordToLower(preVerb[0]);
            # break at commas if necessary
            newTok, newTag= self.splitCommaBare(preVerb,pos[:vbIdx], False);
            if newTok != preVerb:
                saveIdx, preVerb = self.findTag(newTok,newTag,"NOUN");
        # end of sentence
        if vbIdx < len(tok)-1:
            postVerb = makeList(tok[vbIdx+1:]);
        # put phrases w/o subject first
        if newTok != None and saveIdx != None:
            for phrase in newTok:
                if phrase != newTok[saveIdx]:
                    qTok += phrase;
        # "meat" of the setence
        qTok += [verb] + preVerb + postVerb;
        # formatting output
        self.joinQ(qTok);
        return True;

    # If the question is a "who" question,
    # remove a trailing article before "who" in the output,
    # checked for more general cases in formatQ
    def removeLeadingArticle(self):
        toks = self.tokens;
        tags = self.tags;
        if self.qWord != None:
            (idx, word) = self.qWord;
            if word == "who" and idx > 0:
                if tags[idx-1] == "DT":
                    toks.pop(idx-1);
                    tags.pop(idx-1);
                    self.qWord = (idx-1,word);
                    return;
        return;

    # rmEndPunc - remove end punction from the given token string
    # DOES NOT REMOVE from the associated pos, unless run on that separately
    def rmEndPunc(self,tok):
        punc = tok[-1];
        if self.c.ID.isEndPhrasePunc(punc):
            x = tok.pop(-1);
        return;

    # rearranges sentences to flow more naturally
    def formatQuestion(self):
        # split sentences by commas, keeping only the phrase 
        # with the question word 
        # PROS: simplifies question, easier to make grammatical
        # CONS: ambiguity, possible erradication of important points
        #### currently everything is reattached later
        if self.qWord == None:
            self.out = "";
            return;
        else:
            self.removeLeadingArticle();
            (phraseTok, phraseTag, (pSel,idxOffset)) = self.splitComma();
            if pSel != -1:
                tok = phraseTok[pSel];
                pos = phraseTag[pSel];
            else:
                tok = phraseTok;
                pos = phraseTag;
            self.rmEndPunc(tok);
            (qIdx, wrd) = self.qWord;
            qIdx = qIdx - idxOffset;
            if qIdx != 0:
                # question word follow a verb
                if is_verb(pos[qIdx-1]):
                    qTok = self.verbPreArr(tok,qIdx);
                # question word preceeds a verb
                elif qIdx < len(tok) and \
                     (is_verb(pos[qIdx+1]) or pos[qIdx+1] == "MD"):
                    qTok = self.verbPostArr(tok,qIdx,pos);
                # question word in preposition etc
                else: qTok = tok;
            # case: question word already in front, 
            #   only need to change punctuation
            else: qTok = tok;
            # add other details back into the question
            for i, phrase in enumerate(phraseTok):
                if pSel != -1 and i != pSel:
                    qTok += ",";
                    addPhrase = phrase[0:-1];
                    tokTags = rdrpos.pos_tag("".join(addPhrase[0]));
                    if tokTags[0] != "NNP":
                        addPhrase[0] = addPhrase[0].lower();
                    if len(addPhrase) > 1:
                        qTok += addPhrase;
            self.joinQ(qTok);
            return;

    # Turn the question from a list into a string question
    # Set output and capitalization
    def joinQ(self, qTok):
        qTok += ['?'];
        # special join function to remove extra spaces
        question = self.c.sentJoin(qTok); 
        # capitalize first letter
        self.out = question[0].upper() + question[1:];
        return;

    # creates question by replacing the first date
    # replaces with "what" or "what date" instead of "when" 
    # because that seems to work better grammatically most of the time    
    # returns True on success, False on failure
    def qFromDate(self):
        tok = self.tokens;
        pos = self.tags;
        origN = self.N
        if "#DATE" in set(pos):
            idx = pos.index("#DATE");
            # only year specified
            if len(tok[idx]) == 4:
                tok[idx] = "what year";
            # preposition case
            elif idx < len(tok)-1 and pos[idx+1] == "IN":
                tok[idx] = "when";
            # follows a verb
            elif idx > 0 and is_verb(pos[idx-1]):
                    tok[idx] = "what";
            else:
                tok[idx] = "what date";
            self.qWord = (idx, tok[idx]);
            return True;
        else: return False;

    # create a quation from a quantity value
    # error prone
    """
    def qFromQuant(self):
        tok = self.tokens;
        pos = self.tags;
        if "CD" in set(pos):
            idx = pos.index("CD");
            phrase = [];
            phrasetok = [];
            i = idx;
            token = None;
            tag = None;
            while(i < len(pos) and tag not in set(string.punctuation)):
                if token not in set(string.punctuation) and token != None:
                    phrase.append(token);
                    phrasetok.append(tag);
                    if tag == "NNS":
                        break;
                i += 1;
                token = tok[i];
                tag = pos[i];
            if phrase != []:
                print phrase, phrasetok;
    """
    # replaces the noun at the given index, idx with the
    # appropriate question word
    # returns True on success, False on failure 
    def replaceNounWithQ(self, idx):
        tok = self.tokens;
        pos = self.tags;
        nounTag = pos[idx];
        word = tok[idx];
        # error with input, no noun to replace, erroneous index
        if (idx < 0 or idx > len(pos)) or \
           (not is_noun(nounTag) and nounTag != "PRP"):
            return False;        
        # proper noun replacement
        if (len(nounTag) > 2 and nounTag[0:3] == "NNP"):
            tok[idx] = "who or what";
        # pronoun replacement
        elif nounTag == "PRP":
            pFlag = self.c.ID.isReplacablePronoun(word);
            if pFlag == 1:  #subject
                tok[idx] = "who";
            elif pFlag == -1: # object
                tok[idx] = "whom";
            elif pFlag == -2: # posessive
                tok[idx] = "whose";
            elif pFlag == 2: # cannot specify (it, there)
                tok[idx] = "what";
            else:
                return False;
        # common noun replacement
        else:
            tok[idx] = "what";
        # remove leading determiner if present
        if idx > 0 and pos[idx-1] == "DT":
            pos.pop(idx-1);
            tok.pop(idx-1);
            idx = idx -1;
        # save the index of the question word (used in rearranging qurestion)
        self.qWord = (idx, tok[idx]);
        return True;

    # replace the first noun / propernoun / pronoun that proceeds
    # a verb with an appropriate question word
    # returns True on successful replacement, False on failure
    def qFromNoun(self):
        pos = self.tags;
        lastCandidate = None;
        for i,tag in enumerate(pos):
            # last noun / proper noun
            if is_noun(tag):
                lastCandidate = i;
            elif tag == "PRP" and \
                 (self.c.ID.isReplacablePronoun(self.tokens[i]) != 0):
                lastCandidate = i;
            # found verb, take most recent candidate word
            elif is_verb(tag):
                if lastCandidate != None:
                    return self.replaceNounWithQ(lastCandidate);
        return False;

    # replace the first pronoun in the sentence with who
    # not used because the version included in the noun replacement 
    # works more grammatically
    """
    def qFromPronoun(self):
        pos = self.tags;
        tok = self.tokens;
        for i,tag in enumerate(pos):
            if tag == "PRP" and self.c.ID.isReplacablePronoun(tok[i]):
                self.replaceNounWithQ(i);
                return True;
        return False;"""

    # create simple questions by rearranging a sentence starting with if
    # if "clause", [subset] -> why will [subset]
    def ifQ(self):
        pos = self.tags;
        tok = self.tokens;
        # fail on lack of realization with construct
        if "," not in set(pos):
            return False;
        # split on first comma (associated with "if") 
        idx = pos.index(",");
        if idx < len(pos) - 1:
            subTok = tok[idx+1:];
            subPos = pos[idx+1:];
            # find the first verb modifier to be used in question
            if "MD" in set(subPos):
                modVerbIdx = subPos.index("MD");
                modVerb = subTok[modVerbIdx]; 
                subset = subTok[:modVerbIdx];
                if modVerbIdx < len(pos) - 1:
                    subset += subTok[modVerbIdx+1:];
            # if modifer cannot be found in question, 
            # use general word "will"
            else:
                modVerb = "will";
                subset = subTok;
            subset = ["Why"] + [modVerb] + subset;
            # combine tokens
            self.joinQ(subset);
            return True;
        return False;

    # create simple yes / no questions from a sentence
    # by siwtching the placement of the subject and the being verb
    def qYesNo(self):
        tok = self.tokens;
        pos = self.tags;
        seenVerb = False;
        for i,tag in enumerate(pos):
            if is_verb(tag):
                if self.c.ID.isBeingVerb(tok[i]) and seenVerb == False:
                    self.rearrangeBV(i);
                    return True;
                seenVerb = True;
        return False;

    # overall algorithm for creating questions
    # includes combing portions of the input together
    # heirarchy of sentence constructions:
    #   if, yes/no, date, noun
    def make(self,sentence):
        combi = self.c;
        toks = self.tokens;
        pos = self.tags;

        # find date locations and replace them in the given, toks, pos
        # gives dates the tag "#DATE"
        combi.dates(toks, pos);
        # combine names into a single token,
        # sort of an NER
        combi.names(toks, pos);
        # check for context based on timing (might require change of verb)
        #timeFlag = combi.ID.isTimeDep(toks,0);
        
        if toks[0].lower() == "if" and self.ifQ(): 
            return;
        if self.qYesNo(): 
            return;
        if self.N < 15 and self.qFromDate(): 
            self.formatQuestion();
            return;
        if self.qFromNoun(): 
            self.formatQuestion();
            return;
        return;
