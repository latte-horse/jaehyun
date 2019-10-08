#!/usr/bin/python
#gglNewsSearch.py

import codecs
from bs4 import BeautifulSoup
import ssl, urllib.request 
import requests
import traceback
import re


base_url = 'https://www.google.co.kr'

#: 검색조건 설정
target = "에어핏 1&1 대란"
values = {
    'q': target,    # 검색할 내용
    'oq': target,
    'aqs': 'chrome..69i57.35694j0j7',
    'sourceid': 'chrome',
    'ie': 'UTF-8'
}

# Google에서는 Header 설정 필요
hdr = {'User-Agent': 'Mozilla/5.0'}

query_string = urllib.parse.urlencode(values)
req = urllib.request.Request(base_url + '/search?' + query_string, headers=hdr)
context = ssl._create_unverified_context()
try:
    res = urllib.request.urlopen(req, context=context)
except:
    traceback.print_exc()

res_read = res.read()
html_text = res_read.decode('utf-8')
f = codecs.open("sample.html", "w", encoding="utf8")
f.write(html_text)
f.close()


tag_list = []
soup = BeautifulSoup(res_read, 'html.parser')
cand_list = soup.select('.ZINbbc.xpd.O9g5cc.uUPGi div.kCrYT a')
for cand in cand_list:
     temp = cand.select('.BNeawe.vvjwJb.AP7Wnd')
     if len(temp) != 0:
          tag_list.append(cand)

for tag in tag_list:
    print(tag)

tag_next = soup.select(".nBDE1b.G5eFlf")[0]
str_next = str(tag_next)
print(str_next)
p = re.compile("href=.*\"")
m = p.search(str_next)
if m:
    str_next = m.group()
else:
    print("next page not found error")
    exit(1)

str_next = base_url + re.sub("href=\"", "", str_next)[0:-1]
print(str_next)

res = requests.get(str_next)
# print(res.status_code)
# print(res.text)
soup = BeautifulSoup(res.text, 'html.parser')
cand_list = soup.select('.ZINbbc.xpd.O9g5cc.uUPGi div.kCrYT a')
for cand in cand_list:
     temp = cand.select('.BNeawe.vvjwJb.AP7Wnd')
     if len(temp) != 0:
          tag_list.append(cand)

for tag in tag_list:
    print(tag)