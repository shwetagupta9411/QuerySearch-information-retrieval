"""
Runs part 2 of assignment.

python3 quesTwo.py
Args:
    -i inputFileOne.txt
    -o outputFileOne.txt
"""


import os
import sys, getopt
import string, time
from datetime import datetime

# To run the script -
# python3 quesTwo.py -i outputFileOne.txt -o outputFileTwo.txt

class InvertedIndexGenerator(object):
    def __init__(self, writerFlag, iFile, oFile):
        self.iFile = iFile
        self.oFile = oFile
        self.writerFlag = writerFlag
        pass

    def generate(self):
        documents = {}
        try:
            if self.writerFlag == True:
                outFile = open(self.oFile, "w")
                with open(self.iFile) as f:
                    for line in f:
                        try:
                            (key, val) = line.split("\t")
                        except ValueError:
                              continue
                        documents[key.strip()] = val.strip()
            else:
                documents = self.iFile

            keys = documents.keys()
            indexTerms = list(set(' '.join(documents.values()).split()))
            indexTerms.sort()
            if self.writerFlag == True:
                for term in indexTerms:
                    outFile.write(term)
                    for key in keys:
                        if term in documents[key]:
                             outFile.write("\t" + key)
                    outFile.write("\n")
                outFile.close()
            else:
                dataDic = {}
                for term in indexTerms:
                    dataDic[term] = {}
                    for key in keys:
                        dataDic[term][key] = 0
                        if term in documents[key]:
                             dataDic[term][key] = 1
                return dataDic
        except (OSError, IOError) as e:
            print("Wrong input file name or file path", e)



if __name__ == '__main__':
    startTime = datetime.now()
    try:
      opts, _ = getopt.getopt(sys.argv[1:],"i:o:")
      if len(opts) != 2:
          print('Please pass all the parameters: python quesTwo.py -i <inputfile> -o <outputfile>')
          sys.exit()
    except getopt.GetoptError:
      print('usage: -i <inputfile> -o <outputfile>')
      sys.exit()

    for opt, arg in opts:
        if opt == '-i':
            iFile = arg
        if opt == '-o':
            oFile = arg
    start = InvertedIndexGenerator(True, iFile, oFile)
    start.generate()
    # import timeit, functools
    # t = timeit.Timer(functools.partial(generateInvertedIndex, iFile, oFile))
    # print t.timeit(1)
    print(datetime.now() - startTime)
