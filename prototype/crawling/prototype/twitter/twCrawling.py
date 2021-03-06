#!/usr/bin/python
#twCrawling.py

from twitter import Twitter, OAuth
from modules import *

#--------------------------------------------------------------------------
# 지역코드 받아오기
#--------------------------------------------------------------------------
woeid = twFuncs.getWOEID("Korea")

#--------------------------------------------------------------------------
# twitter API 인증
#--------------------------------------------------------------------------
twitter = twFuncs.getTwitterModule()
#--------------------------------------------------------------------------
# 실시간 트렌드 10개 추출
#--------------------------------------------------------------------------
trend_list = twFuncs.getWebTrends(woeid)
#for trend in trend_list: print(trend)

#--------------------------------------------------------------------------
# 키워드당 100개씩의 tweet 추출
#--------------------------------------------------------------------------
twitter_list = []
for search_words in trend_list[:2]: #테스트로 2개만
    tweet_list = twFuncs.getTweets(twitter, search_words, 5) #테스트로 3개만
    twitter_list.append({'search_words' : search_words, 'items' : tweet_list})
    #tweetListList.append(tweetList)

#--------------------------------------------------------------------------
# 결과 확인
#--------------------------------------------------------------------------
for elem in twitter_list:
    print("검색어: " + elem['search_words'])
    for tweet in elem['items']:
        print(tweet)
    print("")


