#!/usr/bin/python
#
# set_defs.py
#
# Class the includes all set defintions 
# Allow defining set of accepted values and quick membership checking
#
# Rachel Kobayashi
#   with
# Aaron Anderson
# Eric Gan
#
#

#uses python sets for speed. 
class Identity():

    def isMonth(self,word):
        calendar = ['january','february','march','april','may','june',
                  'july', 'august','september','october','november','december',
                  'jan','feb','mar','apr','may', 'jun',
                  'jul','aug','sep','sept','oct','nov','dec'];
        months = set(calendar);
        return word.lower() in months;

