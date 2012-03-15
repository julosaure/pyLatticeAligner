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
                        s.append('$')
            s.append('\n')
        return string.join(s)

class AlignCell():
    """ A cell lists all SentPos which are aligned together.
    """
    def __init__(self, lSentence_, lAlignedSentences_):
        self.list = []
        self.index = 0
        self.lSentence = lSentence_
        self.lAlignedSentences = lAlignedSentences_

    def __str__(self):
        return str(map(str, self.list))

    def add(self, sentPos):
        bisect.insort_left(self.list, sentPos)
        #if sentPos.sentence not in self.lAlignedSentences:
        #    self.lAlignedSentences.append(sentPos.sentence)
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.index == len(self.list):
            self.index = 0
            raise StopIteration
        self.index += 1
        return self.list[self.index-1]

    def __eq__(self, other):
        assert isinstance(other, Token)
        return self.eqToken(other)

    def eqToken(self, token):
        assert isinstance(token, Token)
        equals = False
        for sentPos in self:
            if sentPos.pos == -1:
                continue
            sentPosTok = self.lSentence[sentPos.sentence][sentPos.pos]
            if sentPosTok == token:
                equals = True
                break
        return equals
    
    def fillDeletedAlignedTokens(self):
        for n in self.lAlignedSentences:
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
