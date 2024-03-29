#!usr/bin/python

import copy, numpy
from alignment import *
from sentence import * 
from lalign import *
from editDistance import *
from memoization import memo

class MultiAligner:

    def __init__(self, lSentence_, editDist=None):
        self.lSentence = lSentence_
        if editDist is not None:
            self.ed = PosEditDistance()
        else:
            self.ed = SimpleEditDistance()
        
    def align(self):
        sentencesToAlign = copy.copy(self.lSentence)
        
        lNumSentence = LNumSentence(sentencesToAlign)
        lAlign = copy.copy(lNumSentence)

        while len(lAlign) > 1: 
            distMat = self.computeDistanceMatrix(lAlign)
            print distMat
            i1, i2 = self.pickItemsToAlign(distMat, lAlign)
            a2 = lAlign.pop(i2)
            a1 = lAlign.pop(i1)
            #print a1
            #print a2
            align = self.alignItems(a1, a2, sentencesToAlign)
            lAlign.insert(0, align)
        
        align = lAlign[0]
        alignstr =  align.sentAlign()
        return align, alignstr

    def pickItemsToAlign(self, distMat, lAlign):
        """ Finds a pair of Sentence and/or Alignments whose distance is minimal.
        """
        minVal = 999
        minI = 0
        minJ = 0
        for i in xrange(len(lAlign)):
            for j in xrange(i+1, len(lAlign)):
                if distMat[i,j] < minVal:
                    minVal = distMat[i,j]
                    minI = i
                    minJ = j
        return minI, minJ

    def computeDistanceMatrix(self, lAlign):
        """ Computes the distance matrix between all Sentence and Alignments.
        """
        nbSentence = len(lAlign)
        distMat = numpy.zeros((nbSentence, nbSentence), int)
        
        for i in xrange(nbSentence):
            for j in xrange(i+1, nbSentence):
                s1 = lAlign.getSentOrAlignAtPos(i)
                s2 = lAlign.getSentOrAlignAtPos(j)
                #editMat, finalCell = self.computeEditDistance(s1, s2)
                finalCell = self.computeEditDistance(s1, s2)
                distMat[i,j] = finalCell.val
        return distMat


    def alignItems(self, a1, a2, sentencesToAlign):
        """ Aligns 2 items, either Sentence or Alignment.
        """
        if isinstance(a1, tuple) and isinstance(a2, tuple):
            print a1
            print a2
            align = self.alignSentencePair(a1, a2, sentencesToAlign)
        elif isinstance(a1, Alignment) and isinstance(a2, tuple):
            print a1.sentAlign()
            print a2
            align = self.alignSentenceVsAlignment(a1, a2)
        elif isinstance(a1, Alignment) and isinstance(a2, Alignment):
            print a1.sentAlign()
            print a2.sentAlign()
            align = self.alignAlignments(a1, a2)
        else:
            raise Exception("Invalid types: type(a1)="+str(type(a1))+" type(a2)="+str(type(a2)))
        return align

    def alignAlignments(self, a1, a2):
        """Aligns 2 Alignment.
        """
        finalCell = self.computeEditDistance(a1, a2)
        #print editMat

        cell = finalCell
        while cell.i > 0 or cell.j > 0: 
            s = cell.pp() 
            if cell.prev is not None:
                s += " " + cell.prev.pp()
            #print s

            prevPos = max(0, cell.i-1)
            
            if cell.i == cell.prev.i+1:
                pass
                # equality or substitution
                # nothing to do 
            else:
                # insertion
                alignCell = a1.newAlignCell()
                alignCell.fillNonAlignedTokens()
                if cell.i == 0:
                    a1.insert(0, alignCell)
                else:
                    a1.insert(prevPos+1, alignCell)

            if cell.j == cell.prev.j+1:
                prevPos2 = max(0, cell.j-1)
                #prevPos2 = max(0, cell.prev.j)

                if  cell.i == cell.prev.i+1:
                    # equality or substitution 
                    ac2 = a2[prevPos2]
                    for sp in ac2:
                        a1[prevPos].add(sp)
                else:
                    # insertion
                    ac2 = a2[prevPos2]
                    for sp in ac2:
                        if cell.i == 0:
                            a1[0].add(sp)
                        else:
                            a1[prevPos+1].add(sp)
            else:
                # deletion
                for nSent in a2.alignedSentences:
                    a1[prevPos].add(SentPos(nSent, -1))
                
            #print a1.sentAlign(a2.alignedSentences)
            cell = cell.prev
        
        a1.alignedSentences.extend(a2.alignedSentences)
        return a1


    def alignSentenceVsAlignment(self, a1, a2):
        """Aligns an Alignment and a Sentence.
        """
        n2, s2 = a2 #align.lSentence[n2]
        #print s2
        finalCell = self.computeEditDistance(a1, s2)
        #print editMat

        cell = finalCell
        while cell.i > 0 or cell.j > 0: 
            s = cell.pp() 
            if cell.prev is not None:
                s += " " + cell.prev.pp()
            #print s

            prevPos = max(0, cell.i-1)
            
            if cell.i == cell.prev.i+1:
                pass
                # equality or substitution
                # nothing to do 
            else:
                # insertion
                alignCell = a1.newAlignCell()
                alignCell.fillNonAlignedTokens()
                if cell.i == 0:
                    a1.insert(0, alignCell)
                else:
                    a1.insert(prevPos+1, alignCell)

            if cell.j == cell.prev.j+1: 
                prevPos2 = max(0, cell.j-1)
                if  cell.i == cell.prev.i+1:
                    # equality or substitution 
                    a1[prevPos].add(SentPos(n2, prevPos2))
                else:
                    # insertion
                    if cell.i == 0:
                        a1[0].add(SentPos(n2, prevPos2))
                    else:
                        a1[prevPos+1].add(SentPos(n2, prevPos2))
            else:
                # deletion
                a1[prevPos].add(SentPos(n2, -1))
 
            #print a1.sentAlign([n2])
            cell = cell.prev
        a1.alignedSentences.append(n2)
        return a1

        
    def alignSentencePair(self, a1, a2, sentencesToAlign):
        """ Aligns 2 Sentence.
        """
        n1, s1 = a1 #sentencesToAlign[n1]
        n2, s2 = a2 #sentencesToAlign[n2]
        finalCell = self.computeEditDistance(s1, s2)
        #print editMat
        align = Alignment(sentencesToAlign)

        cell = finalCell
        while cell.i > 0 or cell.j > 0: 
            alignCell = align.newAlignCell()
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
                
            # the iteration goes backward, so we insert at pos 0
            align.insert(0, alignCell)
            #print align.sentAlign([n1, n2])
            cell = cell.prev

        align.alignedSentences.extend([n1, n2])
        return align

    @memo
    def computeEditDistance(self, s1, s2):
        """ Compute the edit distance betweem to items, either Sentences or Alignments.
        """
        l1 = len(s1); l2 = len(s2)
        mat = numpy.zeros((l1+1,l2+1), object)
        
        mat[0,0] = DistCell(0, 0, 0, None)
        for i in xrange(1, l1+1): 
            mat[i,0] = DistCell(i, 0, i, mat[i-1,0])
        for j in xrange(1, l2+1):
            mat[0,j] = DistCell(0, j, j, mat[0,j-1])

        for i in xrange(1,l1+1):
            for j in xrange(1,l2+1):
                lPrev = [(mat[i-1,j].val + self.ed.dele(), mat[i-1,j]),
                         (mat[i,j-1].val + self.ed.ins(), mat[i,j-1]),
                         (mat[i-1,j-1].val + self.ed.match(s1[i-1], s2[j-1]), mat[i-1,j-1])]
                prev = reduce(lambda x, y: x if x[0]<=y[0] else y, lPrev, (999,None))
                mat[i,j] = DistCell(i, j, prev[0], prev[1])
                #print i, j, prev[0], prev[1]
        #print mat
        #return mat, mat[l1,l2]
        return mat[l1,l2]
 
class DistCell():
    """ A cell of the edit distance matrix, composed of its positions i and j in the matrix, of its value val, and of a pointer to its predecessor cell (chosen during the dynamic programming step that created this cell).
    """
    def __init__(self, i, j, val, prevDistCell):
        self.i = i
        self.j = j
        self.val = val
        self.prev = prevDistCell

    def __str__(self):
        return str(self.val)

    def pp(self):
        return "DC("+str(self.i)+", "+str(self.j)+", "+str(self.val)+", "+self.prev.coord() if self.prev is not None else "()" +")"

    def coord(self):
        return "("+str(self.i)+", "+str(self.j)+")"
 

    
