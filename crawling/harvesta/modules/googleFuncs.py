# -*- coding: utf-8 -*-
#googleFuncs.py

import urllib.request
import requests
import re
from bs4 import BeautifulSoup
import time


#--------------------------------------------------------------------------
# cnt개의 뉴스 제목과 링크 반환
#--------------------------------------------------------------------------
def getNewsList(search_words, cnt):
    enc_text = urllib.parse.quote(search_words)
    base_url = 'https://www.google.co.kr/search?q='
    suffix1 = "&tbm=nws&start="
    suffix2 = "&sa=N"
    p = re.compile(r"\?q=.*&sa")

    news_list = []
    start = 0
    while len(news_list) < cnt:
        res = requests.get(base_url + enc_text + suffix1 + str(start) + suffix2).text
        f = open("sample.html", "w", encoding="utf-8")
        f.write(res)
        f.close()
        soup =  BeautifulSoup(res, 'html.parser')
        cand_list = soup.select('#ires ol div table h3 a')
        if len(cand_list) == 0: break;
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
        time.sleep(0.5)

    return news_list


#--------------------------------------------------------------------------
# module test code - getNewsList()
#--------------------------------------------------------------------------
if __name__ == "__main__":
    news_list = getNewsList("검찰 개혁", 11) # 뉴스 11개 테스트
    print(news_list) 