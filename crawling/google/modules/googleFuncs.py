#!/usr/bin/python
#googleFuncs.py

import urllib.request
import requests
import re
from bs4 import BeautifulSoup


#--------------------------------------------------------------------------
# cnt개의 뉴스 제목과 링크 반환
#--------------------------------------------------------------------------
def getNewsList(search_word, cnt):

    base_url = 'https://www.google.co.kr/search?q='
    search_word = urllib.parse.quote(search_word)
    suffix1 = "&tbm=nws&ei=I4GcXdSdDvqJr7wPxKyg0A4&start="
    suffix2 = "&sa=N"
    p = re.compile(r"\?q=.*&sa")

    news_list = []
    start = 0
    while len(news_list) < cnt:
        res = requests.get(base_url + search_word + suffix1 + str(start) + suffix2).text
        soup =  BeautifulSoup(res, 'html.parser')
        cand_list = soup.select('#ires ol div table h3 a')
        for cand in cand_list:
            if len(news_list) >= cnt: break;
            m = p.search(cand.get('href'))
            if m:
                link = m.group()[3:-3]
                news_list.append({
                    'title' : cand.text,
                    'link' : urllib.parse.unquote(link).strip() })
            else:
                print("skipped: " + cand.get('href'))

        start += 10
    
    return news_list


#--------------------------------------------------------------------------
# module test code - getNewsList()
#--------------------------------------------------------------------------
if __name__ == "__main__":
    news_list = getNewsList("조국 수호", 11)
    for news in news_list:
        print(news)
    print("total: {}".format(len(news_list)))