# -*- coding: utf-8 -*-
#!/usr/bin/python
#harvesta.py

from modules import *
import json
import time
import os
import shutil
from datetime import datetime
import pandas as pd

# --------------------------------------------------------------------------
# 검색어 list 수집
# --------------------------------------------------------------------------
# keywords list들을 담을 dicntionary
keywordsource_dic = {}
# NAVER와 DAUM의 인기 검색어 수집(google은 제공하지 않고, Twitter는 trend의 경우 의미 없다고 판단하여 사용하지 않음)
naver_search_list = naverFuncs.getKeywords(10)
daum_search_list = daumFuncs.getKeywords()
keywordsource_dic['NAVER'] = naver_search_list
keywordsource_dic['DAUM'] = daum_search_list

# --------------------------------------------------------------------------
# 뉴스 URL list 수집
# --------------------------------------------------------------------------
# 편의상 데이터 프레임 사용
colnames = ['source', 'keywords', 'knum', 'target', 'nnum', 'title', 'url']
df = pd.DataFrame(columns=colnames)

print("Collecting New list. Please wait...  ")
doGoogling = True
for keyword_source in keywordsource_dic.keys():
    keywords_list = keywordsource_dic[keyword_source]
    for i, keywords in enumerate(keywords_list):
        print("{} 검색어 {} NAVER 뉴스 수집 시작... ".format(keyword_source, i+1), flush=True)
        naver_list = naverFuncs.getNewsList(keywords, 30)
        util.insertDFRow(df, keyword_source, keywords, i, 'NAVER', naver_list)
            
        print("{} 검색어 {} DAUM 뉴스 수집 시작... ".format(keyword_source, i+1), flush=True)
        daum_list =  daumFuncs.getNewsList(keywords, 30)
        util.insertDFRow(df, keyword_source, keywords, i, 'DAUM', daum_list)
        
        if doGoogling :
            print("{} 검색어 {} Google 뉴스 수집 시작... ".format(keyword_source, i+1), flush=True)
            google_list = googleFuncs.getNewsList(keywords, 30)
            if google_list != -1:
                util.insertDFRow(df, keyword_source, keywords, i, 'Google', daum_list)
            else:
                print("!"*10 + " Google locks us " + "!"*10)
                doGoogling = False

print("모든 뉴스 수집 완료")

# 테스트 저장(잦은 뉴스 수집으로 블럭 당할 수 있으니 테스트 중엔 저장한 정보를 읽어서 테스트)
df.to_csv("output.csv", mode='w', index=False)

# 블럭을 피하려 테스트 중에는 저장된 파일 이용
dfloaded = pd.read_csv('output.csv')


#--------------------------------------------------------------------------
# 약속된 디렉토리에 html 저장
#--------------------------------------------------------------------------
initialDic = {'NAVER' : 'N', 'DAUM' : 'D', 'Google' : 'G', 'Twitter' : 'T'}
# output root 생성
root = "c:\\harvesta_output"
if not(os.path.isdir(root)): os.makedirs(root)
now = datetime.now()

# yyMMdd 폴더 생성
yyMMdd = "%d%d%02d" % (now.year % 100, now.month, now.day)
yyMMdd = os.path.join(root, yyMMdd)
if not(os.path.isdir(yyMMdd)): os.makedirs(yyMMdd)

# hhmm 폴더 생성
hhmm = "%02d%02d" % (now.hour, now.minute // 10 * 10)
hhmm = os.path.join(yyMMdd, hhmm)
# 싹 지우고 새로 만들기
if os.path.isdir(hhmm): shutil.rmtree(hhmm)
if not(os.path.isdir(hhmm)): os.makedirs(hhmm)

for i in range(len(dfloaded.index)):
    row = dfloaded.iloc[i]
    # keyword 폴더 생성
    dirpath = "%s_K_%02d" % (initialDic[row['source']], row['knum'] + 1)
    dirpath = os.path.join(hhmm, dirpath)
    if not(os.path.isdir(dirpath)): os.makedirs(dirpath)
    # 파일 저장
    filepath = "%s_%02d.txt" % (initialDic[row['target']], row['nnum'] + 1)
    filepath = os.path.join(dirpath, filepath)
    with open(filepath, "w" , encoding = "utf-8") as fp:
        fp.write("내일 하자")
    




    
   










