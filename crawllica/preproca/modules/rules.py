# -*- coding: utf-8 -*-
#rules.py

import re
from bs4 import BeautifulSoup

#------------------------------------------------------------------------------
# 사이트별 개별 전처리 함수 들을 리스트 형태로 반환하는 함수
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
        li = re.sub(r"^-?\s?Copy.*금지\s?-?\s?$", "", li)

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
    # MAGIC
    "*[itemprop='articleBody']",
    # TOMATO 뉴스
    "article div.rn_scontent section div.rns_text",
    # The Viewers
    "form#form1 div.sub-container div.cont-article-top div.cont-area",
    # 경인일보
    "div.bm_view div.view_left div#font.view_txt"
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
                div[style*='z-index:0'] "
        ])):

        skip = True;
        break
                
    return ("unknown", soup) if not skip else ("blacklist", soup)

#------------------------------------------------------------------------------
# 모듈 테스트 코드
#------------------------------------------------------------------------------
if __name__ == "__main__":
    # # fp_src = open("C:\\harvesta_output\\191012\\1150\\D_K_01\\D_28.txt", 
    # #     "r", encoding="utf-8")
    # # text = fp_src.read()
    # fp_src.close()
    text = "<p>첫 줄</p>\n<p>둘째 줄</p>\n<p>셋째 줄</p>"
    text = re.sub(r"</p>", "\n</p>", text)
    print(text)

    soup = BeautifulSoup(text, "html.parser")
