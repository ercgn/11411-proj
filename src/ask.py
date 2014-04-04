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
# The algorithm iterates over each reasonable sentence in the article.  A
# reasonable sentence is defined by the combination of several metrics, such
# as a minimum length, presence of a verb, and appropriate ending punctuation.
# For each reasonable sentence, it turns it into a question using the
# ConstructQuestion class from sent_2_q.py, and scores each generated question
# using a probabalistic language model.  The N highest-scoring questions are
# then written to standard out.
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
from util.set_defs import Identity

import util.qutil as qutil
import random
import nltk
import sys

### CONSTANTS ###

# Usage string
usage = """Usage: ./ask.py article_file.htm N
    where article_file.htm is the HTML file containing the article HTML content
    and N is an integer specifying the number of questions to output.
"""

# Minimum number of tokens required in a sentence to turn it into a question
MIN_SENTENCE_LENGTH = 10

### FUNCTIONS ###

# Returns True if the string s can reasonably be described as a sentence
# There are many metrics to decide whether a string is a sentence;
# including length, containing a verb, end punctuation, etc.  The function
# will only return True if each implemented criteria is satisfied.
def isSentence(s):
    # Get the tokens of the sentence.  It's possible there are none,
    # in which case this is definitely not a sentence.
    toks = nltk.word_tokenize(s)
    if len(toks) == 0:
        return False
    
    # Generate the POS tags for the words in the sentence
    tags = [x[1] for x in nltk.pos_tag(toks)]
    
    # Check for existence of verb
    hasVerb = reduce(lambda x,y: x or y, map(qutil.is_verb, tags))
    
    # Check for a reasonable length
    isMinLength = (len(toks) > MIN_SENTENCE_LENGTH)
    
    # Check for correct end punctuation
    i = Identity()
    hasEndPunct = i.isEndPhrasePunc(toks[-1])
    
    # Must have all criteria to be deemed a reasonable sentence
    return hasVerb and isMinLength and hasEndPunct

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
        sentenceList = filter(isSentence, sentenceList)
        
        # Instantiate a QuestionScorer and generate a (question,score) pair
        # for each sentence in the sentenceList
        scorer = QuestionScorer()
        questions = []
        for sent in sentenceList:
            try: 
                constructor = ConstructQuestion(sent)
                q = constructor.out
                if q == '':
                    # Unable to successfully generate a question; discard
                    continue
            except Exception, msg:
                print 'WARNING: Exception in constructing question!'
                print 'Please track this down and figure out what went wrong'
                print msg
                continue
            qToks = nltk.word_tokenize(q.strip())
            s = scorer.score(qToks)
            questions.append((q,s,sent))
        
        # Sort the questions by score in descending order (so highest score
        # questions are first
        questions.sort(key = lambda x: x[1], reverse=True)
        
        # Output the first N questions (these have the highest score)
        for i in xrange(N):
            # TODO: remove.  Prints corresponding sentence for reference only
            print questions[i][2]
            # Print corresponding generated question
            print questions[i][0]
        
        print ''  # blank line (I like blank lines at the end of output!)
        
    except IOError, msg:
        print "An I/O error occurred while processing the article.  Details:"
        print msg
    
    finally :
        # Cleanup
        articleFd.close()

