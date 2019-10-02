#!/usr/bin/python

# doKhaiii.py

import sys
from khaiii import KhaiiiApi

api = KhaiiiApi()

if len(sys.argv) < 3:
    print("usage: doKahiii [input file to process] [output file]")
    exit(1)

inputPath = sys.argv[1]
outputPath = sys.argv[2]


f = open(inputPath, 'r')
strList = []
while True:
    line = f.readline()

    if not line: break
    if line == "\n": continue

    print(line)
    for word in api.analyze(line):
        strList.append("{0}".format(word))
f.close()

f = open(outputPath, "w")
for string in strList:
    f.writelines(string+"\n")
f.close()

print("Done.")
