#!usr/bin/python

import copy, numpy
from alignment import *
from sentence import * 
from lalign import *

class MultiAligner:

    def __init__(self, lSentence_):
        self.lSentence = lSentence_
        
    def align(self):
        sentencesToAlign = copy.copy(self.lSentence)
        
        lNumSentence = LNumSentence(sentencesToAlign)
        lAlign = copy.copy(lNumSentence)

        a="""distMat = self.computeDistanceMatrix(sentencesToAlign)
        print distMat

        n1, n2 = self.pickSentencePair(distMat, sentencesToAlign)
        align = self.alignSentencePair(n1, n2, sentencesToAlign)
        print align
        print align.sentAlign()

        lAlign.popNum(n2)
        lAlign.popNum(n1)
        lAlign.insert(0, align)
        """
        #while len(align.alignedSentences) < len(sentencesToAlign):
        while len(lAlign) > 1: 
            #n2 = self.pickMinSentence(distMat, align.lSentence, align.alignedSentences)
            #align = self.alignSentenceVsAlignment(align, n2)
            distMat = self.computeDistanceMatrix2(lAlign)
            print distMat
            i1, i2 = self.pickItemsToAlign(distMat, lAlign)
            a2 = lAlign.pop(i2)
            a1 = lAlign.pop(i1)
            #print a1
            #print a2
            align = self.alignItems(a1, a2, sentencesToAlign)
            lAlign.insert(0, align)
            #distMat = self.updateDistanceMatrix(distMat)
        
        align = lAlign[0]
        alignstr =  align.sentAlign()
        return align, alignstr

    def pickItemsToAlign(self, distMat, lAlign):
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

    def computeDistanceMatrix2(self, lAlign):
        nbSentence = len(lAlign)
        distMat = numpy.zeros((nbSentence, nbSentence), int)
        
        for i in xrange(nbSentence):
            for j in xrange(i+1, nbSentence):
                s1 = lAlign.getSentOrAlignAtPos(i)
                s2 = lAlign.getSentOrAlignAtPos(j)
                editMat, finalCell = self.computeEditDistance(s1, s2)
                distMat[i,j] = finalCell.val
        return distMat


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

    def alignItems(self, a1, a2, sentencesToAlign):
        if isinstance(a1, tuple) and isinstance(a2, tuple):
            print a1
            print a2
            align = self.alignSentencePair(a1, a2, sentencesToAlign)
        elif isinstance(a1, Alignment) and isinstance(a2, tuple):
            #print a1.sentAlign()
            print a2
            align = self.alignSentenceVsAlignment(a1, a2)
        elif isinstance(a1, Alignment) and isinstance(a2, Alignment):
            #print a1.sentAlign()
            #print a2.sentAlign()
            align = self.alignAlignments(a1, a2)
        else:
            raise Exception("Invalid types: type(a1)="+str(type(a1))+" type(a2)="+str(type(a2)))
        return align

    def alignAlignments(self, a1, a2):
        #s2 = align.lSentence[n2]
        #print s2
        editMat, finalCell = self.computeEditDistance(a1, a2)
        #print editMat
        a1.alignedSentences.extend(a2.alignedSentences)

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
                alignCell = a1.newAlignCell()
                alignCell.fillNonAlignedTokens()
                a1.insert(cell.i, alignCell)

            if cell.j == cell.prev.j+1: 
                if  cell.i == cell.prev.i+1:
                    # equality or substitution
                    ac2 = a2[cell.j-1]
                    for sp in ac2:
                        a1[cell.i-1].add(sp)
                    #for nSent in a2.alignedSentences:
                    #    a1[cell.i-1].add(SentPos(nSent, cell.j-1))
                else:
                    # insertion
                    ac2 = a2[cell.j-1]
                    for sp in ac2:
                        a1[cell.i].add(sp)
                    #for nSent in a2.alignedSentences:
                    #    a1[cell.i].add(SentPos(nSent, cell.j-1))
            else:
                # deletion
                for nSent in a2.alignedSentences:
                    a1[cell.i-1].add(SentPos(nSent, -1))
                
            #l =  copy.copy(alignedSentences) ; l.append(n2)    
            #print align.sentAlign(l, sentencesToAlign)
            cell = cell.prev
        
        return a1


    def alignSentenceVsAlignment(self, a1, a2):
        n2, s2 = a2 #align.lSentence[n2]
        #print s2
        editMat, finalCell = self.computeEditDistance(a1, s2)
        #print editMat
        a1.alignedSentences.append(n2)

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
                alignCell = a1.newAlignCell()
                alignCell.fillNonAlignedTokens()
                a1.insert(cell.i, alignCell)

            if cell.j == cell.prev.j+1: 
                if  cell.i == cell.prev.i+1:
                    # equality or substitution
                    a1[cell.i-1].add(SentPos(n2, cell.j-1))
                else:
                    # insertion
                    a1[cell.i].add(SentPos(n2, cell.j-1))
            else:
                # deletion
                a1[cell.i-1].add(SentPos(n2, -1))
 
            #l =  copy.copy(alignedSentences) ; l.append(n2)    
            #print align.sentAlign(l, sentencesToAlign)
            cell = cell.prev
        
        return a1

        
    def alignSentencePair(self, a1, a2, sentencesToAlign):
        n1, s1 = a1 #sentencesToAlign[n1]
        n2, s2 = a2 #sentencesToAlign[n2]
        editMat, finalCell = self.computeEditDistance(s1, s2)
        #print editMat
        align = Alignment(sentencesToAlign)
        align.alignedSentences.extend([n1, n2])

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
            
            align.insert(0, alignCell)
            #print align
            cell = cell.prev
        
        return align

    def computeDistanceMatrix(self, sentenceToAlign):
        nbSentence = len(sentenceToAlign)
        distMat = numpy.zeros((nbSentence, nbSentence), int)
        
        for i in xrange(len(sentenceToAlign)):
            for j in xrange(i+1, len(sentenceToAlign)):
                editMat, finalCell = self.computeEditDistance(sentenceToAlign[i], sentenceToAlign[j])
                distMat[i,j] = finalCell.val
        return distMat

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
        self.prev = prevDistCell

    def __str__(self):
        return str(self.val)

    def pp(self):
        return "DC("+str(self.i)+", "+str(self.j)+", "+str(self.val)+", "+self.prev.coord()+")"

    def coord(self):
        return "("+str(self.i)+", "+str(self.j)+")"
 

    
