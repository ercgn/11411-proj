#!/usr/bin/python
#
# gen_sent2q.py
#
# Given a sentence, this class can be used to turn the sentence into a question
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

# "easy" cases to replace:
#   dates -> when
#   numbers -> how many [noun] [verb phrase]?
#   names / proper nouns

class ConstructQuestion(object):
    def __init__(self, sentence):
        self.c = Combine();
        self.tokens = nltk.word_tokenize(sentence.strip());
        self.tags = rdrpos.pos_tag(sentence.strip());
        self.nltkTags = nltk.pos_tag(self.tokens);
        # check if capitaliaztion is necessary and otherwise remove. 
        if (self.nltkTags[0] != self.tags[0]) and \
           self.c.ID.isReplacablePronoun(self.tokens[0]):
            self.tokens[0] = self.tokens[0].lower();
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
        if ',' not in set(tok):
            return tok,pos, (-1,0);
        saveTag = [];
        saveTok = [];
        newTok = [];
        newTag = [];
        idxs = [];
        idxs.append(0);
        for i,word in enumerate(tok):
            if not self.c.ID.isEndPhrasePunc(word):
#                if 1 < i and i < len(tok)-1 and pos[i-1] == "JJ" and pos[i+1] == "JJ": 
                saveTok.append(word);
                saveTag.append(pos[i]);
            else:
                idxs.append(i+1);
                saveTok.append(word);
                saveTag.append(pos[i]);
                newTok.append(saveTok);
                newTag.append(saveTag);
                saveTok = [];
                saveTag = [];
        idxs.append(len(tok));
        (qIdx, qWord) = self.qWord;
        for idx in range(len(idxs)-1):
            if idxs[idx] <= qIdx and qIdx < idxs[idx+1]: 
                return (newTok, newTag, (idx, idxs[idx]));
        return newTok, newTag, (0,0);

    # Arranges a question when the question word is preceeded by a verb
    def verbPreArr(self, tok, qIdx):
        qTok = [];
        beginning = tok[qIdx:];
        if isinstance(beginning,list):
            qTok += beginning;
        else:
            qTok += [beginning];
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
            if isinstance(end,str):
                qTok += [end];
            else:
                qTok += end;
        else:
            qTok += [qPart];
        # does not copy the first word if what is the second word
        # my socks are black today > my what are black today >
        # what are black today
        if qIdx ==  1:
            tok[0] = wordToLower(tok[0]);
            qTok += tok[0:qIdx];
        return qTok;

    # rearrangeBV - rearrange a sentence when a being verb is present
    # so that the question reads [verb] [beinning] [end] ?
    # (Forms yes questions without adding / changing word tokens)
    def rearrangeBV(self,vbIdx):
        # to do: undo sentence start capitalization
        if vbIdx < 0:
            return False;
        pos = self.tags;
        tok = self.tokens;        
        self.rmEndPunc(tok);
        # splicing sentence
        verb = tok[vbIdx];
        begining = [];
        end = [];
        # start of sentence
        if vbIdx > 0:
            beginning = tok[:vbIdx];
            if isinstance(beginning,str):
                beginning = [beginning];
        # end of sentence
        if vbIdx < len(tok)-1:
            end = tok[vbIdx+1:];
            if isinstance(end,str):
                end = [end];
        qTok = [verb] + beginning + end;
        # formatting output
        self.joinQ(qTok);
        return;

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
                    return
        return;
        
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
#                    print "pre";
                    qTok = self.verbPreArr(tok,qIdx);
                # question word preceeds a verb
                elif qIdx < len(tok) and (is_verb(pos[qIdx+1]) or pos[qIdx+1] == "MD"):
                    qTok = self.verbPostArr(tok,qIdx,pos);
                # question word in preposition etc
                else: qTok = tok;
            # case: question word already in front, 
            #   only need to change punctuation
            else: qTok = tok;
            # add other details back into the question
            for i, phrase in enumerate(phraseTok):
                if pSel != -1 and i != pSel:
                    #print phrase;
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
        question = self.c.sentJoin(qTok);
        # capitalize first letter
        self.out = question[0].upper() + question[1:];
        return;

    # creates question by replacing the first date
    # replaces with "what" or "what date" instead of "when" 
    # because that seems to work better grammatically most of the time
    def qFromDate(self):
        tok = self.tokens;
        pos = self.tags;
        origN = self.N
        if "#DATE" in set(pos):
            idx = pos.index("#DATE");
            if len(tok[idx]) == 4:
                tok[idx] = "what year";
            elif idx < len(tok)-1 and pos[idx+1] == "IN":
                tok[idx] = "when";
            elif idx > 0 and is_verb(pos[idx-1]):
                    tok[idx] = "what";
            else:
                tok[idx] = "what date";
            self.qWord = (idx, tok[idx]);
            return True;
        else: return False;

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
    # creates a question by replacing the first noun or pronoun 
    # that preceeds a verb with "what or who" as appropriate"
    def replaceNounWithQ(self, idx):
        tok = self.tokens;
        pos = self.tags;
        nounTag = pos[idx];
        word = tok[idx];
        if (len(nounTag) > 2 and nounTag[0:3] == "NNP"):
            tok[idx] = "who or what";
        elif nounTag == "PRP":
            pFlag = self.c.ID.isReplacablePronoun(word);
            if pFlag == 1:
                tok[idx] = "who";
            elif pFlag == -1:
                tok[idx] = "whom";
            elif pFlag == -2: 
                tok[idx] = "whose";
            elif pFlag == 2:
                tok[idx] = "what";
        else:
            tok[idx] = "what";
        if idx > 0 and pos[idx-1] == "DT":
            pos.pop(idx-1);
            tok.pop(idx-1);
            idx = idx -1;
        self.qWord = (idx, tok[idx]);
        return;

    def qFromNoun(self):
        pos = self.tags;
        lastCandidate = None;
        for i,tag in enumerate(pos):
            if is_noun(tag):
                lastCandidate = i;
            elif tag == "PRP" and \
                 (self.c.ID.isReplacablePronoun(self.tokens[i]) != 0):
                lastCandidate = i;
            elif is_verb(tag):
                if lastCandidate != None:
                    self.replaceNounWithQ(lastCandidate);
                    return True;
        return False;

    # replace the first pronoun in the sentence with who
    def qFromPronoun(self):
        pos = self.tags;
        tok = self.tokens;
        for i,tag in enumerate(pos):
            if tag == "PRP" and self.c.ID.isReplacablePronoun(tok[i]):
                self.replaceNounWithQ(i);
                return True;
        return False;

    def ifQ(self):
        pos = self.tags;
        tok = self.tokens;
        if "," not in set(pos):
            return "";
        else:
            idx = pos.index(",");
            if idx < len(pos) - 1:
                subTok = tok[idx+1:];
                subPos = pos[idx+1:];
                if "MD" in set(subPos):
                    modVerbIdx = subPos.index("MD");
                    modVerb = subTok[modVerbIdx]; 
                    subset = subTok[:modVerbIdx];
                    if modVerbIdx < len(pos) - 1:
                        subset += subTok[modVerbIdx+1:];
                else:
                    modVerb = "will";
                    subset = subTok;
                subset = ["Why"] + [modVerb] + subset;
                self.joinQ(subset);
        return;
    """
    def qFromNoun(self):        
        tok = self.tokens;
        pos = self.tags;
        for i,tag in enumerate(pos[0:-1]):
            nextTag = pos[i+1];
            if is_verb(nextTag):    
                if is_noun(tag):
                    if len(tag) > 2 and tag[0:3] == "NNP":
                        tok[i] = "who";
                    else:
                        tok[i] = "what";
                    self.keyVerb = (i+1,pos[i+1]);
                    self.qWord = (i, tok[i]);
                elif tag == "PRP":
                    tok[i] = "who";
                    self.keyVerb = (i+1, pos[i+1]);
                    self.qWord = (i, tok[i]);
                return True;
        return False;
    """
    def qYesNo(self):
        tok = self.tokens;
        pos = self.tags;
        for i,tag in enumerate(pos):
            if is_verb(tag) and self.c.ID.isBeingVerb(tok[i]):
                self.rearrangeBV(i);
                return True;
        return False;

    def make(self,sentence):
        combi = self.c;
        toks = self.tokens;
        pos = self.tags;

        # find date locations and replace them in the given, toks, pos
        combi.dates(toks, pos);
        combi.names(toks, pos);
#        print "TOKS: ",self.tokens;
#        print "pos:: ",self.tags;
        # check for context based on timing (might require change of verb)
#        timeFlag = combi.ID.isTimeDep(toks,0);
        """
        if toks[0].lower() == "if":
            self.ifQ();
            return;
        if self.N < 15 and self.qFromDate(): 
            self.formatQuestion();
            return;
        if self.qFromNoun(): 
            self.formatQuestion();
            return;"""
        self.qYesNo();
        return;
