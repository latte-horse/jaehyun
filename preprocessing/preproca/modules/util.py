# -*- coding: utf-8 -*-
#util.py

import os
import re

rootpath = "c:\\harvesta_output"

#------------------------------------------------------------------------------
# "yyMMdd\\hhmm" 형식의 패스를 주면 모든 하위 파일 리스트를 넘겨주는 모듈
#------------------------------------------------------------------------------
def get_filelist(path):
    path = os.path.join(rootpath, path)

    # 모든 하위 디렉토리 풀 패스 생성
    kDirList = list(map(
        lambda x : os.path.join(path, x), os.listdir(path)))
    kDirList = list(filter(
        lambda x : os.path.isdir(x), kDirList))

    # 모든 하위 디렉토리의 모든 파일을 하나의 리스트에 담기
    targetList = []
    for path_keyword  in kDirList:
        fileList = list(map(
            lambda x : os.path.join(path_keyword, x), 
            os.listdir(path_keyword)))
        fileList = list(filter(
            lambda x : not re.compile("DONE").search(x), fileList))
        targetList += fileList

    return targetList


#------------------------------------------------------------------------------
# "yyMMdd\\hhmm" 형식의 패스를 주면 모든 DONE 문서를 삭제하는 함수(개발용)
#------------------------------------------------------------------------------
def remove_done(path):
    path = os.path.join(rootpath, path)

    # 모든 하위 디렉토리 풀 패스 생성
    kDirList = list(map(lambda x : os.path.join(path, x), 
        os.listdir(path)))
    # 디렉토리만 남기기
    for i, elem in enumerate(kDirList):
        if not os.path.isdir(elem): kDirList.pop(i)

    # 모든 하위 디렉토리의 모든 파일을 하나의 리스트에 담기
    targetList = []
    for path_keyword  in kDirList:
        fileList = list(map(lambda x : os.path.join(path_keyword, x), 
            os.listdir(path_keyword)))
        fileList = list(filter(
            lambda x : re.compile("DONE").search(x), fileList))
        # print(list_file)
        targetList += fileList
    
    [os.remove(file) for file in targetList]
    print("삭제 완료")


#------------------------------------------------------------------------------
# module test code
#------------------------------------------------------------------------------
if __name__ == "__main__":
    target_list = get_filelist("191012\\1150")
    for i, filepath in enumerate(target_list): print(str(i) + " " + filepath)
    # removeDone("191012\\1150")