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

#uses python sets for speed. 
class Identity():

    def isMonth(self,word):
        return word.lower() in months;

    def isDayOfWeek(self, word):
        return word.lower() in days;

    def isTimeWord(self, word):
        return word.lower() in timewords;

    def isQuestionWord(self,word):
        return word.lower() in qWords;

    # timewords: today, friday, yesterday, etc
    def isTemporal(self, word):
        words = days | timewords;
        return word.lower() in words;

    # return dates in a given phrase
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
            m = re.match('CD (?P<mid>[^\s]{1,4}) CD',newStr);
            if m:
                midTag = m.groupdict()['mid'];
                if len(midTag) >=2 and midTag[0:2] == "NN":                    
                    if self.isMonth(wordList[start+1]):
                        locations.append((start,3));
                elif len(midTag) > 0 and midTag == ",":
                    if idx > 0 and self.isMonth(wordList[start-1]):
                        locations.append((start-1,4));
            # case for a month and day without year
            elif re.match('[^C][^D] NNP CD',newStr) or \
                 re.match(' NNP CD',newStr):
                if self.isMonth(wordList[start+1]):
                    locations.append((start+1, 2));
            elif tag == "CD":
                word = wordList[idx];
                # case for numeric date seprated by slashes
                # accept both year/month/day and month/day/year
                # also year-month-day and month-day-year
                # with both the year as 2 or 4 digits;
                # does not check value of digits
                if re.match('\d{1,2}/\d{1,2}/(\d{4}|\d{2})$',word) or \
                   re.match('(\d{4}|\d{2})/\d{1,2}/\d{1,2}$',word) or \
                   re.match('\d{1,2}-\d{1,2}-(\d{4}|\d{2})$',word) or \
                   re.match('(\d{4}|\d{2})-\d{1,2}-\d{1,2}$',word):
                    locations.append((idx,1));
                # case for year by itself
                # TODO: pin down numeric constraints better. 
                elif re.match('\d{4}$',word):
                    if idx < n-1 and not self.isMonth(wordList[idx+1]):    
                        if word < 3000:
                            print "SUCCESS";
                            locations.append((idx,1));
            tagset.popleft();
        print locations
        return locations;

