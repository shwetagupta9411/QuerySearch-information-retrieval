# QuerySearch

1. I am using python3 for this assignment and the version is Python 3.7.4.
2. Please make sure you keep all the files in one folder and pass the correct file path where ever needed.
3. Question two Generates the inverted index as per the given requirements(it does not generates the matrix of frequencies of terms) .
4. In **question-3** please make sure you pass **input file with matrix of frequencies of terms**.

# Please check the following commands and arguments to run the programmes-

## **Question One**

```
python3 quesOne.py -i <inputFile> -o <outputFile> -s <stopwordList>
Args:
    -i inputFileOne.txt
    -o outputFileOne.txt
    -s stopwordList.txt

example:
python3 quesOne.py -i inputFileOne.txt -o outputFileOne.txt -s stopwordList.txt

```

## **Question Two**

```
python3 quesTwo.py -i <inputFile> -o <outputFile>
Args:
    -i inputFileTwo.txt
    -o outputFileTwo.txt

example:
python3 quesTwo.py -i inputFileTwo.txt -o outputFileTwo.txt

```

## **Question Three**

```
python3 quesThree.py -i <inputFileThree> -o <outputFileThree>
Args:
    -i inputFileThree.txt
    -o outputFileThree.txt

example:
python3 quesThree.py -i inputFileThree.txt -o outputFileThree.txt

```

## **Question Four**

```
python3 quesFour.py --input <outputFileThree> --docOne <D1> --docTwo <D2>
Args:
    --input outputFileThree.txt
    --docOne D1
    --docTwo D2

example:
python3 quesFour.py --input outputFileThree.txt --docOne D1 --docTwo D2

```

## **Question Five**

*Query should be in double quotes*

```
python3 quesFive.py -i <inputFileFive> -s <stopwordList> -q <"material OR {new BUT NOT research} AND barrier">
Args:
    -i inputFileOne.txt
    -s stopwordfile.txt
    -q "breakthrough AND material"

example:
python3 quesFive.py -i inputFileOne.txt -s stopwordList.txt -q "material OR {new BUT NOT research} AND barrier"

```

# sample queries -
# python3 quesFive.py -i inputFileOne.txt -s stopwordList.txt -q "{breakthrough AND new} BUT NOT many"
# python3 quesFive.py -i inputFileOne.txt -s stopwordList.txt -q "shweta AND barrier"
# python3 quesFive.py -i inputFileOne.txt -s stopwordList.txt -q "past OR {new AND student}"
# python3 quesFive.py -i inputFileOne.txt -s stopwordList.txt -q "material OR {new BUT NOT research} AND barrier"
# python3 quesFive.py -i inputFileOne.txt -s stopwordList.txt -q "{past BUT NOT research} AND barrier"
# python3 quesFive.py -i inputFileOne.txt -s stopwordList.txt -q "new BUT NOT (approach AND barrier)"
# python3 quesFive.py -i inputFileOne.txt -s stopwordList.txt -q "challenge or (research BUT NOT materi)"
# python3 quesFive.py -i inputFileOne.txt -s stopwordList.txt -q "{material /2 research} OR {research OR material} AND {breakthrough BUT NOT barrier} AND NOT student"
# python3 quesFive.py -i inputFileOne.txt -s stopwordList.txt -q "{material AND research} OR {research OR material} AND {breakthrough BUT NOT barrier} AND NOT student"
