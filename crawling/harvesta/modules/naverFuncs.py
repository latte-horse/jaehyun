# -*- coding: utf-8 -*-
#naverFuncs.py

import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import json
if __name__ != '__main__':
    from . import config


#--------------------------------------------------------------------------
# 실시간 인기 검색어 cnt개 반환
#--------------------------------------------------------------------------
def getKeywords(cnt):
    url_naver = "https://www.naver.com"
    try:
        html = requests.get(url_naver).content
        soup = BeautifulSoup(html, 'html.parser')
        list_tag = soup.select('.ah_roll_area .ah_k')
        naver_keywords = []
        for keyword in list_tag:
            naver_keywords.append(keyword.get_text())
    except Exception as e:
        print(e)

    #cnt 개의 결과만을 반환
    return naver_keywords[:min([len(naver_keywords), cnt])]


#--------------------------------------------------------------------------
# 검색어로 뉴스를 검색하여 cnt개 반환
#--------------------------------------------------------------------------
def getNewsList(search_words, cnt):
    enc_text = urllib.parse.quote(search_words)
    url = "https://openapi.naver.com/v1/search/news.json?query={0}&display={1}&sort={2}".format(
        enc_text, cnt, "date") 

    # NAVER API를 이용하여 검색
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", config.clientID)
    request.add_header("X-Naver-Client-Secret", config.clientSecret)
    try:
        response = urllib.request.urlopen(request)
    except Exception as e:
        print(e)
    else:
        rescode = response.getcode()
        if(rescode == 200):
            response_body = response.read()
            news_list = json.loads(response_body.decode('utf-8'))['items']

            # title과 link만 추출하여 담기
            result_list = []
            for news in news_list:
                result_list.append({ 
                    'title' : re.sub("<[^>]*>", '', news['title']),
                    'link' : news['originallink'] != '' and news['originallink'] or news['link']})
        else:
            print("Error Code:" + rescode)
   
    #결과 반환 (없으면 없는대로)
    return result_list


#--------------------------------------------------------------------------
# module test code
#--------------------------------------------------------------------------
if __name__ == "__main__":
    naver_keywords = getKeywords(120)
    print(naver_keywords)
    import config
    news_list = getNewsList("미대륙 횡단열차", 30) #1 키워드 1 뉴스 테스트
    for news in news_list: print(news)