"""
Runs part 4 of assignment.

python3 quesThree.py
Args:
    --input inputFileOne.txt
    --docOne D1
    --docTwo D2
"""

import os
import sys, getopt
import string, math

# To run the script -
# python3 quesFour.py --input outputFileThree.txt --docOne D1 --docTwo D2

class CosineCalculator(object):
    def __init__(self, iFile, docOne, docTwo):
        self.iFile = iFile
        self.docOne = docOne
        self.docTwo = docTwo
        pass

    def getCosine(self):
        # cosineSimilarity = d1.d2/|d1|*|d2|
        self.docOne = docOne.upper()
        self.docTwo = docTwo.upper()
        docData = {} # data in a structure format [key: values]
        try:
            with open(self.iFile) as f:
                hFlag = True
                for line in f:
                    if hFlag:
                        try:
                            header = line.strip().split("\t")
                        except ValueError:
                              continue
                        hFlag = False
                    else:
                        try:
                            doc = line.strip().split("\t")
                        except ValueError:
                              continue
                        key = doc[0]
                        doc.pop(0)
                        docData[key] = {}
                        for head in range(len(header)):
                            docData[key][header[head]] = doc[head]

            dotResultDocOne = self.dotProduct(self.docOne, self.docOne, docData)
            lengthDocOne = round(math.sqrt(dotResultDocOne), 3)
            dotResultDocTwo = self.dotProduct(self.docTwo, self.docTwo, docData)
            lengthDocTwo = round(math.sqrt(dotResultDocTwo), 3)
            lenProd = round((lengthDocOne * lengthDocTwo), 3)
            documentsDotRes = self.dotProduct(self.docOne, self.docTwo, docData)
            cosineSimilarity = round((documentsDotRes/lenProd),3)
            print("Cosine Similarity between " + self.docOne + " and " + self.docTwo + ": " + str(cosineSimilarity))
            return cosineSimilarity
        except (OSError, IOError) as e:
            print("Wrong input file name or file path", e)

    def dotProduct(self, docOne, docTwo, docData):
        termKey = docData.keys()
        listOne = []
        listTwo = []

        for key in termKey:
            listOne.append(round(float(docData[key][docOne]), 3))
        if docOne == docTwo:
            listTwo = listOne
        else:
            for key in termKey:
                listTwo.append(round(float(docData[key][docTwo]), 3))

        c = [round(a*b, 3) for a,b in zip(listOne, listTwo)]
        return sum(c)



if __name__ == '__main__':
    try:
      opts, _ = getopt.getopt(sys.argv[1:],"i:d:f", ["input=", "docOne=", "docTwo="])
      if len(opts) != 3:
          print('Please pass all the parameters: python quesFour.py --input <inputfile> --docOne <document one> --docTwo <document two>')
          sys.exit()
    except getopt.GetoptError:
      print('usage: --input <inputfile> --docOne <document one> --docTwo <document two>')
      sys.exit()

    for opt, arg in opts:
        if opt in ("-i", "--input"):
            iFile = arg
        if opt in ("-d", "--docOne"):
            docOne = arg
        if opt in ("-f", "--docTwo"):
            docTwo = arg
    start = CosineCalculator(iFile, docOne, docTwo)
    start.getCosine()
