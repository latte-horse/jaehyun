# 네이버 크롤링 코드

네이버에서 실시간 인기 검색어 10개를 뽑고 이를 이용하여 검색어당 30개씩의 뉴스 링크를 수집하는 코드.

## 실행 방법

모든 소스를 다운 받고 `naverCrawling.py`를 실행시키면 된다. 단 `config.py`는 개인 키 정보가 기록되어 있어 목록에 빠져있다. 아래와 같이 `config.py`를 작성해 주어야 한다.

***modules/config.py***

```python
#config.py

#--------------------------------------------------------------------------------
# NAVER Developpers
# https://developers.naver.com
#--------------------------------------------------------------------------------

clientID = "FILLME"
clientSecret = "FILLME"
```

## 소스 구성

- `naverCrawling.py` : 메인 코드
- `modules/__init__.py`
- ```modules/config.py``` : API KEY 설정
- `modules/naverFuncs.py` : NAVER API를 이용하는 핵심 모듈

## 참조 목록

- https://developers.naver.com/docs/search/blog/

