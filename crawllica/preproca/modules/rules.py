# -*- coding: utf-8 -*-
#rules.py

import re
from bs4 import BeautifulSoup


#------------------------------------------------------------------------------
# 각각의 목표가 있는 전처리 함수 들을 리스트 형태로 반환하는 함수
#------------------------------------------------------------------------------
def get_rulefns():
    return  [
        common,
        whitelist,
        checkskip,
    ]


#------------------------------------------------------------------------------
# soup의 특정 tag에 특정 target string이 포함될 경우 삭제해주는 함수
#------------------------------------------------------------------------------
def rm_by_text(soup, tag, target):
    for elem in soup.findAll(tag):
        if re.compile(target).search(elem.text): 
            elem.string = ""

def rm_by_text_exact(soup, tag, target):
    for elem in soup.findAll(tag):
        if re.compile(target).match(elem.text): 
            elem.string = ""

#------------------------------------------------------------------------------
# 모든 과정이 끝난 후 text 형태로 된 문서에서 특정 문자열들을 삭제하는 함수 (마무리)
#------------------------------------------------------------------------------
def common_rm_text(text):
    text = text.strip()

    # # ------------------------------------
    # # 패턴 △ ▲
    # # ------------------------------------
    # # 공백 패턴
    # text = re.sub(r"([^\S\t\n\r]|&nbsp;){2,}", " ", text)
    # # 기레기 패턴
    # text = re.sub(r"\[.*\=.*기자\]", "", text)
    # text = re.sub("".join([
    #         r"(\s|&nbsp;|\(|\[])*.{2,4}(\s|&nbsp;)*(기자|기상캐스터)",
    #         r"(\s|&nbsp;|\)|\]|\n)*"]), "\n", text)
    # # 뉴스 패턴
    # text = re.sub(r"\[.{0,10}\s*(뉴스|일보)\]", "", text)
    # # 메뉴 패턴
    # text = re.sub(r"(>(\s|&nbsp;)*)*", "", text)
    # text = re.sub(r"(\|(\s|&nbsp;)*)*", "", text)
    # # 기사 정보 패턴
    # text = re.sub(r"최종수정.*[0-9]", "", text)
    # text = re.sub("".join([
    #         r"(기사)?(입력|수정|승인|송고|Posted)(시간)?(\s|&nbsp;)*:?",
    #         r"(\s|&nbsp;)*([0-9]|/|\.|-)*(\s|&nbsp;)*([0-9]|:)*"]), "", text)
    # # 사진 패턴
    # text = re.sub(r"/.{0,10}(\s|&nbsp;)?뉴스", "", text)
    # # 기타 패턴
    # text = re.sub(r"^여백", "", text)

    # #------------------------------------
    # # 콕 찍어
    # #------------------------------------
    # text = re.sub(r"\(?사진(\s|&nbsp;|=)*연합뉴스\)?", "", text)
    # text = re.sub(r"\*?자료제공(\s|&nbsp;)*천문우주지식포털", "", text)
    # text = re.sub(r"\[헤럴드경제\]", "", text)
    # text = re.sub(r"출처=뉴시스", "", text)
    # text = re.sub(r"사회적 책임 이끄는 전문미디어", "", text)
    
    # #------------------------------------
    # # 줄 단위 처리가 편리한 경우
    # #------------------------------------
    # # 개행으로 한 줄 씩 분리
    # text = text.split("\n")
    # # text = re.compile(r"(\n|<br/?>)").split(text)
    # # 좌우 공백 제거
    # text = list(map(lambda line : line.strip(), text))
    # # # 특문 만 있는 라인 제거
    # text = list(map(lambda line : re.sub("".join([
    #         r"^(\||!|@|#|\$|%|\^|&|\*|\(|\)|-|\+|;|:|/|ㆍ|▶|\n|\s|&nbsp;)+",
    #         r"$"]), "", line), text))
    # # # 이메일 제거
    # text = list(map(lambda line : re.sub(
    #         r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", "", 
    #         line), text))
    # # 숫자만 있는 행 제거
    # text = list(filter(lambda line : not re.compile(r"^[0-9]*$").match(line), 
    #         text))
    # # 날짜만 있는 행
    # text = list(filter(lambda line : not re.compile(
    #     r"^([0-9]|\.|-|/)+\s?(\(.{1}\))?\s?$").match(line), text))
    # # 저작권
    # text = list(filter(lambda line : not re.compile(
    #     r"^.?(저작권|(c|C)opyright).*금(지|합니다).?$").match(line), text))
    # text = list(filter(lambda line : not re.compile(
    #     r"^.?ⓒ(.|\s)*금지.?$").match(line), text))
    # # 엡데이트
    # text = list(filter(lambda line : not re.compile(
    #     r"^(UPDATE).*[0-9].?$").match(line), text))
    # # 빈 행 한 번 제거
    # text = list(filter(lambda line : line != "\n" and line != "", text))
    # #------------------------------------
    # # map filter 보다 이게 낫겠는데...
    # #------------------------------------
    # newText = []
    # for line in text:
    #     line = re.sub(r"^.{0,10}\s?뉴스\s?(/)?\s*$", "", line)
    #     line = re.sub(r"^.?끝.?$", "", line)
    #     line = "" if re.compile(r"^연합뉴스TV 기사").search(line) else line
    #     line = line.strip()
    #     if line != "":
    #         newText.append(line)

    # #------------------------------------
    # # 다시 텍스트로 합치기
    # #------------------------------------
    # text = "\n".join(text)

    # text = text.split("\n")
    # text = list(map(lambda line : line.strip(), text))
    #  # 빈 행 한 번 제거
    # text = list(filter(lambda line : line != "\n" and line != "", text))
    text = text.split("\n")
    newText = []
    for li in text:
        li = li.strip()
        if li == "": continue

        # 이메일
        li = re.sub(
            r"^([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$", "", li)
        li = re.sub(
            r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$", "", li)
        li = re.sub("".join([r"^\[?\s?.*([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+", 
            r"\.[a-zA-Z0-9-.]+)\s?\]?"]), "", li)
            

        # 뉴스 패턴
        li = re.sub(r"^뉴스엔\s+.*[a-zA-Z0-9_.+-]+@", "", li)
        li = re.sub(r"^기사제보.*(금지|자료)\s?$", "", li)
        li = re.sub(r"^<?\s?ⓒ.*금지\s?(＞|>)?\s?$", "", li)
        li = re.sub(r"^-?\s?(C|c)opy.*금지\s?-?\s?$", "", li)

        # 기레기 패턴
        li = re.sub(r"^.{0,15}기자\s?$", "", li)
        li = re.sub(r"^\[\s?.*기자\s?\]\s*", "", li)
        li = re.sub("".join([r"^.{0,10}기자.*" , 
            r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$"]), "", li)
        li = re.sub(r"^매경.*기자$", "", li)

        # 날짜 패턴
        li = re.sub("".join([r"(최종|기사)?(수정|입력)\s?:?\s?" , 
            r"(([0-9]{2,4})|(\.|/|-))+\s([0-9]{2}|:)*"]), "", li)
        li = re.sub(r"^UPDATE(\s|[0-9]|\.|-|/|\[|\]|:)*$", "", li)
        
        # 콕 찍어
        li = re.sub(r"^관련기사$", "", li)
        li = re.sub(r"^포토뉴스$", "", li)
        li = re.sub(r"^놓칠 수 없는 한 컷!$", "", li)
        li = re.sub(r"^꼭 봐야 할 뉴스$", "", li)
        li = re.sub(r"^많이 본 뉴스$", "", li)
        li = re.sub(r"^포토뉴스$", "", li)
        li = "" if re.compile(r"^SPONSORED$").match(li.upper()) else li
        li = "" if re.compile(r"^HOT ISSUE NEWS$").match(
                li.upper()) else li
        li = "" if re.compile(r"^HOT PHOTO$").match(li.upper()) else li
        li = "" if re.compile(r"^GALLERY$").match(li.upper()) else li
        li = "" if re.compile(r"^BAR_PROGRESS$").match(li.upper()) else li
        li = re.sub(r"^티브이데일리.*kr$", "", li)
        li = re.sub(r"^더이상의.*다운받기$", "", li)
    
        # 의미 없는 패턴
        li = re.sub("".join([r"^(([0-9]+)|(!|@|#|\$|%|\^|&|\*|\(|\)|\-", 
            r"|\+|=))*$"]), "", li)
        li = "" if len(li) == 1 else li
        
        li = li.strip()
        if li != "": newText.append(li)

    text = "\n".join(newText)

    return text


#------------------------------------------------------------------------------
# 사이트별 제거 함수들
#------------------------------------------------------------------------------
# 공통
def common(soup):
    # 기본적인 태그 등 제거
    [s.extract() for s in soup.select(
        "script, a, style, nav, button, img, header, footer, #footer, \
            .footer, legend, noscript, label, .hide, .hidden, caption")]

    # 문자열 기준 제거
    # rm_by_text_exact(soup, 'div',r"^(상단|하단|중간)?\s?여백")
    # rm_by_text_exact(soup, 'p',
    #     "".join([r"^.{2,4}(\s|&nbsp;)?기자(\s|&nbsp;)?\(?([a-zA-Z0-9_.+-]+", 
    #     r"@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)(\s|&nbsp;)?\)?"]))
    # rm_by_text_exact(soup, 'li', r"^([0-9]|\.|-|/)+\s?(\(.{1}\))?\s?$")
    
    return ("unknown", soup)

# 화이트리스트 셀렉터 문자열들
_selectorList = [
    # DAUM
    "div#harmonyContainer.article_view",
    # NAVER
    "div#articeBody.article_body",
    # NAVER MAIN
    "div#wrap table td.content div#main_content \
        div#articleBody.article_body div#articleBodyContents",
    # MAGIC
    "*[itemprop='articleBody']",
    # TOMATO 뉴스
    "article div.rn_scontent section div.rns_text",
    # The Viewers
    "form#form1 div.sub-container div.cont-article-top div.cont-area",
    # 경인일보
    "div.bm_view div.view_left div#font.view_txt",
    # e뉴스페이퍼 
    "div.mw_basic_view_content div#view_436 div#view_content div#bo_v_con",
    # 스포츠투데이
    "div#wrap div#container div#content div.con_box div.view \
        div.view_article div#article",
    # 티브에데일리
    "table[align='center'] table table div#content div#_article table \
        div.read",
    # 국제신문
    "div#wrap div#Contents div#topArea div.leftArea div#news_textArea \
        div.news_article",
    # 뉴스투데이 news2day
    "div#contents div#main-section div#article-area div.article-view \
        div#news-contents",
    # 한국증권신문
    "div.off-canvas-wrapper div.off-canvas-wrapper-inner div#user-wrap \
        section#user-container div.float-center article.article-veiw-body",
    # 소비자가만드는신문
    "div.out_box div.ob_1 div#container div.container div div#content \
        div#arl_view_box div#arl_view_content.arl_view_content",
    # 쿠키뉴스
    "div.container_v2 div.section_h123_v2 div.section_h12_v2 \
        div.section_12_v2 div.c011_arv div#news_body_area",
    # 더 셀럽
    "div.container section div.cont_area div.left_cont \
        div.news_view_area div.view_news div.read div#CmAdContent",
    # 폴리뉴스
    "div.wrapper div.column div.f_left div.theiaStickySidebar \
        div.arv_001_01 div.news_body_area div#news_body_area",
    # 비욘드포스트
    "body[ondragstart='return false'] div.con div.wrap2.tp2 \
        div.wr2_lt div.v1d div.v1d_con div.vcon div.articleContent",
    # 채널예스
    "div#wrapCon div#conWrap div#conArea div#realCon div#articleView \
        div#articleCont div.txtBox",
    # 부산일보
    "div#wrap div#container div.inner div.article_view div.article_content",

    # 아시아타임즈 (태그가 깨져서 처리 안 됨)
    "div#wrap div.wrap div#main div#subCtsMain div#viewWrap \
        div#viewConts.viewConts"
]

# 화이트리스트 체크
def whitelist(soup):
    for selector in _selectorList:
        for s in soup.select(selector):
            return ("whitelist", s)
    return ("unknown", soup)

# 의도된 스킵 체크
def checkskip(soup):
    if soup.text.split("\n")[1] == "None":
         return ("blacklist", soup)

    skip = False;
    for s in soup.select("".join([
            # 미디어펜
            "div#HeadMenu div#Default_Warp div#MenuBar ul#mega-menu, ",
            # 더코리아뉴스
            "div#wrap div div#divMenu div table td \
                div[style*='z-index:0'], "
            # YTN 94.5
            "div#wrap div#gnb ul#topLink li.b ul li.YTN_CSA_outlink1, "
            # WIKI TREE
            "div.wrap div.multi-scroll-wrap div.multi-scroll-inner \
                div.scroll-zone01 div.scroll-start01 div.scroll-in01 \
                div.article_wrap div.article_byline span.time, "
            # 한국스포츠통신
            "body[onselectstart='return false'] div.off-canvas-wrapper \
                div.off-canvas-wrapper-inner \
                div#offCanvas.off-canvas.user-canvas.position-left,"
            # 남도일보
            "body > table td[align='center'] div.body-wrap-full \
                div.head-top div.body-wrap-basic div.edit-btn li.nobr"
        ])):

        skip = True;
        break
                
    return ("unknown", soup) if not skip else ("blacklist", soup)

#------------------------------------------------------------------------------
# 모듈 테스트 코드
#------------------------------------------------------------------------------
if __name__ == "__main__":
    None