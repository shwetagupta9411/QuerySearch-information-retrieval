"""
Runs part 5 of assignment.
*Query should be in double quotes*

python3 quesFive.py
Args:
    -i inputFileOne.txt
    -q "breakthrough AND material"
"""

import os
import sys, getopt
import string, time
from datetime import datetime
from quesOne import PreProcessing
from quesTwo import InvertedIndexGenerator

# To run the script -
# python3 quesFive.py -i inputFileOne.txt -q "breakthrough AND material"
# python3 quesFive.py -i /Users/shwetagupta/Downloads/input_s1.txt -q "breakthrough AND material"

class Search(object):
    def __init__(self, iFile, query):
        self.iFile = iFile
        self.query = query

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
        preProcess = PreProcessing(False, self.iFile, "", "stopwordList.txt")
        createIndex = InvertedIndexGenerator(False, preProcess.process(), "")
        index = createIndex.generate()
        # print(index)
        # t =  list(self.parenthetic_contents("research AND material"))
        t = list(self.parenthetic_contents("research AND material OR research OR material"))
        print(t)
        print(self.query)

        # newlist = map(test, index)
        # print(list(self.parenthetic_contents(t[2][1])))
        # for k, v in index.iteritems():
        #     keysSub = v.keys()
        #     keysSub.sort()
        #     index[k][]




if __name__ == '__main__':
    startTime = datetime.now()
    try:
      opts, _ = getopt.getopt(sys.argv[1:],"i:q:")
      if len(opts) != 2:
          print('Please pass all the parameters: python quesTwo.py -i <inputfile> -o "query"')
          sys.exit()
    except getopt.GetoptError:
      print('usage: -i <inputfile> -q "query"')
      sys.exit()

    for opt, arg in opts:
        if opt == '-i':
            iFile = arg
        if opt == '-q':
            query = arg
    start = Search(iFile, query)
    start.querySearcher()
    # import timeit, functools
    # t = timeit.Timer(functools.partial(generateInvertedIndex, iFile, oFile))
    # print t.timeit(1)
    print(datetime.now() - startTime)
