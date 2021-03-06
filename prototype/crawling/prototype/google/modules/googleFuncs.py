#!/usr/bin/python
#googleFuncs.py

import urllib.request
import requests
import re
from bs4 import BeautifulSoup
import time
import random

#--------------------------------------------------------------------------
# cnt개의 뉴스 제목과 링크 반환
#--------------------------------------------------------------------------
def getNewsList(search_words, cnt):
    enc_text = urllib.parse.quote(search_words)
    base_url = 'https://www.google.co.kr/search?q='
    suffix1 = "&tbm=nws&start="
    suffix2 = "&sa=N"
    # header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
    #     (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    p = re.compile(r"\?q=.*&sa")

    news_list = []
    start = 0
    while len(news_list) < cnt:
        try:
            res = requests.get(
                base_url + enc_text + suffix1 + str(start) + suffix2)

            #블럭 당하면 caller 에게 -1로 알림
            if re.compile(r"Our systems have detected").search(res.text):
                return -1 

            soup =  BeautifulSoup(res.content, 'html.parser')
            cand_list = soup.select('#ires ol div table h3 a')
            if len(cand_list) == 0: break   # 뉴스가 모자라면 그만둠
            for cand in cand_list:
                if len(news_list) >= cnt: break # 다 채웠으면 그만둠
                m = p.search(cand.get('href'))
                if m:
                    link = m.group()[3:-3]
                    news_list.append({
                        'title' : cand.text,
                        'link' : urllib.parse.unquote(link).strip() })
                else:
                    print("skipped: " + cand.get('href'))
        except Exception as e:
            print(e)
        finally:
            start += 10 # 다음 페이지
            wait = round(random.uniform(0, 2.5), 1)
            print("random sleep {} sec...".format(wait))
            time.sleep(wait)

    return news_list


#--------------------------------------------------------------------------
# module test code - getNewsList()
#--------------------------------------------------------------------------
if __name__ == "__main__":
    news_list = getNewsList("조국 수호", 11)
    for news in news_list:
        print(news)
    print("total: {}".format(len(news_list)))