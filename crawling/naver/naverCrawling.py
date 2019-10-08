#!/usr/bin/python
#naverCrawling.py

from modules import naverFuncs
import json


#--------------------------------------------------------------------------
# 실시간 인기 검색어 10개 추출
#--------------------------------------------------------------------------
naver_keywords = naverFuncs.getKeywords(10)
#for keyword in naverKeywords: print(keyword)

#--------------------------------------------------------------------------
# 검색어당 30개씩의 뉴스 제목과 링크 추출
#--------------------------------------------------------------------------
naver_list = []
for search_words in naver_keywords[:3]: #테스트로 3개만
    news_list = naverFuncs.getNewsList(search_words, 3) #테스트로 3개만
    naver_list.append({'keyword' : search_words, 'items' : news_list})


#--------------------------------------------------------------------------
# 결과 확인(output.json)
#--------------------------------------------------------------------------
with open("output.json", "w" ,encoding = "utf-8") as fp:
    json.dump(naver_list, fp, ensure_ascii=False, indent="\t")
