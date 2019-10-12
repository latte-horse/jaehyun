# -*- coding: utf-8 -*-
#!/usr/bin/python
#preproca.py

from modules import *
from bs4 import BeautifulSoup
import re
import time
stime = time.time()


#------------------------------------------------------------------------------
# 타겟 파일 리스트 생성
#------------------------------------------------------------------path
list_target = util.get_filelist("191012\\1150")

#------------------------------------------------------------------------------
# 개별 파일 전처리 시작
#------------------------------------------------------------------------------

count = len(list_target)
for i, filepath in enumerate(list_target):
    print("{}/{}\t{}".format(i+1, count, filepath), flush=True)
    fp_src = open(filepath, "r", encoding="utf-8")
    text = fp_src.read()
    fp_src.close()

    soup = BeautifulSoup(text, "html.parser")

    # 제거 룰 적용
    for func in rules.get_rulefns():
        soup = func(soup)

    # 글로벌 문자열 치환
    text = rules.common_rm_text(soup.text)
    # for debugging
    # print(text)
    
    #결과 파일 생성
    path_output = filepath[:-4] + "_DONE.txt"
    with open(path_output, "w", encoding="utf-8") as fp_out:
        fp_out.write(text)

etime = time.time() - stime
print("걸린 시간: %dm %02ds" % (etime//60, etime%60) )

