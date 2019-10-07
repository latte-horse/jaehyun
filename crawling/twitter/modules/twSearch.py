#!/usr/bin/python
#twTrends.py

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