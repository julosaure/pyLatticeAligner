#!/usr/bin/python

from sentence import *
from alignment import *

class SimpleEditDistance:

    def ins(self):
        return 1

    def dele(self):
        return 1

    def match(self, item1, item2):
        assert isinstance(item1, Token) or isinstance(item1, AlignCell)
        assert isinstance(item2, Token) or isinstance(item2, AlignCell)

        score = 0
        if item1 == item2:
            # match
            score = 0
        else:
            # substitution
            score = 1
        
        return score

class PosEditDistance:

    def ins(self):
        return 3

    def dele(self):
        return 3

    def match(self, item1, item2):
        assert isinstance(item1, Token) or isinstance(item1, AlignCell)
        assert isinstance(item2, Token) or isinstance(item2, AlignCell)

        if isinstance(item1, Token):
            tok1 = item1
        else:
            tok1 = item1.getEqualOther(item2)
            if tok1 is None:
                tok1 = item1

        if isinstance(item2, Token):
            tok2 = item2
        else:
            tok2 = item2.getEqualOther(item1)
            if tok2 is None:
                tok2 = item2

        score = 99
        #if tok1 != tok2:
        #    score = 2
        if tok1 == tok2 and tok1.tag==tok2.tag and tok1.tag.startswith("NN"):
            # match of Nouns
            score = 0
        elif tok1 == tok2 and tok1.tag==tok2.tag and (tok1.tag.startswith("V") or tok1.tag.startswith("MD")):
            # match of verbs and modals
            score = 0
        elif tok1 == tok2 and tok1.tag==tok2.tag and (tok1.tag.startswith("JJ") or tok1.tag.startswith("RB")):
            # match of adjectives and adverbs
            score = 1
        #elif tok1 == tok2 and tok1.tag==tok2.tag and tok1.tag == ".":
            # match of punctuation marks
        #    score = 0
        elif tok1 == tok2 and tok1.tag == tok2.tag:
            #assert tok1.tag == tok2.tag, tok1.pp()+ " " +tok2.pp()
            # all other mathces
            score = 2
        else:
            # substitution
            score = 3
        
        return score
