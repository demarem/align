from glob import glob
from os import path
import re
import argparse
import os


class Align:
    ''' 
    Converts files containing organism data to files containing locus data.
    Script must be run from within the same directory as where the files are 
    located.
    '''
    def __init__(self, targetFile, fileEnding='.fasta', resultsDir='results'):
        self.loci = {}
        self.targetFile = targetFile
        self.fileEnding = fileEnding
        self.resultsDir = resultsDir

    def buildLoci(self):
        self.parseSingleFile(self.targetFile, 'Target')
        for fasta in glob('*' + self.fileEnding):
            sampleName = path.splitext(fasta)[0]
            fastaFile = open(fasta, 'rU')
            self.parseSingleFile(fastaFile, sampleName)

    def parseSingleFile(self, fastaFile, sampleName):
        locus = None
        for line in fastaFile:
            if '>' in line:
                locus = int(re.search(r'.*\[(.*)\].*', line).group(1))
                line = '>' + sampleName + '\n'
            if locus in self.loci:
                self.loci[locus] += line
            else:
                self.loci[locus] = line

    def buildNewFiles(self):
        if not os.path.exists(self.resultsDir):
            os.makedirs(self.resultsDir)
        else:
            print 'ERROR: Directory already exists'
            exit()

        for locus in self.loci:
            locusPath = self.resultsDir + '/' + str(locus) + self.fileEnding
            locusFile = open(locusPath, 'w')
            locusFile.write(self.loci[locus])
            locusFile.close()

    def run(self):
        self.buildLoci()
        self.buildNewFiles()

def parseArgs():
    parser = argparse.ArgumentParser(\
        description='A Python script for converting organism data to locus data.')
    parser.add_argument('targetFile', metavar='targetFile', type=argparse.FileType('rU'),
                help='input file', nargs=1)

    args = parser.parse_args()
    # debugging argument parsing
    # print args

    return args

def main():
    args = parseArgs()
    align = Align(args.targetFile[0])
    align.run()

if __name__ == '__main__':
    main()
