#!/usr/bin/env python
#tw-trends.py

import requests
from operator import itemgetter
import re

#
# Twitter API를 이용한 실시간 트렌드 10개
#
def getAPITrends(twitter, woeid):
    
    results = twitter.trends.place(_id = woeid) 

    listTrendsCompact = []
    for location in results:
        for trend in location["trends"]:
            name = re.sub('#', '', trend["name"])
            name = re.sub('_', ' ', name)
            volume = trend["tweet_volume"]
            volume = 0 if volume == None else volume
            listTrendsCompact.append({"name" : name, "volume" : volume, "len" : len(name)})
    sortedTrends = sorted(listTrendsCompact, key=itemgetter("volume", "len"), reverse=True)

    listFinal = []
    for trend in sortedTrends[:10]:
        listFinal.append(trend["name"])
    
    return listFinal
    
    """
    for location in results:
        for trend in location["trends"]:
            #print(" - %s" % trend["name"])
            print(trend)
    """


#
# 비로그인 GET 방식을 이용한 수동 수집 꼼수 트렌드 10개
#
def getWebTrends(woeid):
    data = requests.get("https://twitter.com/i/trends?id=" + woeid).json()
    #ToDo: 파싱 작업 필요. 추후 구현.
    
