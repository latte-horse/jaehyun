#!/usr/bin/python
#twTrends.py

import requests
from operator import itemgetter
import re

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
# 비로그인 GET 방식을 이용한 수동 수집 꼼수 트렌드 10개 (미완)
#--------------------------------------------------------------------------
def getWebTrends(woeid):
    data = requests.get("https://twitter.com/i/trends?id=" + woeid).json()
    #ToDo: 파싱 작업 필요. 추후 구현.
    
