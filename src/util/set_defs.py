#!/usr/bin/python
#
# set_defs.py
#
# Class inclues  all set defintions 
# Allow defining set of accepted values and quick membership checking
#
# Rachel Kobayashi
#   with
# Aaron Anderson
# Eric Gan
#
#

import re;
from collections import deque;
from qutil import *

# set definitions here
# allows for quick change
# and quick intersection / union, subtraction of sets
# be CAREFUL of abbreviations (converts to lower for check);
months = set(['january','february','march','april','may','june',
              'july', 'august','september','october','november','december',
              'jan','feb','mar','apr','may', 'jun',
              'jul','aug','sep','sept','oct','nov','dec']);
days = set(['monday','tuesday','wednesday',
            'mon', 'tue','tues','wed','thur','thu','fri','sat','sun'
            'thursday','friday','saturday','sunday',]);
timewords = set(['today','tomorrow','yesterday']);
qWords = set(['who','what','where','when','why','did','do','does','is','was','how']);
namePre = set(['mr.', 'mrs.', 'ms.', 'dr.', 'miss']);
linkVerb = set(['is', 'am', 'are','was']);
endPhrasePunc = set(['!', ',','.',';','?']);

## REGULAR EXPRESSION STRINGS
# (note there is an alernative way of savying the expression,
# but that is mostly applied when used multiple times)
# dates divided by foward slashes or dashes
# accept both year/month/day and month/day/year
# also year-month-day and month-day-year
# with both the year as 2 or 4 digits;
# does not check value of digits
RE_DATE_FSLH1 = '\d{1,2}/\d{1,2}/(\d{4}|\d{2})$';
RE_DATE_FSLH2 = '(\d{4}|\d{2})/\d{1,2}/\d{1,2}$'
RE_DATE_DASH1 = '\d{1,2}-\d{1,2}-(\d{4}|\d{2})$'
RE_DATE_DASH2 = '(\d{4}|\d{2})-\d{1,2}-\d{1,2}$'
# tag sequence is number [anything] number
RE_CD_EP_CD = 'CD (?P<mid>[^\s]{1,4}) CD'
# tag sequence is [not_number] proper_noun number
RE_X_NNP_CD = '([^C][^D]+) NNP CD'
#  re.match(' NNP CD',newStr):

#uses python sets for speed. 
class Identity(object):

    def isEndPhrasePunc(self,word):
        return word.lower() in endPhrasePunc;

    def isMonth(self,word):
        return word.lower() in months;

    def isDayOfWeek(self, word):
        return word.lower() in days;

    def isTimeWord(self, word):
        return word.lower() in timewords;

    def isQuestionWord(self,word):
        return word.lower() in qWords;

    def isNamePre(self, word):
        return word.lower() in namePre;

    def isLinkVerb(self,word):
        return word.lower() in linkVerb;

    # timewords: today, friday, yesterday, etc
    def isTemporal(self, word):
        words = days | timewords;
        return word.lower() in words;

    # > 0 to check for days of the week
    # < 0 to check for today, tommorrow, yesterday
    # = 0 to check for both
    def isTimeDep(self, wordList, ckCode):
        for word in wordList:
            if ckCode < 0 and self.isTimeWord(word):
                return True;
            elif ckCode > 0 and self.isDayOfWeeK(word):
                return True;
            elif ckCode == 0 and self.isTemporal(word):
                return True;
        return False;

    # return dates in a given phrase
    # TODO pin down numerical constraints better
    def findDates(self, wordList, tagList):
        n = len(wordList);
        tagset = deque(["",""]);
        tag = "";
        locations = [];
        for idx in range(0,n):
            start = idx -2;
            tag = tagList[idx];
            tagset.append(tag);
            newStr = q2str(tagset,3);
            m = re.match(RE_CD_EP_CD,newStr);
            if m:
                midTag = m.groupdict()['mid'];
                if len(midTag) >=2 and midTag[0:2] == "NN":                    
                    if self.isMonth(wordList[start+1]):
                        locations.append((start,3));
                elif len(midTag) > 0 and midTag == ",":
                    if idx > 0 and self.isMonth(wordList[start-1]):
                        locations.append((start-1,4));
            # case for a month and day without year
            # contains errors with regular expression
            elif re.match(RE_X_NNP_CD,newStr) or \
                 newStr == ' NNP CD':
                if self.isMonth(wordList[start+1]):
                    locations.append((start+1, 2));
            elif tag == "CD":
                word = wordList[idx];
                # case for numeric date seprated by slashes or dashes
                if re.match(RE_DATE_FSLH1,word) or \
                   re.match(RE_DATE_FSLH2,word) or \
                   re.match(RE_DATE_DASH1,word) or \
                   re.match(RE_DATE_DASH2,word):
                    locations.append((idx,1));
                # case for year by itself
                elif re.match('\d{4}$',word):
                    if idx < n-1 and not self.isMonth(wordList[idx+1]):    
                        if int(word) > 0 and int(word) < 2100:
                            locations.append((idx,1));
            tagset.popleft();
        return locations;

    def findNmPrefix(self, wordList, tagList):
        prevTag = tagList[0];
        locations = [];
        for idx in range(1, len(tagList)):
            tag = tagList[idx];
            if prevTag == "NNP" and tag == "NNP":
                if self.isNamePre(wordList[idx-1]):
                    if idx < len(tagList) and tagList[idx+1] == "NNP":
                        locations.append((idx-1, 3));
                    else:
                        locations.append((idx-1, 2));
            prevTag = tag;
        return locations;
