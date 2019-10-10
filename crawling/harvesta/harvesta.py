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
df_tw = pd.DataFrame(columns=colnames)
print("Collecting News list. Please wait...  ")
# 구글 검색은 초기 진입시 시도하지만 블럭을 먹으면 멈춰야 하므로 flag를 설정한다
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

print("모든 뉴스 수집 완료")

# 코드 작성 중 잦은 뉴스 수집으로 블럭 당할 수 있으니 테스트 중엔 결과를 저장
df.to_csv("output.csv", mode='w', index=False, encoding="utf-8")
df_tw.to_csv("output_tw.csv", mode='w', index=False, encoding="utf-8")

# 코드 작성 테스트 중 블럭을 피하려 테스트 중에는 저장된 파일 이용
dfloaded = pd.read_csv('output.csv')
dfloaded_tw = pd.read_csv('output_tw.csv')


#--------------------------------------------------------------------------
# 약속된 디렉토리 상위 구조 생성
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


#--------------------------------------------------------------------------
# html 저장
#--------------------------------------------------------------------------
# 로그 파일
logfp = open(os.path.join(hhmm, "log.txt"), "w", encoding="utf-8")
print("저장 시작")
#-------------------------------------
# 일반 뉴스 저장
#-------------------------------------
count = len(dfloaded.index)
for i in range(count):
    print("News: {} / {} 저장중".format(i+1, count))
    row = dfloaded.iloc[i]
    # keyword 폴더 생성 ex) D_K_01
    dirpath = "%s_K_%02d" % (initialDic[row['source']], row['knum'] + 1)
    dirpath = os.path.join(hhmm, dirpath)
    if not(os.path.isdir(dirpath)): os.makedirs(dirpath)
    # 파일 저장 패스 생성 ex) D_01.txt
    filepath = "%s_%02d.txt" % (initialDic[row['target']], row['nnum'] + 1)
    filepath = os.path.join(dirpath, filepath)

    # html 가져오기 성공 시 파일 생성
    body = util.getBody(row['url'])
    if body['code'] == 0:
        fp = open(filepath, "w" , encoding="utf-8")
        fp.write("{}\n".format(row['title']))
        fp.write("{}".format(body['text']))
        fp.flush(); fp.close()
    else:
        errortext = "{}\t{}\t{}\n\n".format(i+1, row['url'], body['text'])
        print(errortext)
        logfp.write(errortext)
        logfp.flush()
#-------------------------------------
# 트위터 저장
#-------------------------------------
count = len(dfloaded_tw)
for i in range(count):
    print("Tweets: {} / {} 저장중".format(i+1, count))
    row = dfloaded_tw.iloc[i]
    # keyword 폴더 생성 ex) D_K_01
    dirpath = "%s_K_%02d" % (initialDic[row['source']], row['knum'] + 1)
    dirpath = os.path.join(hhmm, dirpath)
    if not(os.path.isdir(dirpath)): os.makedirs(dirpath)
    # 파일 저장 패스 생성 ex) D_01.txt
    filepath = "%s_%02d.txt" % (initialDic[row['target']], row['nnum'] + 1)
    filepath = os.path.join(dirpath, filepath)

    # tweets 가져오기 성공 시 파일 생성(타입이 str 일 경우만 저장)
    if type(row['url']) == type(""):
        fp = open(filepath, "w" , encoding="utf-8")
        fp.write(row['url'])
        fp.flush(); fp.close()

print("저장 끝")
