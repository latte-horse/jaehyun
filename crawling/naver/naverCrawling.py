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
for search_words in naver_keywords[:2]: #테스트로 2개만
    news_list = naverFuncs.getNewsList(search_words, 3) #테스트로 3개만
    naver_list.append({'search_words' : search_words, 'items' : news_list})

#--------------------------------------------------------------------------
# 결과 확인
#--------------------------------------------------------------------------
for elem in naver_list:
    print("검색어: " + elem['search_words'])
    for news in elem['items']:
        print(news)
    print("")


# 추후 json 변환이 필요할 경우 참조 코드
# dump = json.dumps(target_str, ensure_ascii = False).encode("utf-8")
