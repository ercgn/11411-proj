#!/usr/bin/python
#
# rdrpos.py
#
# Wrapper module for the RDR POS tagger written by Dat Quoc Nguyen,
# Dai Quoc Nguyen, Dang Duc Pham, and Son Bao Pham
# Contains one convenience method for easily tagging a string (similar
# to functionality provided by nltk.pos_tag)
#
# Aaron Anderson
#   with
# Rachel Kobayashi
# Eric Gan
#
#

from RDR_POS.pSCRDRtagger.EnPOS import EnRDRTree
from RDR_POS.Utility.Utils import readDictionary
import os

def pos_tag(text):
    r = EnRDRTree()
    r.constructTreeFromRulesFile('RDR_POS/Trained/EN.RDR')
    dictionary = readDictionary('RDR_POS/Trained/EN.DICT')
    tagList = r.tagRawCorpus(dictionary, text.strip())
    

