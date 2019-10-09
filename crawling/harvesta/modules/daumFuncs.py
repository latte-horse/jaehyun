# -*- coding: utf-8 -*-
#daumFuncs.py

import requests
from bs4 import BeautifulSoup
#import pandas as pd
import urllib.request
#from datetime import datetime
#import lxml
import json
#import pathlib

#--------------------------------------------------------------------------
# 실시간 인기 검색어 cnt개 반환
#--------------------------------------------------------------------------
def getKeywords():
    html = requests.get("https://www.daum.net").text
    soup=BeautifulSoup(html, 'html.parser')
    title_list = soup.select(".list_mini .rank_cont .link_issue")

    htmllist = []
    for top in title_list:
        htmllist.append(top.get_text())

    return htmllist


#--------------------------------------------------------------------------
# 검색어로 뉴스를 검색하여 cnt개 반환
#--------------------------------------------------------------------------
def getNewsList(search_words, cnt):
    enc_text = urllib.parse.quote(search_words)
    furl = "https://search.daum.net/search?w=news&sort=recency&q="
    surl = "&cluster=n&DA=STC&s=NS&a=STCF&dc=STC&pg=1&r=1&p="
    lurl = "&rc=1&at=more&sd=&ed=&period="

    news_list = []
    i = 0
    while len(news_list) < cnt: # cnt개 채울 때 까지
        url = requests.get(furl + enc_text + surl + str(i) + lurl).text
        soup = BeautifulSoup(url,'html.parser')
        urlname = soup.select(".f_link_b")
        urllink = soup.select("a[class*=f_link_b]")
        for list1, list2 in zip(urlname, urllink):
            if len(news_list) >= cnt: break; # cnt개 채우면 중단
            news_list.append({"title" : list1.text, "link" : list2.get('href')})

        i += 1

    return news_list


#--------------------------------------------------------------------------
# module test code
#--------------------------------------------------------------------------
if __name__ == "__main__":
    daum_keywords = getKeywords()
    print(daum_keywords)
    print(getNewsList(daum_keywords[0], 1)) #1 키워드 1 뉴스 테스트

