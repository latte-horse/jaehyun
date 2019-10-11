# -*- coding: utf-8 -*-
#!/usr/bin/python
#preproca.py

from modules import util
from modules import removeRules
from bs4 import BeautifulSoup
import re


# --------------------------------------------------------------------------
# 타겟 파일 리스트 생성
# --------------------------------------------------------------------------
list_target = util.getTargetList("191011\\0940")

# --------------------------------------------------------------------------
# 개별 파일 전처리 시작
# --------------------------------------------------------------------------
print("전처리 시작")
count = len(list_target)
for i, filepath in enumerate(list_target):
    print("{}/{}".format(i+1, count), flush=True)
    fp_src = open(filepath, "r", encoding="utf-8")
    text = fp_src.read()
    fp_src.close()

    soup = BeautifulSoup(text, "html.parser")

    # 기본적인 태그 등 제거
    [s.extract() for s in soup.select(
        "script, a, style, img, noscript, footer, #footer, \
            input, label")]

    # 싸이트 특정 태그 등 제거
    for func in removeRules.getSiteRuleFuncs():
        soup = func(soup)

    # 글로벌 문자열 치환
    text = removeRules.commonTextRemover(soup)

    #결과 파일 생성
    path_output = filepath[:-4] + "_DONE.txt"
    with open(path_output, "w", encoding="utf-8") as fp_out:
        fp_out.write(text)
        
print("전처리 완료")

