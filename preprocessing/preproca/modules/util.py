# -*- coding: utf-8 -*-
#util.py

import os
import re

rootpath = "c:\\harvesta_output"

#--------------------------------------------------------------------------
# "yyMMdd\\hhmm" 형식의 패스를 주면 모든 하위 파일 리스트를 넘겨주는 모듈
#--------------------------------------------------------------------------
def getTargetList(hhmmpath):
    path_hhmm = os.path.join(rootpath, hhmmpath)

    # 모든 하위 디렉토리 풀 패스 생성
    list_keyworddir = list(map(lambda x : os.path.join(path_hhmm, x), 
        os.listdir(path_hhmm)))
    # 디렉토리만 남기기
    for i, elem in enumerate(list_keyworddir):
        if not os.path.isdir(elem): list_keyworddir.pop(i)
    
    # 모든 하위 디렉토리의 모든 파일을 하나의 리스트에 담기
    list_target = []
    for path_keyword  in list_keyworddir:
        list_file = list(map(lambda x : os.path.join(path_keyword, x), 
            os.listdir(path_keyword)))
        # print(list_file)
        list_target += list_file

    return list_target


#--------------------------------------------------------------------------
# "yyMMdd\\hhmm" 형식의 패스를 주면 모든 DONE 문서를 삭제하는 함수(개발용)
#--------------------------------------------------------------------------
def removeDone(hhmmpath):
    path_hhmm = os.path.join(rootpath, hhmmpath)

    # 모든 하위 디렉토리 풀 패스 생성
    list_keyworddir = list(map(lambda x : os.path.join(path_hhmm, x), 
        os.listdir(path_hhmm)))
    # 디렉토리만 남기기
    for i, elem in enumerate(list_keyworddir):
        if not os.path.isdir(elem): list_keyworddir.pop(i)

    # 모든 하위 디렉토리의 모든 파일을 하나의 리스트에 담기
    list_target = []
    for path_keyword  in list_keyworddir:
        list_file = list(map(lambda x : os.path.join(path_keyword, x), 
            os.listdir(path_keyword)))
        list_file = list(filter(lambda x : re.compile("DONE").search(x), list_file))
        # print(list_file)
        list_target += list_file
    
    [os.remove(file) for file in list_target]
    print("삭제 완료")


#--------------------------------------------------------------------------
# module test code
#--------------------------------------------------------------------------
if __name__ == "__main__":
    # target_list = getTargetList("191011\\0940")
    # for i, filepath in enumerate(target_list): print(str(i) + " " + filepath)
    removeDone("191011\\0940")