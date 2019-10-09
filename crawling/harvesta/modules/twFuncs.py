# -*- coding: utf-8 -*-
#twFuncs.py

from twitter import Twitter, OAuth
import yweather
import requests
from operator import itemgetter
import re
from bs4 import BeautifulSoup
if __name__ != "__main__":
    from . import config


#--------------------------------------------------------------------------
# twitter Module 반환
#--------------------------------------------------------------------------
def getTwitterModule():
    return Twitter(auth = OAuth(
        config.access_key,
        config.access_secret,
        config.consumer_key,
        config.consumer_secret))


#--------------------------------------------------------------------------
# 지역명에 해당하는 WOEID 반환
#--------------------------------------------------------------------------
def getWOEID(location):
    return yweather.Client().fetch_woeid(location)


#--------------------------------------------------------------------------
# Twitter API를 이용한 실시간 트렌드 10개
#--------------------------------------------------------------------------
def getAPITrends(twitter, woeid):
    places = twitter.trends.place(_id = woeid) 
    compact_list = []
    for location in places:
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

    #메타 정보 확인을 위한 테스트 코드
    # for location in results:
    #     for trend in location["trends"]:
    #         #print(" - %s" % trend["name"])
    #         print(trend)
    
    return final_list


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
# 키워드를 받아 검색하여 cnt개의 tweet 내용을 list로 반환하는 함수
#--------------------------------------------------------------------------
def getTweets(twitter, keyword, cnt):
    tweet_list = []
    query = twitter.search.tweets(q = keyword, count = cnt)
    #print("Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"]))
    for result in query["statuses"]:
        tweet_list.append(result["text"])

    return tweet_list


#--------------------------------------------------------------------------
# module test conde
#--------------------------------------------------------------------------
if __name__ == "__main__":
    import config
    woeid = getWOEID("Korea"); print(woeid)
    trends = getWebTrends(woeid); print(trends)
    twitter = getTwitterModule()
    tweets = getTweets(twitter, trends[1], 100)
    for tweet in tweets:
        print(tweet)


#--------------------------------------------------------------------------
# module test code - getWebTrends()
#--------------------------------------------------------------------------
# if __name__ == "__main__":
#     trends_html = requests.get(
#         "https://twitter.com/i/trends?id=" + "23424868").json()['module_html']
#     soup = BeautifulSoup(trends_html, 'html.parser')
#     tag_list = soup.select('.trend-name')

#     for tag in tag_list:
#         trend = re.sub(r"^[#]", "", tag.text)
#         trend = re.sub(r"_", " ", trend)
#         print(trend)
