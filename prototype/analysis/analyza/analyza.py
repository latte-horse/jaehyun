#!/usr/bin/python
# -*- coding: utf-8 -*-
#analyza.py

from konlpy.tag import Komoran
from gensim.models import Word2Vec
import os
import re


#------------------------------------------------------------------------------
#  TBD
#------------------------------------------------------------------------------
def do_edit(path):
    # 문서 파일 리스트 생성
    filelist = list(filter(lambda file :  
            re.compile(r"DONE.txt").search(file), os.listdir(path)))
    filelist = list(map(lambda file : os.path.join(path, file), filelist))

    komoran = Komoran()
    # doc0 = open(filelist[0], 'r', encoding='utf-8').read()
    # doc1 = re.sub("\xa0", " ", open(filelist[1], 'r', encoding='utf-8').read())
    # tokens  = komoran.pos(doc0, flatten=True)
    # print(komoran.nouns(doc0))

    lines = []
    for i, file in enumerate(filelist):
        with open(file, 'r', encoding='utf-8') as fp:
            while True:
                try:
                    line = fp.readline()
                    if not line: break
                    line = re.sub("\xa0", " ", line).strip()
                    if line == "" : continue
                    tokens = komoran.nouns(line)
                    if len(tokens) == 0: continue
                    lines.append(komoran.nouns(line))
                except Exception as e:
                    print(e)
                    continue


    model = Word2Vec(lines, 
        size=200, window = 5, min_count=20, workers=4, iter=200, sg=1)

    for i, word in enumerate(model.wv.most_similar(positive="국감", topn=100)):
        print("%03d\t%s" % (i, word))

    print(len(model.wv.vocab))








#------------------------------------------------------------------------------
#  main
#------------------------------------------------------------------------------
if __name__ == "__main__":
    path = "C:\\crawllica_output\\191017\\1630\\D_K_01"

    do_edit(path)
   

    

    