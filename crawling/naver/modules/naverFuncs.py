#!/usr/bin/python
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
    naverKeywords = []
    url_naver = "http://www.naver.com"

    html = requests.get(url_naver).text
    soup = BeautifulSoup(html, 'html.parser')

    listHtml = soup.select('.ah_roll_area .ah_k')

    #naverKeywords 변수에 keyword 추가
    for keyword in listHtml:
        naverKeywords.append(keyword.get_text())

    #cnt 개의 결과만을 반환
    return naverKeywords[:cnt]


#--------------------------------------------------------------------------
# 검색어로 뉴스를 검색하여 cnt개 반환
#--------------------------------------------------------------------------
def getNewsList(search_words, cnt):
    encText = urllib.parse.quote(search_words)
    url = "https://openapi.naver.com/v1/search/news.json?query={0}&display={1}&sort={2}".format(
        encText, cnt, "date"
    ) 

    #naver API를 이용하여 검색
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", config.clientID)
    request.add_header("X-Naver-Client-Secret", config.clientSecret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        newsList = json.loads(response_body.decode('utf-8'))['items']

        #title과 link만 추출하여 담기
        resultList = []
        for news in newsList:
            resultList.append({ 
                'title' : re.sub("<[^>]*>", '', news['title']),
                'link' : news['link']})
        
        #결과 반환
        return resultList

    else:
        print("Error Code:" + rescode)
        exit(1)


#--------------------------------------------------------------------------
# module test code
#--------------------------------------------------------------------------
if __name__ == "__main__":
    naverKeywords = getKeywords(10)
    print(naverKeywords)
    import config
    print(getNewsList(naverKeywords[0], 10))