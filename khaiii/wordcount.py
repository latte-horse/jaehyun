# wordcount.py

import sys
from collections import Counter

file = open(sys.argv[1], "r", encoding='utf-8-sig')
wordList = Counter(file.read().split("\n")).most_common()

for item in wordList: 
    print( "{}\t{}".format(*item) )
