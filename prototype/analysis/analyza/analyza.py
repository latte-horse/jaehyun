#!/usr/bin/python
#analyza.py


from gensim.models import Word2Vec
from modules import util
import os
import re
import pandas


#------------------------------------------------------------------------------
#  TBD
#------------------------------------------------------------------------------
def do_edit(path):
    # 문서 파일 리스트 생성
    filelist = list(filter(lambda file :  
            re.compile(r"DONE.txt").search(file), os.listdir(path)))
    filelist = list(map(lambda file : os.path.join(path, file), filelist))

    # tokens  = komoran.pos(doc0, flatten=True)
    # print(komoran.nouns(doc0))

    lines = util.getlines(filelist)

    model = Word2Vec(lines, 
        size=200, window = 5, min_count=20, workers=4, iter=200, sg=1)


    wv = model.wv
    del(model)

    vocs = []
    for key in wv.vocab:
        vocs.append(key)
    
    df =  pandas.DataFrame(columns = vocs , index = vocs)
    for i in vocs:
        dists = []
        for j in vocs:
            dists.append(wv.distance(i, j))
        df[i] = dists

    # 분석을 위해 임시 저장
    df.to_csv("d-matrix.csv", encoding="utf-8")






    # print(model.wv.distances("발언"))












#------------------------------------------------------------------------------
#  main
#------------------------------------------------------------------------------
if __name__ == "__main__":
    path = "C:\\crawllica_output\\191017\\1630\\D_K_01"

    do_edit(path)
   

    

    