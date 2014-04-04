#!/usr/bin/python
#
# ask.py
#
# Runs the utility for generating questions from article text.
#
# Usage: ./ask.py article_file.htm N
#  where article_file.htm is the HTML file containing the article HTML content
#  and N is an integer specifying the number of questions to output.
#
# The algorithm picks c*N sentences from the article text at random, where c
# is a constant.  It then turns them into questions using the
# ConstructQuestion class from sent_2_q.py, and scores each one using a
# probabalistic language model.  The N highest-scoring questions are then
# written to standard out.
#
# Error 501: Not Yet Implemented
#
# Aaron Anderson
#   with
# Eric Gan
# Rachel Kobayashi
#

### IMPORTS ###

from ask.q_scorer import QuestionScorer
from ask.sent_2_q import ConstructQuestion
from util.article_parser import MyHTMLParser

import random
import nltk
import sys

### CONSTANTS ###

# Usage string
usage = """Usage: ./ask.py article_file.htm N
    where article_file.htm is the HTML file containing the article HTML content
    and N is an integer specifying the number of questions to output.
"""

# C is the proportion of questions generated to questions output.
# I.e. if the desired number of questions is N, the number of
# questions generated will be C*N.  The program then outputs the
# N questions with the highest scores.
#
# TODO:
# This is in lieu of a model where we repeatedly generate questions
# until we have N questions with a score above some absolute threshold.
# We should talk about which model is more desirable, and why, or if we
# want to combine both models in some fashion.
C = 10

### FUNCTIONS ###

# Picks n random sentences out of the given list of sentences without
# replacement.  Output is a tuple (sentences, k) where sentences is a list
# of unique sentences chosen from sentenceList, and k is the number of
# sentences that were chosen.
# In the ideal case, k == n, but if len(sentenceList) < n,
# k == len(sentenceList) instead and sentences == sentenceList
def pickSentences(sentenceList, n):
    if len(sentenceList) < n:
        return (sentenceList, len(sentenceList))
    else:
        # Pick n random indices without replacement from which
        # we will select the sentences
        indices = random.sample(xrange(len(sentenceList)), n)
        sentences = [sentenceList[i] for i in indices]
        return (sentences, len(sentences))

# Returns True if the string s contains any alphanumeric character.
# Needed to filter the sentence list to remove any "sentences" which are
# really just empty space or newlines.
def containsAlphanum(s):
    return reduce(lambda x,y: x or y, [c.isalpha() for c in s])

# Checks for the presence and right number of command line
# arguments, and returns the article filename and number of
# questions to generate as a tuple (filename, n)
# If there are not the right number of arguments, the function
# prints the usage message and exits the program.
def getInputs():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(usage);
    n = int(args[1])
    return (args[0], n)

### MAIN ###
if __name__ == "__main__":
    
    # Get the arguments from the command line
    (articleFilename, N) = getInputs()
    
    # Attempt to open the article file
    try:
        articleFd = open(articleFilename, 'r')
    except IOError:
        print "Could not find article file: %s\n" % (articleFilename)

    # Read text of the article and turn sentences into questions
    try:
        parser = MyHTMLParser()
        text = articleFd.read()
        parser.feed(text)
        
        # Retrieve the list of sentences within the article from the parser
        sentenceList = parser.grabTextSentenceList()
        sentenceList = filter(containsAlphanum, sentenceList)
        
        # Pick C*N sentences which will be turned into questions
        (shortSentenceList, k) = pickSentences(sentenceList, C*N)
        
        # Instantiate a QuestionScorer and generate a (question,score) pair
        # for each sentence in shortSentenceList
        scorer = QuestionScorer()
        questions = []
        for sent in shortSentenceList:
            print sent
            constructor = ConstructQuestion(sent)
            q = constructor.out
            print q
            qToks = nltk.word_tokenize(q.strip())
            s = scorer.score(qToks)
            questions.append((q,s))
        
        # Sort the questions by score in descending order (so highest score
        # questions are first
        questions.sort(key = lambda x: x[1], reverse=True)
        
        # Output the first N questions (these have the highest score)
        for i in xrange(N):
            print questions[i][0]
        
        print ''  # blank line (I like blank lines at the end of output!!!)
        
    except IOError, msg:
        print "An I/O error occurred while processing the article.  Details:"
        print msg
    
    finally :
        # Cleanup
        articleFd.close()

