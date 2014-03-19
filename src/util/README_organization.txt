Error 501: Not Yet Implemented
Aaron Anderson
Eric Gan
Rachel Kobayashi
Last updated 3/12/2014 by Rachel


CODE ORGANZATION INTENTIONS
Some general notes about the current methods and guidelines for the code in this project.


Functions / classes / documents relating only to the ASKING aspect of the project have the prefix "ans" before the name of the file:
  ans_q_parser.py

Likewise, those related to the GENERATING questions aspect of the project have the prefix "gen" before the name of the file:
  gen_makeQuestions.py
  gen_sent2q.py

We have talked about moving helper / utility files into a separate folder to declutter the current src folder. As this requires some setup to handle moving between functions I have elected to ask / allow Aaron to help handle this move as he currently did something similar so we can interface with the RDR POS tagger. 
Consider moving:
  article_parser.py
  combinations.py
  nltk_help.py
  qutil.py
  rdrpos.py
  set_defs.py

TODO:
  * develope consistant naming convenstions for files / classes / function; with file and class naming most important as opposed to function naming. 
  * rename qx_parse.py to something consistant with the above methods (qx_parse.py is the question parser, will be worked on more after break)
  * change main.py to fit the parameters for the project (./answer, ./ask)



notes on files:
  * combinations.py - contains class to combine parts of an array based on the original context
    words: from subset, group words that appear together in some sample
    dates: given the location and length of date list, group and replace tag

  * set_defs.py - contains set difinitions, contains class that allows in testing wither a word or in said sets. 
    also includes the findDates function which find dates in the input wordList

  * qutil.py - question utility file, place for small functions that are unrelated to other methods of the project
