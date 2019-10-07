#!/usr/bin/python
#twTrends.py

import requests
from operator import itemgetter
import re
from bs4 import BeautifulSoup

#--------------------------------------------------------------------------
# Twitter API를 이용한 실시간 트렌드 10개
#--------------------------------------------------------------------------
def getAPITrends(twitter, woeid):
    
    results = twitter.trends.place(_id = woeid) 

    compact_list = []
    for location in results:
        for trend in location["trends"]:
            name = re.sub('#', '', trend["name"])
            name = re.sub('_', ' ', name)
            volume = trend["tweet_volume"]
            volume = 0 if volume == None else volume
            compact_list.append({"name" : name, "volume" : volume, "len" : len(name)})
    sorted_list = sorted(compact_list, key=itemgetter("volume", "len"), reverse=True)

    final_list = []
    for trend in sorted_list[:10]:
        final_list.append(trend["name"])
    
    return final_list
    
    #메타 정보 확인을 위한 테스트 코드
    # for location in results:
    #     for trend in location["trends"]:
    #         #print(" - %s" % trend["name"])
    #         print(trend)


#--------------------------------------------------------------------------
# 비로그인 GET 방식을 이용한 수동 수집 꼼수 트렌드 10개
#--------------------------------------------------------------------------
def getWebTrends(woeid):
    trends_html = requests.get(
        "https://twitter.com/i/trends?id=" + "23424868").json()['module_html']
    soup = BeautifulSoup(trends_html, 'html.parser')
    tag_list = soup.select('.trend-name')

    trend_list = []
    for tag in tag_list:
        trend = re.sub(r"^[#]", "", tag.text)
        trend = re.sub(r"_", " ", trend)
        trend_list.append(trend)
    
    return trend_list


#--------------------------------------------------------------------------
# module test code - getWebTrends()
#--------------------------------------------------------------------------
if __name__ == "__main__":
    trends_html = requests.get(
        "https://twitter.com/i/trends?id=" + "23424868").json()['module_html']
    soup = BeautifulSoup(trends_html, 'html.parser')
    tag_list = soup.select('.trend-name')

    for tag in tag_list:
        trend = re.sub(r"^[#]", "", tag.text)
        trend = re.sub(r"_", " ", trend)
        print(trend)

