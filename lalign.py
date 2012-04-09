#!/usr/bin/python

import copy
import sentence
import alignment

class AbsPos:
    def __init__(self, i):
        self.abspos = i

    def __str__(self):
        return str(self.abspos)

    def __eq__(self, other):
        return self.abspos == other.abspos

    def __cmp__(self, other):
        if isinstance(other, AbsPos):
            return cmp(self.abspos, other.abspos)
        #elif isinstance(other, int):
        #    return cmp(self.pos, other)
        else:
            raise Exception("Invalide type, type(other)="+str(type(other)))

    def __index__(self):
        return self.abspos


class AbsSent(tuple):
    def __init__(self, args):
        assert len(args) == 2
        assert isinstance(args[0], AbsPos)
        assert isinstance(args[1], sentence.Sentence)
        tuple.__init__(self, args)

    def __str__(self):
        return str(map(str, self))


class LNumSentence(list):
    def __init__(self, lSentence_):
        lSentence = copy.copy(lSentence_)
        i = 0
        for sent in lSentence:
            p = AbsSent([AbsPos(i), sent])
            self.append(p)
            i += 1

    def popBySentenceNum__(self, num_):
        pos = 0
        for item in self:
            if isinstance(item, PosSent):
                num, sent = item
                if num == num_:
                    self.pop(pos)
                    break
            pos += 1


    def getSentOrAlignAtPos(self, pos):
        item = self[pos]
        if isinstance(item, AbsSent):
            num, sent = item
            return sent
        elif isinstance(item, alignment.Alignment):
            return item
        else:
            raise Exception("Invalid item at position "+str(pos)+" of type "+str(type(item)))
