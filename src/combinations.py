#######
#
# combination.py
#
# utilities for combining related information:
#   words: from subset, group words that appear together in some sample
#   date:  group date information
#######

import rdrpos

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

# return dates in a given phrase
# TODO: clean up algorithm, simplify
    def dates(self, phrase):
        pos = rdrpos.pos_tag(phrase);
        tokens = phrase.strip().split();
        idx = -1;
        numbers = [];
        indicies = [];
        for tag in pos:
            if tag == "CD":
                idx = pos.index(tag,idx+1);
                numbers.append(tokens[idx]);
                indicies.append(idx);
        insertDict = {};
        for idx,listIDX in enumerate(indicies):
            if listIDX > 0:
                word = tokens[listIDX-1];
                if self.ID.isMonth(word):                    
                    insertDict[idx] = word;
        shift = 0;
        for k,v in insertDict.items():
            numbers.insert(k+shift, v);
            shift += 1;
        combined = self.words(numbers, tokens);
        print combined;
        return;

#uses python sets, maybe move or change structure
class Identity():
    def isMonth(self,word):
        calendar = ['january','february','march','april','may','june',
                  'july', 'august','september','october','november','december',
                  'jan','feb','mar','apr','may', 'jun',
                  'jul','aug','sep','sept','oct','nov','dec'];
        months = set(calendar);
        return word.lower() in months;
