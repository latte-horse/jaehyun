# wordcount.py

import sys
from collections import Counter

file = open(sys.argv[1], "r")
wordList = Counter(file.read().split()).most_common()

for item in wordList: 
    print( "{}\t{}".format(*item) )
