#!/usr/bin/python
#tw_crawling.py

from twitter import *
import config
import tw_woeid
import tw_trends
import tw_search


# 지역코드 받아오기
woeid = tw_woeid.getWOEID("Korea")
# twitter API 인증
twitter = Twitter(auth = OAuth(
    config.access_key,
    config.access_secret,
    config.consumer_key,
    config.consumer_secret))

# 실시간 트렌드 10개 추출
trendList = tw_trends.getAPITrends(twitter, woeid)
# 결과 확인
for trend in trendList:
    print(trend)

# 키워드당 100개씩의 tweet 추출
tweetListList = []
for trend in trendList:
    tweetList = tw_search.getTweets(twitter, trend)
    tweetListList.append(tweetList)

# 결과 확인
for tweetList in tweetListList:
    for tweet in tweetList:
        print(tweet)


