# -*- coding: utf-8 -*-
#!/usr/bin/python
#harvesta.py

from modules import *
import urllib.request
import json
import time
import os
import shutil
from datetime import datetime
import pandas as pd


# --------------------------------------------------------------------------
# 검색어 list 수집
# --------------------------------------------------------------------------
naver_search_list = naverFuncs.getKeywords(10)
daum_search_list = daumFuncs.getKeywords()
keywordsource_dic = {'NAVER': naver_search_list, 'DAUM' :daum_search_list}


# --------------------------------------------------------------------------
# 뉴스 URL list 수집
# --------------------------------------------------------------------------
# 편의상 데이터 프레임 사용
colnames = ['ksource', 'keywords', 'knum', 'nsource', 'nnum', 'title', 'url']
df = pd.DataFrame(columns=colnames)
df_tw = pd.DataFrame(columns=colnames)
print("Collecting News list. Please wait...  ")
# 구글 검색은 초기 진입 시 시도하지만 블럭 먹으면 멈춰야 하므로 flag 를 설정한다
doGoogling = True
# Twitter 검색을 위한 twitter API 모듈 로드
twitter = twFuncs.getTwitterModule()
for keyword_source in keywordsource_dic.keys():
    keywords_list = keywordsource_dic[keyword_source]
    for i, keywords in enumerate(keywords_list):
        print("{} 검색어 {} NAVER 뉴스 수집 시작... ".format(keyword_source, i+1), flush=True)
        naver_list = naverFuncs.getNewsList(keywords, 30)
        util.insertDFRow(df, keyword_source, keywords, i, 'NAVER', naver_list)
            
        print("{} 검색어 {} DAUM 뉴스 수집 시작... ".format(keyword_source, i+1), flush=True)
        daum_list =  daumFuncs.getNewsList(keywords, 30)
        util.insertDFRow(df, keyword_source, keywords, i, 'DAUM', daum_list)

        # 구글의 경우 일시 블락이 걸릴 경우 다시 시도하지 않음
        if doGoogling :
            print("{} 검색어 {} Google 뉴스 수집 시작... ".format(keyword_source, i+1), flush=True)
            google_list = googleFuncs.getNewsList(keywords, 30)
            if google_list != -1:
                util.insertDFRow(df, keyword_source, keywords, i, 'Google', daum_list)
            else:
                print("!"*10 + " Google blocks us " + "!"*10)
                doGoogling = False

        # 트위터의 경우 특이 케이스로 다른 데이터 프레임에 담음
        print("{} 검색어 {} Twitter 트윗 수집 시작... ".format(keyword_source, i+1), flush=True)
        tweets = twFuncs.getTweets(twitter, keywords, 100)
        util.insertDFRow(df_tw, keyword_source, keywords, i, 'Twitter', tweets)
print("모든 뉴스 링크 수집 완료")


# #--------------------------------------------------------------------------
# # 코드 작성 중엔 잦은 뉴스 수집으로 블럭 당할 수 있으니 재사용 용도로 결과를 저장
# # 릴리즈 시 주석처리
# #--------------------------------------------------------------------------
# df.to_csv("output.csv", mode='w', index=False, encoding="utf-8")
# df_tw.to_csv("output_tw.csv", mode='w', index=False, encoding="utf-8")
# del(df)
# del(df_tw)
# # 이 위를 모두 주석 처리하고 테스트
# df = pd.read_csv('output.csv')
# df_tw = pd.read_csv('output_tw.csv')


#--------------------------------------------------------------------------
# 약속된 디렉토리 상위 구조 생성
#--------------------------------------------------------------------------
now = datetime.now()
output_root = "c:\\harvesta_output" + \
    "\\%d%d%02d" % (now.year % 100, now.month, now.day) + \
    "\\%02d%02d" % (now.hour, now.minute // 10 * 10)
# 디렉토리 존재 시 모두 삭제 후 새로 생성
if os.path.isdir(output_root): shutil.rmtree(output_root)
if not(os.path.isdir(output_root)): os.makedirs(output_root)


#--------------------------------------------------------------------------
# html 저장
#--------------------------------------------------------------------------
# Suffix Dict.
initialDic = {'NAVER' : 'N', 'DAUM' : 'D', 'Google' : 'G', 'Twitter' : 'T'}
# 로그 파일
logfp = open(os.path.join(output_root, "log.txt"), "w", encoding="utf-8")
print("저장 시작")
#-------------------------------------
# 일반 뉴스 저장
#-------------------------------------
count = len(df.index)
for i in range(count):
    print("News: {} / {} 저장중".format(i+1, count))
    row = df.iloc[i]
    # keyword 폴더 생성 ex) D_K_01
    dirpath = os.path.join(output_root, 
        "%s_K_%02d" % (initialDic[row['ksource']], row['knum'] + 1))
    if not(os.path.isdir(dirpath)): os.makedirs(dirpath)
    # 파일 저장 패스 생성 ex) D_01.txt
    filepath = os.path.join(dirpath, 
        "%s_%02d.txt" % (initialDic[row['nsource']], row['nnum'] + 1))
        
    # html 가져오기 성공 시 파일 생성
    body = util.getBody(row['url'])
    if body['code'] == 0:
        with open(filepath, "w" , encoding="utf-8") as fp:
            fp.write("{}\n".format(row['title']))
            fp.write(body['text'])
    # 실패시 error 로그 추가
    else:
        errortext = "{}\t{}\t{}\n\n".format(i+1, row['url'], body['text'])
        print(errortext)
        logfp.write(errortext)
        logfp.flush()
#-------------------------------------
# 트위터 저장
#-------------------------------------
count = len(df_tw)
for i in range(count):
    print("Tweets: {} / {} 저장중".format(i+1, count))
    row = df_tw.iloc[i]
    # keyword 폴더 생성 ex) D_K_01
    dirpath = os.path.join(output_root, 
        "%s_K_%02d" % (initialDic[row['ksource']], row['knum'] + 1))
    if not(os.path.isdir(dirpath)): os.makedirs(dirpath)
    # 파일 저장 패스 생성 ex) D_01.txt
    filepath = os.path.join(dirpath, 
        "%s_%02d.txt" % (initialDic[row['nsource']], row['nnum'] + 1))

    # tweets 가져오기 성공 시 파일 생성(타입이 str 일 경우만 저장)
    if type(row['url']) == type(""):
        with open(filepath, "w" , encoding="utf-8") as fp:
            fp.write(row['url'])

print("저장 끝")
