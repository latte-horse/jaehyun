# -*- coding: utf-8 -*-
#removeRules.py

import re
from bs4 import BeautifulSoup

#--------------------------------------------------------------------------
# 사이트별 개별 전처리 함수 들을 리스트 형태로 반환하는 함수
#--------------------------------------------------------------------------
def getSiteRuleFuncs():
    return  [
        asiaToday,
    ]


#--------------------------------------------------------------------------
# soup의 특정 tag에 특정 target string이 포함될 경우 삭제해주는
#--------------------------------------------------------------------------
def soupRemover(soup, tag, target):
    for elem in soup.findAll(tag):
        if re.compile(target).search(elem.text): 
            elem.string = ""


#--------------------------------------------------------------------------
# 모든 과정이 끝난 후 text 형태로 된 문서에서 특정 문자열들을 삭제하는 함수
#--------------------------------------------------------------------------
def commonTextRemover(soup):

    # text = list(map(lambda line : str(line), soup.contents))
    text = soup.text.strip()
    # 개행으로 한 줄 씩 분리
    text = text.split("\n")
    # 좌우 공백 제거
    text = list(map(lambda line : line.strip(), text))
    # 특문 한 글자 라인 제거
    text = list(map(lambda line : re.sub(r"^(\||!|@|#|\$|%|\^|&|\*|\(|\)|-|\+|;|:)$", "", line), text))
    # 이메일 제거
    text = list(map(lambda line : re.sub(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", "", line), text))
    # 빈 행 제거
    text = list(filter(lambda line : line != "\n" and line != "", text))
    
    text = "\n".join(text)

    return text


#--------------------------------------------------------------------------
# 사이트별 제거 함수들
#--------------------------------------------------------------------------
# 아시아투데이
def asiaToday(soup):
    # 인기 뉴스 제목 등 제거
    [s.extract() for s in soup.select(".breaking_dump_list, noscript, .hot_news_box")]
    [s.extract() for s in soup.select(".header_main_box, #navi_first, span.wr_day")]
    [s.extract() for s in soup.select("p.byline_wrap, td.hidephotocaption")]

    soupRemover(soup, 'p', '모바일 넘버원 아시아투데이')
    soupRemover(soup, 'p', '이슈 & 뉴스')
    soupRemover(soup, 'h5', '기사 의견쓰기')
    
    return soup