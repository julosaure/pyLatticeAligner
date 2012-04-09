#!/usr/bin/python

from sentence import *
from alignment import *

class SimpleEditDistance:
    """ Standard Edit Distance.
    """
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
    """ POS enhanced edit distance: aligns preferentially tokens
    that share a same POS.
    """
    def ins(self):
        return 2

    def dele(self):
        return 2

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
        
        # we compute equality only once, because it's expensive
        tokensMatch = tok1 == tok2

        if tokensMatch and tok1.tag==tok2.tag and tok1.tag.startswith("NN"):
            # match of Nouns
            score = 0
        elif tokensMatch and tok1.tag==tok2.tag and (tok1.tag.startswith("V") or tok1.tag.startswith("MD")):
            # match of verbs and modals
            score = 0
        elif tokensMatch and tok1.tag==tok2.tag and (tok1.tag.startswith("JJ") or tok1.tag.startswith("RB")):
            # match of adjectives and adverbs
            score = 0
        #elif tok1 == tok2 and tok1.tag==tok2.tag and tok1.tag == ".":
            # match of punctuation marks
            # score = 0
        elif tokensMatch and tok1.tag == tok2.tag:
            # all other mathces
            score = 0
            
        else:
            scoreTagMatch = 1
            scoreSubst = 2
            if isinstance(tok1, Token):
                if isinstance(tok2, Token):
                    # Token / Token
                    if tok1.tag == tok2.tag:
                        score = scoreTagMatch
                    else:
                        score = scoreSubst
                else:
                    # Token / AlignCell
                    if tok1.tag in tok2.tags():
                        score = scoreTagMatch
                    else:
                        score = scoreSubst
            else:
                if isinstance(tok2, Token):
                    # AlignCell / Token
                    if tok2.tag in tok1.tags():
                        score = scoreTagMatch
                    else:
                        score = scoreSubst
                else:
                    # AlignCell / AlignCell
                    score = scoreSubst
                    for t in tok1.tags():
                        if score == scoreTagMatch:
                            break
                        for tt in tok2.tags():
                            if t == tt:
                                score = scoreTagMatch
                                break
                              
        return score
