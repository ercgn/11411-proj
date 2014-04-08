#!/usr/bin/python
#
# rand_sents.py
#
# Utility to pull N random sentences from an article and put them in
# a file.  (Can be used for testing question generation without having
# to manually extract sentences from the articles.)
#
# Usage:
#  ./rand_sents.py N article_file.htm output_file.txt
#  
#    N is the number of sentences to pull
#    article_file.htm is the file to pull sentences from
#    output_file.txt is the name of the file to write the sentences to
#      If - is used, write to standard output.
#
#  Not all arguments are necessary; in fact, none are necessary (see the
#  specified defaults below).  However, the arguments must be fully
#  specified up to the last one given (e.g. N must be specified before any
#  filenames are given).
#  
#  If not all the command line inputs are specified, the program uses
#  the following defaults:
#    N = 10
#    article_file.htm = ../data/set1/a2.htm
#    output_file.txt = test_files/rand_sents.txt
#  These defaults can be easily changed by editing the Default Parameters
#  section below.
#
#
# Error 501: Not Yet Implemented
# 
# Aaron Anderson
#   with
# Eric Gan
# Rachel Kobayashi
#

### IMPORTS ###

from util.article_parser import MyHTMLParser
from util.qutil import isSentence

import random
import sys

### CONSTANTS ###

# Default Parameters
DEFAULT_N = 10
DEFAULT_ARTICLE_FILENAME = '../data/set1/a2.htm'
DEFAULT_OUTPUT_FILENAME = 'test_files/rand_sents.txt'

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

# Parses the command line and gets the appropriate program parameters
# Returns a tuple (N, articleFilename, outputFilename) with the specified
# values, or default values if none were specified.
def getInputs():
    # Set defaults
    inputs = [DEFAULT_N, DEFAULT_ARTICLE_FILENAME, DEFAULT_OUTPUT_FILENAME]
    
    args = sys.argv[1:]
    for i in range(min(len(inputs),len(args))):
        if i == 0:
            # First argument is an integer
            inputs[i] = int(args[i])
        else:
            inputs[i] = args[i]
    
    return tuple(inputs)

### MAIN ###
if __name__ == "__main__":
    
    (N, articleFilename, outputFilename) = getInputs()
    print "Getting %d sentences from %s" % (N, articleFilename)
    print "Output will be written to %s" % (outputFilename)
    print "Read the source comments for more options!"
    
    # Attempt to open the article file
    try:
        articleFd = open(articleFilename, 'r')
    except IOError:
        sys.exit("Error: Could not find article file: %s\n" % (articleFilename))
    
    # Attempt to open output file
    if outputFilename == '-':
        outputFd = sys.stdout
    else:
        try:
            outputFd = open(outputFilename, 'w')
        except IOError:
            print "Error: Could not open output file for writing: %s\n" % (outputFilename)
            articleFd.close()
            sys.exit()
    
    # Read text of the article and turn sentences into questions
    try:
        parser = MyHTMLParser()
        text = articleFd.read()
        parser.feed(text)
        
        # Retrieve the list of sentences within the article from the parser
        sentenceList = parser.grabTextSentenceList()
        sentenceList = filter(isSentence, sentenceList)
        
        # Pick N random sentences
        (randSentences, k) = pickSentences(sentenceList, N)
        
        # Write sentences to outputFd
        for sent in randSentences:
            outputFd.write(sent + '\n')
        
    except IOError, msg:
        print "An I/O error occurred while processing.  Details:"
        print msg
    
    finally :
        # Cleanup
        articleFd.close()
        outputFd.close()

