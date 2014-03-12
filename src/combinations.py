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

class Combine:
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

    def dates(self, words, tags, location):
        lengthAdj = 0;
        date = [];
        for place in location:
            (startIdx, n) = place;
            insertIdx = startIdx - lengthAdj;
            for i in range(0,n):
                date.append(words.pop(insertIdx));
                tags.pop(insertIdx);
            words.insert(insertIdx, " ".join(date));
            tags.insert(insertIdx, "#DATE");
            lengthAdj += (n-1);
        return
