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

    def sentAlign(self, tempSentences=[]):
        """ Allows to visualize an Alignment.
        tempSentences allows to visualize an Alignment during the decoding/alignment of the
        current Alignment with a new sentence or Alignment: add the sentence(s) of this new
        item in input into tempSentences.
        """
        s = []
        #print lSentence
        temp = copy.copy(self.alignedSentences)
        temp.extend(tempSentences)
        for i in temp:
            sent = self.lSentence[i]
            #print sent
            for cell in self:
                s.append('(')
                for sentPos in cell:
                    if sentPos.sentence == i:
                        if sentPos.pos == -1:
                            s.append('X')
                        else:
                            s.append(str(sent[sentPos.pos]))
                        s.append(',')
                s.pop()
                s.append(')')
            s.append('\n')
        return ''.join(s)

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
                count = 0
                if sentPos.sentence == i:
                    if sentPos.pos == -1:
                        s.append('X')
                    else:
                        s.append(str(sent[sentPos.pos]))
                    s.append(',')
                    count += 1
                    if count > 1:
                        print "Sentence "+str(i)+": "+sent
                        print string.join(s)
                        raise Exception("ALERT: Several positions for sentence "+str(i)+" in the same AlignCell. This should not be possible. There is probably an error during the decoding of alignments.")
            #s.append('\n')
        return string.join(s)


    def add(self, sentPos):
        assert sentPos.sentence not in self.alignedSentences, str(sentPos.sentence)+" "+str([str(a) for a in self.alignedSentences])
        #assert sentPos.pos < len(self.lSentence[sentPos.sentence]), str(sentPos.pos)+ " " +str(self.lSentence[sentPos.sentence])
        bisect.insort_left(self, sentPos)

    def addEmpty(self, sentPos):
        assert sentPos.sentence in self.alignedSentences, str(sentPos.sentence)+" "+str([str(a) for a in self.alignedSentences])
        bisect.insort_left(self, sentPos)

    def fillNonAlignedTokens(self):
        for n in self.alignedSentences:
            self.addEmpty(SentPos(n, -1))

    def tags(self):
        """ Retrieve the list of the tags of the tokens in this AlignCell.
        """
        lTags = []
        for sp in self:
            token = self.lSentence[sp.sentence][sp.pos]
            lTags.append(token.tag)
        return lTags

    def __eq__(self, other):
        if isinstance(other, sentence.Token):
            if self.getSelfTokenEqualsOtherToken(other) is not None:
                return True
            else:
                return False
        elif isinstance(other, AlignCell):
            if self.getSelfTokenEqualsOtherAlignCell(other) is not None:
                return True
            else:
                return False
        else:
            raise Exception("Invalid type, type(other)="+str(type(other)))

    def getEqualOther(self, other):
        """ Retrieve the Token in this AlignCell which equals the other token or a token in other.
        """
        if isinstance(other, sentence.Token):
            return self.getSelfTokenEqualsOtherToken(other) 
        elif isinstance(other, AlignCell):
            return self.getSelfTokenEqualsOtherAlignCell(other) 
        else:
            raise Exception("Invalid type, type(other)="+str(type(other)))


    def getSelfTokenEqualsOtherToken(self, token):
        """ Retrieve the Token in this AlignCell which equals the token in input.
        """
        assert isinstance(token, sentence.Token)
        equalToken = None
        for sentPos in self:
            if sentPos.pos == -1:
                continue
            assert sentPos.sentence.abspos < len(self.lSentence)
            assert sentPos.pos < len(self.lSentence[sentPos.sentence]), str(sentPos.pos) + str(self.lSentence[sentPos.sentence]) 
            sentPosTok = self.lSentence[sentPos.sentence][sentPos.pos]
            if sentPosTok == token:
                equalToken = sentPosTok
                break
        #print self.pp() + " / " +str(token)+ " -> " +str(equals)
        return equalToken
    
    def getSelfTokenEqualsOtherAlignCell(self, other):
        """ Retrieve the Token in this AlignCell which equals a token in the AlignCell in input.
        """
        assert isinstance(other, AlignCell)
        equalToken = None
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
                    equalToken = sentPosTok
                    breakMainLoop = True
                    break
        #print self.pp() + " / " +str(token)+ " -> " +str(equals)
        return equalToken

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
