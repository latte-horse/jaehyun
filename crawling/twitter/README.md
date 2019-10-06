# 트위터 크롤링 코드

트위터에서 실시간 트렌드 10개를 뽑고 이를 이용하여 키워드당 100개씩의 트윗을 수집하는 코드.

## 실행 방법

모든 소스를 다운 받고 `tw_crawling.py`를 실행시키면 된다.  단 `config.py`는 개인 키 정보가 기록되어 있어 목록에 빠져있다. 아래와 같이 `config.py`를 작성해 주어야 한다.

```python
#config.py

#--------------------------------------------------------------------------------
# These tokens are needed for user authentication.
# Credentials can be generated via Twitter's Application Management:
#	https://developer.twitter.com
#--------------------------------------------------------------------------------

consumer_key = "FILLME"
consumer_secret = "FILLME"
access_key = "FILLME"
access_secret = "FILLME"
```

## 소스 구성

- `tw_crawling.py` : 메인 코드

- `tw_woeid.py` : 지역명을 기반으로 location code를 반환해 주는 코드
- `tw_trends.py` : 트위터 실시간 인기 트렌드 10개를 반환해 주는 코드
- `tw_search.py` : 입력된 키워드를 바탕으로 100개의 트윗을 반환해 주는 코드

## 참조 목록

- https://github.com/ideoforms/python-twitter-examples
