#!/usr/bin/python

import fileinput, argparse
import nltk, nltk.data
import sentence, multiAligner, lattice

# default tagger in NLTK 
POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'

class PyLatticeAligner():

    def __init__(self, editDist):
        self.stemmer = nltk.stem.SnowballStemmer("english")
        # default NLTK tokenizer
        self.tokenizer = nltk.TreebankWordTokenizer()
        self.tagger = None
        if editDist is not None:
            self.tagger = nltk.data.load(POS_TAGGER)

    def readSentences(self, inputFile, noJunk):
        lSentences = []
        for line in fileinput.input(inputFile):
            line = line.decode('utf8')
            line = line.strip()
            sent = sentence.Sentence(line, self.stemmer, self.tokenizer, self.tagger if self.tagger is not None else None)
            print sent.pp()
            if noJunk and len(sent)<=noJunk:
                continue
            lSentences.append(sent)
        #print lSentences
        return lSentences

    def computeMultiAlign(self, lSentences):
        aligner = multiAligner.MultiAligner(lSentences, self.tagger)
        align, alignstr = aligner.align()
        print alignstr
        f = open("output.csv", "w")
        f.write(alignstr)
        f.close()
        
        return align

    def searchBestPath(self, align):
        lat = lattice.Lattice(align)
        print lat
        print lat.getBestPath(False)
        print lat.getBestPath()

    def main(self, inputFile, noJunk):
        lSentences = self.readSentences(inputFile, noJunk)
        align = self.computeMultiAlign(lSentences)
        self.searchBestPath(align)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Multialign sentences to generate a better one..')
    parser.add_argument("fileName", nargs=1, action="store", help="Name of the file that contains the sentences to align")
    parser.add_argument("-nojunk", "-nj", dest="noJunk", action="store", type=int, help="Remove from input junk sentences made of less or equal to NOJUNK words")
    parser.add_argument("-edit", "-ed", dest="editDist", action="store", type=int, help="Choose the type of edit distance: standard if not specified, POS-aware if 1")
    args = parser.parse_args()
    print args

    aligner = PyLatticeAligner(args.editDist)
    aligner.main(args.fileName, args.noJunk)
