"""
Runs part 3 of assignment.

python3 quesThree.py
Args:
    -i inputFileOne.txt
    -o outputFileOne.txt
"""

import os
import sys, getopt
import string, time
import math
from datetime import datetime

# To run the script -
# python3 quesThree.py -i outputFileTwo.txt -o outputFileThree.txt

class TfidfCalculator(object):
    def __init__(self, iFile, oFile):
        self.iFile = iFile
        self.oFile = oFile
        pass

    def getTFIDF(self):
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

            outFile.write("\n")
            for term in docData:
                outFile.write(term)
                idf[term] = round(math.log(float(len(header))/float(n_i[term]), 10), 3)
                for each in header:
                    termFreq = float(docData[term][each])/float(maxFreq[each])
                    docData[term][each] = round(termFreq * idf[term], 3)
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
    # import timeit, functools
    # t = timeit.Timer(functools.partial(getTFIDF, iFile, oFile))
    # print t.timeit(1)
    print(datetime.now() - startTime)
