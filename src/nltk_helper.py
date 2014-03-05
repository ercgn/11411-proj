# Some code was borrowed since the naive nltk tokenizer wasn't perfect.
# http://stackoverflow.com/questions/14095971/how-to-tweak-the-nltk-sentence-tokenizer

import nltk.data, sys
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.corpus import wordnet
from nltk.stem import porter

def parseFileToSentences(file_name):
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    fp = open(file_name, "r")
    data = fp.read()
    data = data.replace('?"', '? "').replace('!"', '! "').replace('."', '. "')

    sentences = []
    for para in data.split('\n'):
        if para:
            sentences.extend(sentence_splitter.tokenize(para))
    return sentences

def parseTextToSentences(text):
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
    sentence_splitter = PunktSentenceTokenizer(punkt_param)
    data = text
    data = data.replace('?"', '? "').replace('!"', '! "').replace('."', '. "')

    sentences = []
    for para in data.split('\n'):
        if para:
            sentences.extend(sentence_splitter.tokenize(para))
    return sentences

def getSynonyms(word):
    syns = wordnet.synsets(word)
    #To get rid of duplicates, we first convert to set.
    synonyms = list(set([l.name.replace('_', ' ') for s in syns for l in s.lemmas]))
    return synonyms

def areSynonyms(word1, word2):
    return word2 in getSynonyms(word1)

def printSynonyms(word):
    print getSynonyms(word)

def getStem(word):
    stemmer = porter.PorterStemmer()
    return stemmer.stem(word)

def hasSameStem(word1, word2):
    return getStem(word1) == getStem(word2)