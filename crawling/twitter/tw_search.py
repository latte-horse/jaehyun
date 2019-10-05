#!/usr/bin/env python
#tw-trends.py

#
# 키워드를 받아 검색하여 100개의 tweet 내용을 list로 반환하는 함수
#
def getTweets(twitter, keyword):
    tweetList = []
    query = twitter.search.tweets(q = keyword, count = 100)
    #print("Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"]))
    for result in query["statuses"]:
        tweetList.append(result["text"])

    return tweetList