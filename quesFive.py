"""
Runs part 5 of assignment.
*Query should be in double quotes*

python3 quesFive.py
Args:
    -i inputFileOne.txt
    -s stopwordfile.txt
    -q "breakthrough AND material"

"""

import os
import sys, getopt
import string, time
from datetime import datetime
from quesOne import PreProcessing
from quesTwo import InvertedIndexGenerator
from porterStemmer import PorterStemmer

# To run the script -
# python3 quesFive.py -i inputFileOne.txt -s stopwordList.txt -q "material OR {new BUT NOT research} AND barrier"

class Search(object):
    def __init__(self, iFile, query, stopwordFile):
        self.iFile = iFile
        self.query = query
        self.stopwordFile = stopwordFile

    def parenthetic_contents(self, string):
        """Generate parenthesized contents in string as pairs (level, contents)."""
        stack = []
        for i, c in enumerate(string):
            if c == '{' or c == '(':
                stack.append(i)
            elif (c == '}'or c == ')') and stack:
                start = stack.pop()
                yield (len(stack), string[start + 1: i])


    def querySearcher(self):
        """This is the main function which performs the AND, OR, AND NOT, BUT NOT and OR NOT operations"""
        try:
            stemmer = PorterStemmer()
            preProcess = PreProcessing(False, self.iFile, "", self.stopwordFile)
            preProcessRes = preProcess.process()
            createIndex = InvertedIndexGenerator(False, preProcessRes, "")
            mainIndex = createIndex.generate()
            originalquery = self.query
            self.query = self.query.lower()
            self.query = self.query.replace('but', 'and')
            querySep =  list(self.parenthetic_contents(self.query))
            res = self.queryCalculator(querySep, mainIndex, stemmer, preProcessRes)
            tempQuery = self.query
            tempQuery = tempQuery.replace('{', '')
            tempQuery = tempQuery.replace('}', '')
            tempQuery = tempQuery.replace('(', '')
            tempQuery = tempQuery.replace(')', '')
            tempQuery = tempQuery.replace('/', '')
            mapKey = {}

            quryStem = []
            for t in tempQuery.split(" "):
                quryStem.append(stemmer.stem(t))
            tempQuery = ' '.join(quryStem)

            for i, r in enumerate(res.keys()):
                mapKey["%d_%s" % (i, "firstItr")] = r
                tempQuery = tempQuery.replace(r, "%d_%s" % (i, "firstItr"))
            res = {**res, **mainIndex}
            andPro = tempQuery.split(" ")

            """AND operation"""
            for index, term in enumerate(andPro):
                if term == "and":
                    if andPro[index+1] == "not":
                        continue
                    else:
                        if mapKey.get(andPro[index-1], -1) == -1:
                            tempKeyFirst = andPro[index-1]
                        else:
                            tempKeyFirst = mapKey[andPro[index-1]]

                        if mapKey.get(andPro[index+1], -1) == -1:
                            tempKeySecond = andPro[index+1]
                        else:
                            tempKeySecond = mapKey[andPro[index+1]]

                        res["%s and %s" % (andPro[index-1], andPro[index+1])] = {}
                        for k in res[tempKeyFirst].keys():
                            res["%s and %s" % (andPro[index-1], andPro[index+1])][k] = res[tempKeyFirst][k] and res[tempKeySecond][k]
                        tempQuery = tempQuery.replace("%s and %s" % (andPro[index-1], andPro[index+1]), "%d_%s" % (index, "secondItr"))
                        mapKey["%d_%s" % (index, "secondItr")] = "%s and %s" % (andPro[index-1], andPro[index+1])

            """OR operation"""
            orPro = tempQuery.split(" ")
            for index, term in enumerate(orPro):
                if term == "or":
                    if orPro[index+1] == "not":
                        continue
                    else:
                        if mapKey.get(orPro[index-1], -1) == -1:
                            tempKeyFirst = orPro[index-1]
                        else:
                            tempKeyFirst = mapKey[orPro[index-1]]

                        if mapKey.get(orPro[index+1], -1) == -1:
                            tempKeySecond = orPro[index+1]
                        else:
                            tempKeySecond = mapKey[orPro[index+1]]

                        res["%s or %s" % (orPro[index-1], orPro[index+1])] = {}
                        for k in res[tempKeyFirst].keys():
                            res["%s or %s" % (orPro[index-1], orPro[index+1])][k] = res[tempKeyFirst][k] or res[tempKeySecond][k]
                        tempQuery = tempQuery.replace("%s or %s" % (orPro[index-1], orPro[index+1]), "%d_%s" % (index, "thirdItr"))
                        mapKey["%d_%s" % (index, "thirdItr")] = "%s or %s" % (orPro[index-1], orPro[index+1])

            """AND NOT, OR NOT, BUT NOT operations"""
            notPro = tempQuery.split(" ")
            for index, term in enumerate(notPro):
                if term == "not":
                    tempKeyNot = {}
                    if mapKey.get(notPro[index+1], -1) == -1:
                        tempKeySecond = notPro[index+1]
                    else:
                        tempKeySecond = mapKey[notPro[index+1]]

                    for k in res[tempKeySecond].keys():
                        if not res[tempKeySecond][k] == True:
                            tempKeyNot[k] = 1
                        else:
                            tempKeyNot[k] = 0

            for index, term in enumerate(notPro):
                if term == "and":
                    if mapKey.get(notPro[index-1], -1) == -1:
                        tempKeyFirst = notPro[index-1]
                    else:
                        tempKeyFirst = mapKey[notPro[index-1]]

                    res["%s and not %s" % (notPro[index-1], notPro[index+2])] = {}
                    for kee in res[tempKeyFirst].keys():
                        res["%s and not %s" % (notPro[index-1], notPro[index+2])][kee] = res[tempKeyFirst][kee] and tempKeyNot[kee]
                        tempQuery = tempQuery.replace("%s and not %s" % (notPro[index-1], notPro[index+2]), "%d_%s" % (index, "fourthItr"))
                        mapKey["%d_%s" % (index, "fourthItr")] = "%s and not %s" % (notPro[index-1], notPro[index+2])

                if term == "or":
                    if mapKey.get(notPro[index-1], -1) == -1:
                        tempKeyFirst = notPro[index-1]
                    else:
                        tempKeyFirst = mapKey[notPro[index-1]]

                    res["%s or not %s" % (notPro[index-1], notPro[index+2])] = {}
                    for kee in res[tempKeyFirst].keys():
                        res["%s or not %s" % (notPro[index-1], notPro[index+2])][kee] = res[tempKeyFirst][kee] or tempKeyNot[kee]
                        tempQuery = tempQuery.replace("%s or not %s" % (notPro[index-1], notPro[index+2]), "%d_%s" % (index, "fourthItr"))
                        mapKey["%d_%s" % (index, "fourthItr")] = "%s or not %s" % (notPro[index-1], notPro[index+2])


            self.queryAnswer(originalquery, tempQuery, mapKey, res)
        except:
            print('The term is not present in the Documents')


    def calCulateWithin(self, preProcessRes, que, stemmer, parentheticResult):
        """Resolves the proximity clause"""
        try:

            withinQ = que.split(" ")
            firstTerm = stemmer.stem(withinQ[0])
            rangee = int(withinQ[1].replace("/", "")) + 1
            secondTerm = stemmer.stem(withinQ[2])
            parentheticResult["%s %d %s" % (firstTerm, rangee-1, secondTerm)] = {}

            for doc in preProcessRes.keys():
                firstTermIndex = 0
                secondTermIndex = 0
                docVal = preProcessRes[doc].split(" ")
                docVal = list(dict.fromkeys(docVal).keys())
                parentheticResult["%s %d %s" % (firstTerm, rangee-1, secondTerm)][doc] = 0
                for ind, el in enumerate(docVal):
                    if el == firstTerm:
                        firstTermIndex = ind
                    if el == secondTerm:
                        secondTermIndex = ind

                if secondTermIndex > 0:
                    if firstTermIndex < secondTermIndex:
                        diff = secondTermIndex - firstTermIndex
                        if diff <= rangee-1:
                            parentheticResult["%s %d %s" % (firstTerm, rangee-1, secondTerm)][doc] = 1

            return parentheticResult

        except:
            print('Proximity clause can not be processed')


    def queryAnswer(self, originalquery, tempQuery, mapKey, res):
        """Gives the final result of Documents for the query"""
        printRes = []
        if len(tempQuery.split(" ")) == 1:
            for outRes in res[mapKey[tempQuery]].keys():
                if res[mapKey[tempQuery]][outRes]:
                    printRes.append(outRes)
            if( len(printRes) > 1):
                print("Matching documents for query ", originalquery, " are : ", printRes)
            else:
                print("None of the documents matching the query ", originalquery)
        else:
            print("Incorrect Query")

    def queryCalculator(self, querySep, mainIndex, stemmer, preProcessRes):
        """Resolves the {} or () clause and returns the result"""
        try:
            parentheticResult = {}
            for q in querySep:
                if '/' in q[1]:
                    parentheticResult = self.calCulateWithin(preProcessRes, q[1], stemmer, parentheticResult)
                else:
                    qWords = q[1].split(" ")
                    if len(qWords) == 3:
                        stemOne = stemmer.stem(qWords[0])
                        operator = qWords[1]
                        stemTwo = stemmer.stem(qWords[2])
                        if operator == "and":
                            parentheticResult["%s and %s" % (stemOne, stemTwo)] = {}
                            for key in mainIndex[stemOne].keys():
                                parentheticResult["%s and %s" % (stemOne, stemTwo)][key] = mainIndex[stemOne][key] and mainIndex[stemTwo][key]

                        if operator == "or":
                            parentheticResult["%s or %s" % (stemOne, stemTwo)] = {}
                            for key in mainIndex[stemOne].keys():
                                parentheticResult["%s or %s" % (stemOne, stemTwo)][key] = mainIndex[stemOne][key] or mainIndex[stemTwo][key]


                    elif len(qWords) > 3:
                        notRes = {}
                        stemOne = stemmer.stem(qWords[0])
                        operatorFirst = qWords[1]
                        operatorSecond = qWords[2]
                        stemTwo = stemmer.stem(qWords[3])
                        for key in mainIndex[stemOne].keys():
                            if operatorSecond == "not":
                                if not mainIndex[stemTwo][key] == True:
                                    notRes[key] = 1
                                else:
                                    notRes[key] = 0

                        if operatorFirst == "and":
                            parentheticResult["%s and not %s" % (stemOne, stemTwo)] = {}
                            for key in mainIndex[stemOne].keys():
                                parentheticResult["%s and not %s" % (stemOne, stemTwo)][key] = mainIndex[stemOne][key] and notRes[key]
                        if operatorFirst == "or":
                            parentheticResult["%s or not %s" % (stemOne, stemTwo)] = {}
                            for key in mainIndex[stemOne].keys():
                                parentheticResult["%s or not %s" % (stemOne, stemTwo)][key] = mainIndex[stemOne][key] or notRes[key]

            return parentheticResult
        except:
            print('The term is not present in the Documents')


if __name__ == '__main__':
    startTime = datetime.now()
    try:
      opts, _ = getopt.getopt(sys.argv[1:],"i:q:s:")
      if len(opts) != 3:
          print('Please pass all the parameters: python quesFive.py -i <inputfile> -s <stopwordfile> -q "query"')
          sys.exit()
    except getopt.GetoptError:
      print('usage: -i <inputfile> -s <stopwordfile> -q "query"')
      sys.exit()

    for opt, arg in opts:
        if opt == '-i':
            iFile = arg
        if opt == '-s':
            stopwordFile = arg
        if opt == '-q':
            query = arg
    start = Search(iFile, query, stopwordFile)
    start.querySearcher()
    print(datetime.now() - startTime)
