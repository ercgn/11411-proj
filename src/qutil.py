#!/usr/bin/python
#
# util.py
#
# Class the contains general utility functions 
# used across all functions
#
# Rachel Kobayashi
#   with
# Aaron Anderson
# Eric Gan
#
#

from collections import deque;
from copy import deepcopy;

# outputs the first n items in queue into a string;
def q2str(queue, n):
    copyQ = deepcopy(queue);
    tags = [];
    if len(queue) >= n:
        for count in range(0,n):
            tag = copyQ.popleft();
            tags.append(tag);
    outStr = " ".join(tags);
    return outStr;
