#!/usr/bin/python
#gglCrawling.py

from modules import *
import json


#--------------------------------------------------------------------------
# 테스트용 검색어(google은 대한민국의 경우 실시간 검색어 없음)
#--------------------------------------------------------------------------
search_list = [
    "불타는 청춘", 
    "패스트 트랙 수사"
]


#--------------------------------------------------------------------------
# 검색어당 30개씩의 뉴스 제목과 링크 추출
#--------------------------------------------------------------------------
google_list = []
for search_words in search_list:
    news_list = googleFuncs.getNewsList(search_words, 30)
    google_list.append({'keyword' : search_words, 'items' : news_list})


#--------------------------------------------------------------------------
# 결과 확인(output.json)
#--------------------------------------------------------------------------
with open("output.json", "w" ,encoding = "utf-8") as fp:
    json.dump(google_list, fp, ensure_ascii=False, indent="\t")


