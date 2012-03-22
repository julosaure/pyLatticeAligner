#!/usr/bin/python

import string, bisect, copy
import sentence 
from lalign import *

class Alignment(list):
    """An alignment is a list of AlignCell where each AlignCell lists
    all the words or indels which are aligned together.
    """
    def __init__(self, lSentence_):
        self.lSentence = copy.copy(lSentence_)
        self.alignedSentences = []

    def __str__(self):
        return str(map(str, self.__iter__()))

    def sentAlign(self):
        s = []
        #print lSentence
        for i in self.alignedSentences:
            sent = self.lSentence[i]
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

    def newAlignCell(self):
        """ AlignCell Factory constructor.
        Use this method for creating a new AlignCell that belongs to this Alignment.
        """
        return AlignCell(self.lSentence, self.alignedSentences)

class AlignCell(list):
    """ A cell is a list of SentPos which are aligned together.
    
    All AlignCell must be created with Alignment.newAlignCell() in order
    to have a proper management of the sentences which are aligned. 
    """
    def __init__(self, lSentence_, alignedSentences_):
        self.lSentence = lSentence_
        self.alignedSentences = alignedSentences_

    def __str__(self):
        return str(map(str, self))

    def pp(self):
        s = []
        for i in self.alignedSentences:
            sent = self.lSentence[i]
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
        assert sentPos.sentence in self.alignedSentences, str(sentPos.sentence)+" "+str(self.alignedSentences)
        assert sentPos.pos < len(self.lSentence[sentPos.sentence]), str(sentPos.pos)+ " " +str(self.lSentence[sentPos.sentence])
        bisect.insort_left(self, sentPos)
        
    def __eq__(self, other):
        #print other
        if isinstance(other, sentence.Token):
            return self.eqToken(other)
        elif isinstance(other, AlignCell):
            return self.eqAlignCell(other)
        else:
            raise Exception("Invalid type, type(other)="+str(type(other)))

    def eqToken(self, token):
        assert isinstance(token, sentence.Token)
        equals = False
        for sentPos in self:
            if sentPos.pos == -1:
                continue
            assert sentPos.sentence.abspos < len(self.lSentence)
            assert sentPos.pos < len(self.lSentence[sentPos.sentence]), str(sentPos.pos) + str(self.lSentence[sentPos.sentence]) 
            sentPosTok = self.lSentence[sentPos.sentence][sentPos.pos]
            if sentPosTok == token:
                equals = True
                break
        #print self.pp() + " / " +str(token)+ " -> " +str(equals)
        return equals
    
    def eqAlignCell(self, other):
        assert isinstance(other, AlignCell)
        equals = False
        breakMainLoop = False
        for sentPos in self:
            if breakMainLoop:
                break
            if sentPos.pos == -1:
                continue
            for sentPosOther in other:
                if sentPosOther.pos == -1:
                    continue
                
                sentPosTok = self.lSentence[sentPos.sentence][sentPos.pos]
                sentPosOtherTok = other.lSentence[sentPosOther.sentence][sentPosOther.pos]
                if sentPosTok == sentPosOtherTok:
                    equals = True
                    breakMainLoop = True
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
        assert isinstance(sentence, AbsPos)
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
