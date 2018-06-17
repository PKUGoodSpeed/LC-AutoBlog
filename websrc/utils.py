"""
Useful functions
@author: pkugoodspeed
@date: 06/12/2018
@copyright: jogchat.com
"""
import sqlite3
from termcolor import colored
from sys import stdout

def ColorMessage(msg, color, printout=True):
    msg = colored(msg, color)
    if printout:
        print(msg)
    return msg


def getHtmlElement(tag='p', msg="undefined", selfclose=False, **kwargs):
    """
    Creating an HTML element
    return <tag args>msg</tag>
    """
    element = "<" + tag
    for key, val in kwargs.items():
        element += " " + key + "=" + val
    element += ">"
    if selfclose:
        return element
    element += "{M}</{T}>".format(M=msg, T=tag)
    return element


class ProgressBar:
    '''
    Here I implement a progress bar program by myself.
    '''
    _bar = 50
    _blk = 0
    _n = 0
    def __init__(self):
        pass
        
    def setBar(self, num_iteration, bar_size = 50, bracket = '[]'):
        assert len(bracket) == 2
        self._blk = (num_iteration + bar_size - 1)/bar_size
        self._bar = num_iteration/self._blk
        self._n = num_iteration
        stdout.write("{1}{0}{2}".format(' '*int(self._bar), bracket[0], bracket[1]))
        stdout.flush()
        stdout.write("\b" * int(self._bar + 1))
        
    def show(self, i):
        if((i+1) % self._blk == 0):
            stdout.write("=")
            stdout.flush()
        if(i+1 == self._n):
            stdout.write('\n')