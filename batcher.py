#!/usr/bin/python

import glob, fileinput, subprocess, sys, argparse, os.path, datetime

MALIGNER = "/Users/julien/workspaces/xp/hcomp12/pyLatticeAligner/pyLatticeAligner.py"


def main(directory, refFile, opts=None):
    
    begin = datetime.datetime.now()
    
    outFile = os.path.join(directory,refFile[:-4] + ".aligned")
    out = open(outFile, "w")

    i= 1
    for refTrad in fileinput.input(directory+"/"+refFile):

        fileName =  refFile[:-4] + str(i) + ".txt"
        fileTrad = os.path.join(directory, fileName)
        print fileTrad
        tmpFile = os.path.join('/tmp/', fileName + ".tmp")
        tmpF = open(tmpFile, "w")

        cmd = [ MALIGNER, fileTrad] 
        if opts is not None:
            cmd.extend(opts)
        print cmd
        subprocess.call(cmd, stdout=tmpF, stderr=subprocess.STDOUT)

        cmd = [ "tail", "-n",  "1", tmpFile]
        malignedTrad = subprocess.check_output(cmd)
        print malignedTrad

        out.write(malignedTrad)

        cmd = ["rm", tmpFile]
        subprocess.call(cmd)
        
        i += 1
        
    out.close()
    print "Total time: "+ str(datetime.datetime.now()-begin)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Launch several multialignments in batch')
    parser.add_argument("dir", nargs=1, action="store", help="Name of the directory to process")
    parser.add_argument("refName", nargs=1, action="store", help="Name of the reference file containing the reference translation, i.e. wiki.ref")
    parser.add_argument("-opts", nargs=argparse.REMAINDER, action="store", help="Options to pass to the multialigner")

    args = parser.parse_args()
    #print args
    
    main(args.dir[0], args.refName[0], args.opts)
