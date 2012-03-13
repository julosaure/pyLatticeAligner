#!usr/bin/python

import copy, numpy

class MultiAligner:

    def __init__(self, lSentence_):
        self.lSentence = lSentence_
        self.nbSentence = len(self.lSentence)
        self.dSentence = {}
        for i in xrange(self.nbSentence):
            self.dSentence[i] = self.lSentence[i]
        

    def align(self):
        sentenceToAlign = copy.copy(self.lSentence)
        nbSentence = len(sentenceToAlign)
        
        distMat = numpy.zeros((nbSentence, nbSentence), int)
        distMat = self.computeDistanceMatrix(distMat, sentenceToAlign)
        print distMat

        #while len(sentenceToAlign)>0:
        #    self.alignSentence()
        #    mat = self.computeDistanceMatrix()

    def alignSentence(self):
        pass

    def computeDistanceMatrix(self, mat, sentenceToAlign):
        for i in xrange(len(sentenceToAlign)):
            for j in xrange(i+1, len(sentenceToAlign)):
                if i == j:
                    mat[i,j] = 0
                else:
                    mat[i,j] = self.computeEditDistance(sentenceToAlign[i], sentenceToAlign[j])
        return mat

    def computeEditDistance(self, s1, s2):
        l1 = len(s1); l2 = len(s2)
        mat = numpy.zeros((l1+1,l2+1), object)
        
        for i in xrange(l1+1): 
            mat[i,0] = DistCell(0, FirstDistCell())
        for j in xrange(l2+1):
            mat[0,j] = DistCell(0, FirstDistCell())

        for i in xrange(1,l1+1):
            for j in xrange(1,l2+1):
                lPrev = [(mat[i-1,j].val+1, mat[i-1,j]),
                         (mat[i,j-1].val+1, mat[i,j-1]),
                         (mat[i-1,j-1].val+(0 if s1[i-1]==s2[j-1] else 1), mat[i-1,j-1])]
                prev = reduce(lambda x, y: x if x[0]<=y[0] else y, lPrev, (999,None))
                mat[i,j] = DistCell(prev[0], prev[1])
        print mat
        return mat[l1,l2].val

class FirstDistCell():
    pass

class DistCell():
    def __init__(self,  val, prevDistCell):
        self.val = val
        assert prevDistCell is not None, "prevDistCell is null"
        assert isinstance(prevDistCell, DistCell)==True or isinstance(prevDistCell, FirstDistCell), type(prevDistCell)+" not allowed"
        self.prev = prevDistCell

    def __str__(self):
        return str(self.val)

class Alignment(list):
    
    def __init__(self):
        pass


class Cell(list):
    """ A cell lists all SentPos which are aligned together.
    """
    pass


class SentPos():
    """ A couple representing a Position in a Sentence.
    """
    def __init__(self, sentence, pos):
        self.sentence = sentence
        self.pos = pos

    def __str__(self):
        return (self.sentence, self.pos)
