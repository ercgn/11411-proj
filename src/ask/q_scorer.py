#!/usr/bin/python
#
# q_scorer.py
#
# The QuestionScorer class contains all utilities used for scoring a question,
# based on a probabilistic language model trained on the Brown corpus from
# nltk.
#
# Error 501: Not Yet Implemented
#
# Aaron Anderson
#   with
# Eric Gan
# Rachel Kobayashi
#

import kenlm

### CONSTANTS ###

# Location of the training data corpus
CORPUS_FILENAME = '../corpus/BrownCorpus.binary'

class QuestionScorer(object):
    
    # The constructor initializes the language model which is used
    # to analyze the fluency of the questions.
    def __init__(self):
        self.model = kenlm.LanguageModel(CORPUS_FILENAME)
    
    # Takes a question, as a list of tokens, and returns that question's score
    # under the language model.  The score is a negative floating point number
    # representing (I believe) the log of the probability of the sentence under
    # the language model.  Higher (less negative) numbers correspond to better
    # fluency.
    def score(self, questionToks):
        
        # Join the tokens together with whitespace.  It is necessary that each
        # token be separated by whitespace, which is why the input is a list
        # and not a string.
        q_raw = ' '.join(questionToks)
        
        baselineScore = self.model.score(q_raw)
        # We can possibly add more factors than just the baseline
        # probabalistic model here, but for right now this score should serve
        # us well.
        return baselineScore


