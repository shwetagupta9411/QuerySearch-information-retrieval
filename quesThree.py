"""
Runs part 3 of assignment.

python3 quesThree.py
Args:
    -i inputFileThree.txt
    -o outputFileThree.txt
"""

import os
import sys, getopt
import string, time
import math
from datetime import datetime

# To run the script -
# python3 quesThree.py -i inputFileThree.txt -o outputFileThree.txt

class TfidfCalculator(object):
    def __init__(self, iFile, oFile):
        self.iFile = iFile
        self.oFile = oFile
        pass

    def getTFIDF(self):
        """This function reads the matrix of frequencies of terms and generates the tf-Idf value."""
        outFile = open(self.oFile, "w")
        docData = {} # data in a structure format [key: values]
        maxFreq = {} # Contains maximum frequency of documents
        idf = {}
        n_i = {}
        hFlag = True
        maxflag = True
        outFile.write("\t\t")
        try:
            with open(self.iFile) as f:
                for line in f:
                    if hFlag:
                        try:
                            header = line.strip().split("\t")
                        except ValueError:
                              continue
                        header.sort()
                        hFlag = False
                    else:
                        try:
                            doc = line.strip().split("\t")
                        except ValueError:
                              continue
                        key = doc[0]
                        doc.pop(0)
                        docData[key] = {}
                        docCount = 0
                        for head in range(len(header)):
                            docData[key][header[head]] = int(doc[head])
                            if int(doc[head]) > 0:
                                docCount = docCount + 1
                            if maxflag:
                                maxFreq[header[head]] = doc[head]
                                outFile.write("\t" + header[head])
                            else:
                                if maxFreq[header[head]] < doc[head]:
                                    maxFreq[header[head]] = doc[head]
                        maxflag = False
                        n_i[key] = docCount

            """writes the tf-idf values"""
            outFile.write("\n")
            for term in docData:
                outFile.write(term)
                idf[term] = round(math.log(float(len(header))/float(n_i[term]), 10), 3) # this is the idf values
                for each in header:
                    termFreq = float(docData[term][each])/float(maxFreq[each]) #this is term frequency
                    docData[term][each] = round(termFreq * idf[term], 3) #this is tf-idf values
                    outFile.write("\t" + str(docData[term][each]))
                outFile.write("\n")
            outFile.close()
        except (OSError, IOError) as e:
            print("Wrong input file name or file path", e)

if __name__ == '__main__':
    startTime = datetime.now()
    try:
      opts, _ = getopt.getopt(sys.argv[1:],"i:o:")
      if len(opts) != 2:
          print('Please pass all the parameters: python quesThree.py -i <inputfile> -o <outputfile>')
          sys.exit()
    except getopt.GetoptError:
      print('usage: -i <inputfile> -o <outputfile>')
      sys.exit()

    for opt, arg in opts:
        if opt == '-i':
            iFile = arg
        if opt == '-o':
            oFile = arg
    start = TfidfCalculator(iFile, oFile)
    start.getTFIDF()
    print(datetime.now() - startTime)
