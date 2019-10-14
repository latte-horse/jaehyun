# -*- coding: utf-8 -*-
#!/usr/bin/python
#preproca.py

from .modules import *
from bs4 import BeautifulSoup
import re
import time

def preproc(inputRoot):
    # 시작 시간
    stime = time.time()

    #------------------------------------------------------------------------------
    # 타겟 파일 리스트 생성
    #------------------------------------------------------------------------------
    # rootpath = "c:\\harvesta_output\\"
    list_target = util.get_filelist(inputRoot)
    # for debugging
    # list_target = list_target[0:12]

    #------------------------------------------------------------------------------
    # 개별 파일 전처리 시작
    #------------------------------------------------------------------------------
    count = len(list_target)
    for i, (prefix, filepath) in enumerate(list_target):
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
        # 제목 남기기
        title = soup.text.split("\n")[0]

        # 제거 룰 적용
        for func in rules.get_rulefns():
            bNext, soup = func(soup)
            if not bNext: break
        
        # 화이트리스트 통과 했으면 본문만 있으므로 타이틀을 따로 넣어줌
        if not bNext: text = "{}\n{}".format(title, soup.text)
        else: text = soup.text
            
        # 글로벌 문자열 치환
        text = rules.common_rm_text(text)
        # for debugging
        print(text)

        
        #결과 파일 생성
        path_output = filepath[:-4] + "_DONE.txt"
        with open(path_output, "w", encoding="utf-8") as fp_out:
            fp_out.write(text)

    # 걸린 시간 출력
    etime = time.time() - stime
    print("걸린 시간: %dm %02ds" % (etime//60, etime%60) )

