#!/usr/bin/python
#
# generic.py
#
# Generates generic questions. We first try to generate generic questions,
# and then we generate the rest of the questions via extraction.
# If the input article does not fall under the following categories, 
# then we don't generate any generic questions.
#
# Eric Gan
#   with
# Aaron Anderson
# Rachel Kobayashi
#
#

import nltk, sys 
import util.nltk_helper as nhelp
import util.rdrpos as rdrpos

GENERIC_LANGUAGE = [
    "Is [TOPIC] a regional Indian Language?",
    "Is [TOPIC] a programming language?",
    "Is [TOPIC] an Italic language?",
    "Is [TOPIC] a West Germanic language?",
    "How did [TOPIC] originate?"
]

GENERIC_PROG_LANGUAGE = [
    "Who was the creator of [TOPIC]?",
    "when was [TOPIC] created?",
    "Is [TOPIC] an object-oriented programming language?"
]

GENERIC_SOCCER = [
    "When was [TOPIC] born?",
    "Where was [TOPIC] born?",
    "Did [TOPIC] ever win an Olympic gold medal?"
]

GENERIC_CONSTELLATION = [
    "Is [TOPIC] in the zodiac?",
    "Where is [TOPIC] located?"
]

GENERIC_MOVIE = [
    "Who directed [TOPIC]?",
    "Who wrote [TOPIC]?",
    "When was [TOPIC] released?"
]

def generateGenericQuestions(content):


