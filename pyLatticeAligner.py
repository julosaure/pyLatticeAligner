#!/usr/bin/python

import fileinput
import sentence, multiAligner

INFILE = "./sentences8.txt"

def readSentences():
    lSentences = []
    for line in fileinput.input(INFILE):
        line = line.strip()
        sent = sentence.Sentence(line)
        print sent
        lSentences.append(sent)
    print lSentences
    return lSentences

def computeMultiAlign(lSentences):
    align = multiAligner.MultiAligner(lSentences)
    align.align()

def reduceMalignToLattice(mAlign):
    pass

def searchBestPath(lattice):
    pass

def main():
    lSentences = readSentences()
    mAlign = computeMultiAlign(lSentences)
    lattice = reduceMalignToLattice(mAlign)
    searchBestPath(lattice)

if __name__ == "__main__":
    main()
