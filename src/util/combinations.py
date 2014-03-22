#!/usr/bin/python
#
# combinations.py
#
# class for combining related information:
#   words: from subset, group words that appear together in some sample
#   dates: given the location and length of dates, group, replace tag
#
# Rachel Kobayashi
#   with
# Aaron Anderson
# Eric Gan
#
#

import rdrpos
from set_defs import Identity;
#import util.qutil

DATE_TAG = "#DATE";

class Combine(object):
    def __init__(self):
        self.ID = Identity();

    # combines words in the list "words" 
    #if they appear next to each other in the given string "question"
    # probably  not super efficient right now
    def words(self,words, question):
        Q = len(question);
        combined = [];
        x = 0;
        idx = -1;
        if len(words) <= 1:
            return words;
        while x < len(words):
            idx = question.index(words[x], idx+1);
            phrase = "";
            if idx < Q-1:
                y = 0;
                while x + y < len(words) and question[idx + y] == words[x + y]:
                    phrase += words[x + y] + " ";
                    y+=1;
                combined.append(phrase.strip());
                x += y;
            else:
                combined.append(words[x]);
                x += 1;
        return combined;

    # wrapper function to the regular join function 
    # meant for sentences (wordList joined by spaces)
    # combines commas in a natural method. 
    # combines 's and . as well 
    def sentJoin(self,wordList):
        rmList = [];
        for i,word in enumerate(wordList):
            if i > 0: 
                if word == "," or word[0] == "'" or word == ".":
                    prev = wordList[i-1];
                    prev += word;
                    wordList[i-1] = prev;
                    rmList.append(i);
        offset = 0;
        for index in rmList:
            wordList.pop(index-offset); 
            offset += 1;
        sentence = " ".join(wordList);
        return sentence;

    def joinWordTag(self, locations, replaceStr):
        if self.words == None or self.tags == None:
            return 0;
        else:
            save = [];
            lengthAdj = 0;
            toks = self.words;
            pos = self.tags;
            for place in locations:
                (startIdx, n) = place;
                insertIdx = startIdx - lengthAdj;
                for i in range(0,n):
                    save.append(toks.pop(insertIdx));
                    pos.pop(insertIdx);
                toks.insert(insertIdx, " ".join(save));
                save = [];
                pos.insert(insertIdx, replaceStr);
                lengthAdj += (n-1);
        return 1;

    # dates combines dates into a single entity 
    # both in the "words" token list
    # and in the tags list, with the tag "#DATE"
    # dateLoc is a list of tuples (i,n)
    #   where i is the start index of the date
    #   and n is the length (in tokens) of the date
    def dates(self, words, tags):
        dateLoc = self.ID.findDates(words,tags);
        self.words = words;
        self.tags = tags;
        success = self.joinWordTag(dateLoc, DATE_TAG);
        words = self.words;
        tags = self.tags;
        self.words = None;
        self.tags = None;
        return;

    def names(self, words, tags):
        nameLoc = self.ID.findNmPrefix(words, tags);
        self.words = words;
        self.tags = tags;
        success = self.joinWordTag(nameLoc,"NNP_PER");
        words = self.words;
        tags = self.tags;
        self.words = None;
        self.tags = None;
        return;
