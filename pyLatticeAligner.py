#!/usr/bin/python

import fileinput
import nltk
import sentence, multiAligner, lattice

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
        aligner = multiAligner.MultiAligner(lSentences)
        align = aligner.align()
        return align

    def searchBestPath(self, align):
        lat = lattice.Lattice(align)
        print lat
        print lat.getBestPath()
        print lat.getBestPath(False)

    def main(self):
        lSentences = self.readSentences()
        align = self.computeMultiAlign(lSentences)
        self.searchBestPath(align)

if __name__ == "__main__":
    aligner = PyLatticeAligner()
    aligner.main()
