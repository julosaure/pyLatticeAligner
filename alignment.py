#!/usr/bin/python

import string, bisect

class Alignment(list):
    
    def __init__(self):
        pass

    def __str__(self):
        return str(map(str, self.__iter__()))

    def sentAlign(self, lSentence):
        s = []
        for i in xrange(len(lSentence)):
            sent = lSentence[i]
            print sent
            for cell in self:
                for sentPos in cell:
                    if sentPos.sentence == i:
                        if sentPos.pos == -1:
                            s.append('X')
                        else:
                            s.append(str(sent[sentPos.pos]))
                        s.append('\t')
            s.append('\n')
        return string.join(s)

class AlignCell():
    """ A cell lists all SentPos which are aligned together.
    """
    def __init__(self):
        self.list = []
        self.index = 0

    def __str__(self):
        return str(map(str, self.list))#__iter__()))

    def add(self, sentPos):
        bisect.insort_left(self.list, sentPos)
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        if self.index == len(self.list):
            raise StopIteration
        self.index += 1
        return self.list[self.index-1]

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
