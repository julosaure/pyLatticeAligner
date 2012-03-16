#!/usr/bin/python

import fileinput
import nltk
import sentence, multiAligner

INFILE = "./data/sentences10.txt"

class PyLatticeAligner():

    def __init__(self):
        self.stemmer = nltk.stem.SnowballStemmer("english")

    def readSentences(self):
        lSentences = []
        for line in fileinput.input(INFILE):
            line = line.strip()
            sent = sentence.Sentence(line, self.stemmer)
            print sent
            lSentences.append(sent)
        #print lSentences
        return lSentences

    def computeMultiAlign(self, lSentences):
        align = multiAligner.MultiAligner(lSentences)
        align.align()

    def reduceMalignToLattice(self, mAlign):
            pass

    def searchBestPath(self, lattice):
        pass

    def main(self):
        lSentences = self.readSentences()
        mAlign = self.computeMultiAlign(lSentences)
        lattice = self.reduceMalignToLattice(mAlign)
        self.searchBestPath(lattice)

if __name__ == "__main__":
    aligner = PyLatticeAligner()
    aligner.main()
