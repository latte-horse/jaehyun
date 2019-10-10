# -*- coding: utf-8 -*-
#util.py

import urllib.request
import requests
from bs4 import BeautifulSoup
import re

def insertDFRow(df, keyword_source, keywords, i, news_source, news_list):
    for j, news in enumerate(news_list):
        df.loc[len(df.index)] = [keyword_source, keywords, i, news_source, j, news['title'], news['link']]

        
def getBody(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    # p = re.compile(r"zdnet")
    # if p.search(url):
    #     url = re.sub(r"\?f=o", "", url)

    code = 0
    text = ""
    try:
        res = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        code = 1; text = e

    else:  
        res = res.content
        soup = BeautifulSoup(res, 'html.parser')
        body = soup.select_one("body")
        body = str(body)
        body = re.sub("<body.*>", "", body)
        body = re.sub("</body>", "", body)
        code = 0; text = body

    return {'code' : code , 'text' : text}


#--------------------------------------------------------------------------
# module test code
#--------------------------------------------------------------------------
if __name__ == "__main__":
    body = getBody("http://www.kookje.co.kr/news2011/asp/newsbody.asp?code=0700&key=20191010.99099004655")
 
    print(body)