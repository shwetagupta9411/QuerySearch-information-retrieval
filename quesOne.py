"""
Runs part 1 of assignment.

python3 quesOne.py
Args:
    -i inputFileOne.txt
    -o outputFileOne.txt
    -s stopwordList.txt
"""

import os
import sys, getopt
import string, time
from porterStemmer import PorterStemmer
from datetime import datetime


# To run the script - stream
# python3 quesOne.py -i inputFileOne.txt -o outputFileOne.txt -s stopwordList.txt


class PreProcessing(object):
    def __init__(self, writerFlag, iFile, oFile, stopwordFile):
        self.iFile = iFile
        self.oFile = oFile
        self.stopwordFile = stopwordFile
        self.writerFlag = writerFlag
        pass
    def process(self):
        """
        This function reads the text file and performs-
            -punctuation
            -tokenization
            -lower-casing/upper-casing / punctuation / numbers
            -stop word
            -stemming
        """
        try:
            stopWords = open(self.stopwordFile, "r").read()
            try:
                if self.writerFlag  == True:
                    outFile = open(self.oFile, "w")
                stemmer = PorterStemmer()
                dataDic = {}
                translator = str.maketrans('', '', string.punctuation)
                nTranslator = str.maketrans('', '', "0123456789")
                with open(self.iFile) as f:
                    for line in f:
                        try:
                            (key, val) = line.split("\t")
                        except ValueError:
                              continue
                        stringToWrite = ""
                        val = val.translate(translator)
                        val = val.translate(nTranslator)
                        val = val.lower().strip().split(" ")
                        if self.writerFlag  == True:
                            stringToWrite = "%s %s \t" % (stringToWrite, key.upper())

                        for words in val:
                            if words.strip() not in stopWords:
                                stringToWrite = "%s %s" % (stringToWrite, stemmer.stem(words))

                        stringToWrite = "%s \n" % (stringToWrite)
                        if self.writerFlag  == False:
                            dataDic[key.strip()] = stringToWrite.strip()
                        else:
                            outFile.write(stringToWrite)
                if self.writerFlag  == True:
                    outFile.close()
                else:
                    return dataDic
            except (OSError, IOError) as e:
                print("Wrong input file name or file path", e)
        except (OSError, IOError) as e:
            print("Wrong stopwords file name or file path", e)



if __name__ == '__main__':
    startTime = datetime.now()
    try:
      opts, _ = getopt.getopt(sys.argv[1:],"i:o:s:")
      if len(opts) != 3:
          print('Please pass all the parameters: python quesOne.py -i <inputfile> -o <outputfile> -s <stopwordfile>')
          sys.exit()
    except getopt.GetoptError:
      print('usage: -i <inputfile> -o <outputfile> -s <stopwordlist>')
      sys.exit()

    for opt, arg in opts:
        if opt == '-i':
            iFile = arg
        if opt == '-o':
            oFile = arg
        if opt == '-s':
            stopwordFile = arg
    start = PreProcessing(True, iFile, oFile, stopwordFile)
    start.process()
    print(datetime.now() - startTime)
