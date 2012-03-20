#!/usr/bin/python

import math, bisect
from alignment import *
from sentence import Token

class Lattice(list):
    """ A Lattice representing all the possible path in the alignment
    of tokens.
    """
    def __init__(self, align_):
        assert isinstance(align_, Alignment), type(align_)
        self.__convert(align_)
    
    def __str__(self):
        return "".join([str(c) + "\n" for c in self])
        
    def __convert(self, align):
        """ Converts an Alignment to a Lattice by merging identical tokens
        summing their probabilities.
        """
        for distCell in align:
            nbToken = float(len(distCell))
            dicToken = {}
            for sentPos in distCell:
                tok = NullToken()
                if sentPos.pos != -1:
                    tok = distCell.lSentence[sentPos.sentence][sentPos.pos]
                try:
                    dicToken[tok] += 1
                except KeyError:
                    dicToken[tok] = 1
            
            latCell = LatticeCell()
            for token, count in dicToken.iteritems():
                latCell.append(LatticeToken(token, -math.log(count/nbToken)))
            self.append(latCell)

    def getBestPath(self, clean=True):
        """ Returns the best path in the lattice, with or without 
        the null tokens.
        """
        path = []
        for cell in self:
            tok = cell[0].token
            if (not clean) or (clean and not isinstance(tok, NullToken)):
                path.append(str(tok)+" ")
        return ''.join(path)


class LatticeCell(list):
    """ Represents a position in the Lattice, and stores all possible
    Token at this position with their probability.
    """
    def __str__(self):
        return str(map(str, self))

    def append(self, tok):
        assert isinstance(tok, LatticeToken)
        bisect.insort_right(self, tok)

class LatticeToken():
    """ A Token with its associated minus log probability in LatticeCell.
    """
    def __init__(self, token_, minlogprob_):
        assert isinstance(token_, Token)
        self.token = token_
        self.minlogprob = minlogprob_

    def __str__(self):
        return str((str(self.token), self.minlogprob))

    def __cmp__(self, o):
        """Tokens are compared with their minus log probability.
        """
        return cmp(self.minlogprob, o.minlogprob)
