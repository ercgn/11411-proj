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
import nltk
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
        qTok += [tok[qIdx-1]];
        if qIdx-1 > 0:
            tok[0] = wordToLower(tok[0]);
            qTok += tok[0:qIdx-1];
        return qTok;
    
    # Arranges a question when the question word is followed by a verb
    def verbPostArr(self, tok, qIdx):
        qTok = [];
        beginning = tok[qIdx:];
        if isinstance(beginning,list):
            qTok += beginning;
        else:
            qTok += [beginning];
        # does not copy the first word if what is the second word
        # my socks are black today > my what are black today >
        # what are black today
        if qIdx-1 > 0:
            tok[0] = wordToLower(tok[0]);
            qTok += tok[0:qIdx];
        return qTok;

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
            punc = tok[-1];
            # add question mark. 
            if self.c.ID.isEndPhrasePunc(punc):
                x = tok.pop(-1);
            (qIdx, wrd) = self.qWord;
            qIdx = qIdx - idxOffset;
            if qIdx != 0:
                # question word follow a verb
                if is_verb(pos[qIdx-1]):
                    qTok = self.verbPreArr(tok,qIdx);
                # question word preceeds a verb
                elif qIdx < len(tok) and is_verb(pos[qIdx+1]):
                    qTok = self.verbPostArr(tok,qIdx);
                # question word in preposition etc
                else: qTok = tok;
            # case: question word already in front, 
            #   only need to change punctuation
            else: qTok = tok;
            # add other details back into the question
            for i, phrase in enumerate(phraseTok):
                if pSel != -1 and i != pSel:
                    #print phrase;
                    qTok += phrase[0:-1];
            qTok += ['?'];            
            question  =  self.c.sentJoin(qTok);        
            # capitalize first letter
            self.out =  question[0].upper() + question[1:];
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

    # creates a question by replacing the first noun or pronoun 
    # that preceeds a verb with "what or who" as appropriate"

    def replaceNounWithQ(self, idx):
        tok = self.tokens;
        pos = self.tags;
        nounTag = pos[idx];
        word = tok[idx];
        if (len(nounTag) > 2 and nounTag[0:3] == "NNP"):
            tok[idx] = "who";
        elif nounTag == "PRP":
            pFlag = self.c.ID.isReplacablePronoun(word);
            if pFlag == 1:
                tok[idx] = "who";
            elif pFlag == -1:
                tok[idx] = "whom";
        else:
            tok[idx] = "what";       
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
    def make(self,sentence):
        combi = self.c;
        toks = self.tokens;
        pos = self.tags;

        # find date locations and replace them in the given, toks, pos
        combi.dates(toks, pos);
        combi.names(toks, pos);
        print "TOKS: ",self.tokens;
#        print "pos:: ",self.tags;
        # check for context based on timing (might require change of verb)
#        timeFlag = combi.ID.isTimeDep(toks,0);
        if self.N < 15 and self.qFromDate(): 
            self.formatQuestion();
            return;
        if self.qFromNoun(): 
            self.formatQuestion();
            return;
        return;
