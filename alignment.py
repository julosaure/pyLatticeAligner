#!/usr/bin/python

import string, bisect
from sentence import *

class Alignment(list):
    """An alignment is a list of AlignCell where each AlignCell lists
    all the words or indels which are aligned together.
    """
    def __str__(self):
        return str(map(str, self.__iter__()))

    def sentAlign(self, lSentence, sentencesToAlign):
        s = []
        #print lSentence
        for i in lSentence:
            sent = sentencesToAlign[i]
            #print sent
            for cell in self:
                for sentPos in cell:
                    if sentPos.sentence == i:
                        if sentPos.pos == -1:
                            s.append('X')
                        else:
                            s.append(str(sent[sentPos.pos]))
                        s.append(',')
            s.append('\n')
        return string.join(s)

class AlignCell(list):
    """ A cell is a list of SentPos which are aligned together.
    """
    def __init__(self, sentencesToAlign_, alignedSentences_):
        self.sentencesToAlign = sentencesToAlign_
        self.alignedSentences = alignedSentences_

    def __str__(self):
        return str(map(str, self))

    def pp(self):
        s = []
        for i in self.alignedSentences:
            sent = self.sentencesToAlign[i]
            for sentPos in self:
                if sentPos.sentence == i:
                    if sentPos.pos == -1:
                        s.append('X')
                    else:
                        s.append(str(sent[sentPos.pos]))
                    s.append(',')
            #s.append('\n')
        return string.join(s)


    def add(self, sentPos):
        bisect.insort_left(self, sentPos)
        
    def __eq__(self, other):
        assert isinstance(other, Token)
        return self.eqToken(other)

    def eqToken(self, token):
        assert isinstance(token, Token)
        equals = False
        for sentPos in self:
            if sentPos.pos == -1:
                continue
            sentPosTok = self.sentencesToAlign[sentPos.sentence][sentPos.pos]
            if sentPosTok == token:
                equals = True
                break
        #print self.pp() + " / " +str(token)+ " -> " +str(equals)
        return equals
    
    def fillNonAlignedTokens(self):
        for n in self.alignedSentences:
            self.add(SentPos(n, -1))

class SentPos():
    """ A couple representing a Position in a Sentence.
    """
    def __init__(self, sentence, pos):
        self.sentence = sentence
        self.pos = pos

    def __str__(self):
        return str((self.sentence, self.pos))

    def __cmp__(self, other):
        """Order 2 SentPos according to their sentence number, then pos number.
        """
        comp = self.sentence.__cmp__(other.sentence)
        if comp == 0:
            comp = self.pos.__cmp__(other.pos)
        return comp 
