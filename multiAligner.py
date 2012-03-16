#!usr/bin/python

import copy, numpy
from alignment import *

class MultiAligner:

    def __init__(self, lSentence_):
        self.lSentence = lSentence_
        
    def align(self):
        sentencesToAlign = copy.copy(self.lSentence)
        nbSentence = len(sentencesToAlign)
        
        distMat = numpy.zeros((nbSentence, nbSentence), int)
        distMat = self.computeDistanceMatrix(distMat, sentencesToAlign)
        print distMat

        alignedSentences = []
        n1, n2 = self.pickSentencePair(distMat, sentencesToAlign)
        align = self.alignSentencePair(n1, n2, sentencesToAlign, alignedSentences)
        print align
        print align.sentAlign([n1, n2], sentencesToAlign)
        
        alignedSentences.extend([n1, n2])
        while len(alignedSentences) < len(sentencesToAlign):
            n2 = self.pickMinSentence(distMat, sentencesToAlign, alignedSentences)
            align = self.alignSentenceVsAlignment(align, n2, sentencesToAlign, alignedSentences)
            alignedSentences.append(n2)
            #distMat = self.updateDistanceMatrix(distMat)
        res =  align.sentAlign(alignedSentences, sentencesToAlign)
        print res
        f = open("toto.csv", "w")
        f.write(res)
        f.close()
        
    def pickSentencePair(self, distMat, sentencesToAlign):
        """ Pick the sentence pair with minimal edit distance in distMat.
        """
        minVal = 999
        minI = 0
        minJ = 0
        for i in xrange(len(sentencesToAlign)):
            for j in xrange(i+1, len(sentencesToAlign)):
                if distMat[i,j] < minVal:
                    minVal = distMat[i,j]
                    minI = i
                    minJ = j
        return minI, minJ

    def pickMinSentence(self, distMat, sentencesToAlign, lAlignedSentences):
        """ Pick the sentence with minimal edit distance to previously aligned sentences.
        """
        minVal = 999
        minJ = 0
        for i in lAlignedSentences:
            for j in xrange(len(sentencesToAlign)):
                if j in lAlignedSentences:
                    continue
                if distMat[i,j] < minVal:
                    minVal = distMat[i,j]
                    minJ = j
        return minJ

    def alignSentenceVsAlignment(self, align, n2, sentencesToAlign, alignedSentences):
        s2 = sentencesToAlign[n2]
        print s2
        editMat, finalCell = self.computeEditDistance(align, s2)
        print editMat
                
        cell = finalCell
        while cell.i > 0 or cell.j > 0: 
            #alignCell = align[sell.i-1]
            #print cell.pp()

            if cell.i == cell.prev.i+1:
                pass
                # equality or substitution
                # nothing to do 
            else:
                # insertion
                alignCell = AlignCell(sentencesToAlign, alignedSentences)
                alignCell.fillNonAlignedTokens()
                align.insert(cell.i, alignCell)

            if cell.j == cell.prev.j+1: 
                if  cell.i == cell.prev.i+1:
                    # equality or substitution
                    align[cell.i-1].add(SentPos(n2, cell.j-1))
                else:
                    # insertion
                    align[cell.i].add(SentPos(n2, cell.j-1))
            else:
                # deletion
                align[cell.i-1].add(SentPos(n2, -1))
 
            l =  copy.copy(alignedSentences) ; l.append(n2)    
            #print align.sentAlign(l, sentencesToAlign)
            cell = cell.prev
        return align

        
    def alignSentencePair(self, n1, n2, sentencesToAlign, alignedSentences):
        s1 = sentencesToAlign[n1]
        s2 = sentencesToAlign[n2]
        editMat, finalCell = self.computeEditDistance(s1, s2)
        print editMat
        align = Alignment()
        
        cell = finalCell
        while cell.i > 0 or cell.j > 0: 
            alignCell = AlignCell(sentencesToAlign, alignedSentences)
            #print cell.pp()

            if cell.i == cell.prev.i+1:
                # equality or substitution
                alignCell.add(SentPos(n1, cell.i-1))
            else:
                # deletion
                alignCell.add(SentPos(n1, -1))

            if cell.j == cell.prev.j+1: 
                # equality or substitution
                alignCell.add(SentPos(n2, cell.j-1))
            else:
                # insertion
                alignCell.add(SentPos(n2, -1))

            
            align.insert(0, alignCell)
            #print align
            cell = cell.prev
        return align

    def updateDistanceMatrix(self, distMat):
        pass

    def computeDistanceMatrix(self, mat, sentenceToAlign):
        for i in xrange(len(sentenceToAlign)):
            for j in xrange(i+1, len(sentenceToAlign)):
                editMat, finalCell = self.computeEditDistance(sentenceToAlign[i], sentenceToAlign[j])
                mat[i,j] = finalCell.val
        return mat

    def computeEditDistance(self, s1, s2):
        l1 = len(s1); l2 = len(s2)
        mat = numpy.zeros((l1+1,l2+1), object)
        
        mat[0,0] = DistCell(0, 0, 0, None)
        for i in xrange(1, l1+1): 
            mat[i,0] = DistCell(i, 0, i, mat[i-1,0])
        for j in xrange(1, l2+1):
            mat[0,j] = DistCell(0, j, j, mat[0,j-1])

        for i in xrange(1,l1+1):
            for j in xrange(1,l2+1):
                lPrev = [(mat[i-1,j].val+1, mat[i-1,j]),
                         (mat[i,j-1].val+1, mat[i,j-1]),
                         (mat[i-1,j-1].val+(0 if s1[i-1]==s2[j-1] else 1), mat[i-1,j-1])]
                prev = reduce(lambda x, y: x if x[0]<=y[0] else y, lPrev, (999,None))
                mat[i,j] = DistCell(i, j, prev[0], prev[1])
                #print i, j, prev[0], prev[1]
        #print mat
        return mat, mat[l1,l2]

 
class DistCell():
    def __init__(self, i, j, val, prevDistCell):
        self.i = i
        self.j = j
        self.val = val
        #assert prevDistCell is not None , "prevDistCell is null"
        #assert isinstance(prevDistCell, DistCell)==True or isinstance(prevDistCell, FirstDistCell), type(prevDistCell)+" not allowed"
        self.prev = prevDistCell

    def __str__(self):
        return str(self.val)

    def pp(self):
        return "DC("+str(self.i)+", "+str(self.j)+", "+str(self.val)+", "+self.prev.coord()+")"

    def coord(self):
        return "("+str(self.i)+", "+str(self.j)+")"
 

    
