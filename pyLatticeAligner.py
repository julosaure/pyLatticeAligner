#!/usr/bin/python

import fileinput, argparse
import nltk
import sentence, multiAligner, lattice

class PyLatticeAligner():

    def __init__(self):
        self.stemmer = nltk.stem.SnowballStemmer("english")

    def readSentences(self, inputFile, noJunk):
        lSentences = []
        for line in fileinput.input(inputFile):
            line = line.decode('utf8')
            line = line.strip()
            sent = sentence.Sentence(line, self.stemmer)
            print sent
            if noJunk and len(sent)<2:
                continue
            lSentences.append(sent)
        #print lSentences
        return lSentences

    def computeMultiAlign(self, lSentences):
        aligner = multiAligner.MultiAligner(lSentences)
        align, alignstr = aligner.align()
        print alignstr
        f = open("output.csv", "w")
        f.write(alignstr)
        f.close()
        
        return align

    def searchBestPath(self, align):
        lat = lattice.Lattice(align)
        print lat
        print lat.getBestPath()
        print lat.getBestPath(False)

    def main(self, inputFile, noJunk):
        lSentences = self.readSentences(inputFile, noJunk)
        align = self.computeMultiAlign(lSentences)
        self.searchBestPath(align)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Multialign sentences to generate a better one..')
    parser.add_argument("fileName", nargs=1, action="store", help="Name of the file that contains the sentences to align")
    parser.add_argument("-nojunk", dest="noJunk", action="store_true", help="Remove from input junk sentences made on only 1 word")

    args = parser.parse_args()
    print args

    aligner = PyLatticeAligner()
    aligner.main(args.fileName, args.noJunk)
