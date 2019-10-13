# -*- coding: utf-8 -*-
#!/usr/bin/python
#preproca.py

from modules import *
from bs4 import BeautifulSoup
import re
import time

# 시작 시간
stime = time.time()

#------------------------------------------------------------------------------
# 타겟 파일 리스트 생성
#------------------------------------------------------------------------------
rootpath = "c:\\harvesta_output\\"
list_target = util.get_filelist(rootpath + "191012\\1150")

#------------------------------------------------------------------------------
# 개별 파일 전처리 시작
#------------------------------------------------------------------------------
count = len(list_target)
for i, filepath in enumerate(list_target):
    # 로그
    print("{}/{}\t{}".format(i+1, count, filepath), flush=True)

    # 파일 읽고 닫기
    with open(filepath, "r", encoding="utf-8") as fp:
        text = fp.read()
    
    # 문장 단위 처리 편의성을 위해서 개행 추가
    text = re.sub(r"</p>", "</p>\n", text)
    text = re.sub(r"<br/?>", "\n", text)

    # 뷰티퓰스프로 떠넘기기
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

# 걸린 시간 출력
etime = time.time() - stime
print("걸린 시간: %dm %02ds" % (etime//60, etime%60) )

