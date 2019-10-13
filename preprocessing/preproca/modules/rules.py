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
        ytnnews,
        joinscom,
        nocutnews,
        metroseoul,
        sbsnews,
        asiatoday,
        kndaily,
        opinionnews,
        kookje,
        wowtv,
        thefact,
        polinews,
        econovil,
        bbsicokr,
        kukinews,
        heraldcorp,
        upinews,
        kbsnews,
        viva100,
        yonhapnewstv,
        edaily,
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

    # ------------------------------------
    # 패턴 △ ▲
    # ------------------------------------
    # 공백 패턴
    text = re.sub(r"([^\S\t\n\r]|&nbsp;){2,}", " ", text)
    # 기레기 패턴
    text = re.sub(r"\[.*\=.*기자\]", "", text)
    text = re.sub("".join([
            r"(\s|&nbsp;|\(|\[])*.{2,4}(\s|&nbsp;)*(기자|기상캐스터)",
            r"(\s|&nbsp;|\)|\]|\n)*"]), "\n", text)
    # 뉴스 패턴
    text = re.sub(r"\[.{0,10}\s*(뉴스|일보)\]", "", text)
    # 메뉴 패턴
    text = re.sub(r"(>(\s|&nbsp;)*)*", "", text)
    text = re.sub(r"(\|(\s|&nbsp;)*)*", "", text)
    # 기사 정보 패턴
    text = re.sub(r"최종수정.*[0-9]", "", text)
    text = re.sub("".join([
            r"(기사)?(입력|수정|승인|송고|Posted)(시간)?(\s|&nbsp;)*:?",
            r"(\s|&nbsp;)*([0-9]|/|\.|-)*(\s|&nbsp;)*([0-9]|:)*"]), "", text)
    # 사진 패턴
    text = re.sub(r"/.{0,10}(\s|&nbsp;)?뉴스", "", text)
    # 기타 패턴
    text = re.sub(r"^여백", "", text)

    #------------------------------------
    # 콕 찍어
    #------------------------------------
    text = re.sub(r"\(?사진(\s|&nbsp;|=)*연합뉴스\)?", "", text)
    text = re.sub(r"\*?자료제공(\s|&nbsp;)*천문우주지식포털", "", text)
    text = re.sub(r"\[헤럴드경제\]", "", text)
    text = re.sub(r"출처=뉴시스", "", text)
    text = re.sub(r"사회적 책임 이끄는 전문미디어", "", text)
    
    #------------------------------------
    # 줄 단위 처리가 편리한 경우
    #------------------------------------
    # 개행으로 한 줄 씩 분리
    text = text.split("\n")
    # text = re.compile(r"(\n|<br/?>)").split(text)
    # 좌우 공백 제거
    text = list(map(lambda line : line.strip(), text))
    # # 특문 만 있는 라인 제거
    text = list(map(lambda line : re.sub("".join([
            r"^(\||!|@|#|\$|%|\^|&|\*|\(|\)|-|\+|;|:|/|ㆍ|▶|\n|\s|&nbsp;)+",
            r"$"]), "", line), text))
    # # 이메일 제거
    text = list(map(lambda line : re.sub(
            r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", "", 
            line), text))
    # 숫자만 있는 행 제거
    text = list(filter(lambda line : not re.compile(r"^[0-9]*$").match(line), 
            text))
    # 날짜만 있는 행
    text = list(filter(lambda line : not re.compile(
        r"^([0-9]|\.|-|/)+\s?(\(.{1}\))?\s?$").match(line), text))
    # 저작권
    text = list(filter(lambda line : not re.compile(
        r"^.?(저작권|(c|C)opyright).*금(지|합니다).?$").match(line), text))
    text = list(filter(lambda line : not re.compile(
        r"^.?ⓒ(.|\s)*금지.?$").match(line), text))
    # 엡데이트
    text = list(filter(lambda line : not re.compile(
        r"^(UPDATE).*[0-9].?$").match(line), text))
    # 빈 행 한 번 제거
    text = list(filter(lambda line : line != "\n" and line != "", text))
    #------------------------------------
    # map filter 보다 이게 낫겠는데...
    #------------------------------------
    newText = []
    for line in text:
        line = re.sub(r"^.{0,10}\s?뉴스\s?(/)?\s*$", "", line)
        line = re.sub(r"^.?끝.?$", "", line)
        line = "" if re.compile(r"^연합뉴스TV 기사").search(line) else line
        line = line.strip()
        if line != "":
            newText.append(line)

    #------------------------------------
    # 다시 텍스트로 합치기
    #------------------------------------
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
    # rm_by_text(soup, 'p', "및 재배포")
    rm_by_text_exact(soup, 'div',r"^(상단|하단|중간)?\s?여백")
    rm_by_text_exact(soup, 'p',
        "".join([r"^.{2,4}(\s|&nbsp;)?기자(\s|&nbsp;)?\(?([a-zA-Z0-9_.+-]+", 
        r"@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)(\s|&nbsp;)?\)?"]))
    rm_by_text_exact(soup, 'li', r"^([0-9]|\.|-|/)+\s?(\(.{1}\))?\s?$")

    return soup

# SBS 뉴스
def ytnnews(soup):
    for s in soup.select(" \
            div#YTN_main_2017 div.header, div#zone1 div.cate, \
            p.copyright_bottom"
        ):
        s.extract()
    return soup

# 중앙일보
def joinscom(soup):
    for s in soup.select(" \
        #layer_jmnet, div#sub div[class*=rts], div#divJpodEpisode~*, \
        #aside #wide_trend, div#widget_sponsored_div~*, \
        div#widget_sponsored_div, span.byline em"
        ):
        s.extract()
    rm_by_text(soup, 'strong', "지면보다 빠른 뉴스")
    rm_by_text(soup, 'p', "디지털에서만 만날 수 있는 중앙일보 뉴스")
    return soup

# 노컷뉴스
def nocutnews(soup):
    for s in soup.select(" \
            div#pnlRightArea, #divRecommend, #divTimeNews, div.toastnews, \
            div.con_section2 div.sect h3, div.h_info div.sub_group2, \
            div.h_info ul.bl_b, div.view_gnb, div.allmenu, #divSubCategory"
        ):
        s.extract()
    return soup

# 메트로신문
def metroseoul(soup):
    for s in soup.select(" \
            div#header-menu, div.menu_box2 li div.sec, div#news_writer, \
            div#content-body div.default-box div.body-right-box, \
            div#copyright, div.newsofTopicTitle, div.topicPlusTitle, \
            div.today_metronews"
        ):
        s.extract()
    return soup

# SBS 뉴스
def sbsnews(soup):
    for s in soup.select(" \
            div.w_navigation, div.layer_gnb, div.w_article_title \
            div.info_area, \
            div.w_article_title div.control_area, div.article_relation_area, \
            div.w_article_cont div.w_article_side, div.w_footer, div.sns_list"
        ):
        s.extract()
    return soup

# 아시아투데이
def asiatoday(soup):
    for s in soup.select(" \
            .breaking_dump_list, noscript, .hot_news_box, .header_main_box, \
            #navi_first, span.wr_day, p.byline_wrap, td.hidephotocaption"
        ):
        s.extract() 
    rm_by_text(soup, 'p', '모바일 넘버원 아시아투데이')
    rm_by_text(soup, 'p', '이슈 & 뉴스')
    rm_by_text(soup, 'h5', '기사 의견쓰기')
    return soup

# 경남데일리
def kndaily(soup):
    for s in soup.select(" \
            div.mHeight_B, div#head-info, div#footer-wrap, div#article-reply, \
            div#side-scroll-start, div.reply-write-footer, div.reply-msg, \
            div.article-hotnews"
        ):
        s.extract()
    
    return soup

# 오피니언뉴스
def opinionnews(soup):
    for s in soup.select(" \
            section.article-head-info, aside.user-aside, div.aht-control, \
            div.tag-group, div.view-copyright, article#reply, div.reveal"
        ):
        s.extract()
    return soup

# 국제신문
def kookje(soup):
    for s in soup.select(" \
            div#header, div.news_reporterDate, div.news_snsPrint, \
            td.imgcaption, div#topArea div.rightArea"
        ):
        s.extract()
    return soup

# 한국경제TV
def wowtv(soup):
    for s in soup.select(" \
            div#divPrintPopup, div.location-page, div.box-util-button, \
            div.article-repoter-infor, div.box-section-emotion, \
            div.box-section-emotion~*, div.wrap-right-adbox #divContentRight, \
            div.best-infor-news ~ div"
        ):
        # div.list-news-type01 h2.title02, div.quickMenu"
        s.extract()
    rm_by_text_exact(soup, 'strong', "서비스 상품")
    # rm_by_text(soup, 'h2', "인기 갤러리")
    return soup

# 더팩트
def thefact(soup):
    for s in soup.select(" \
            div.timeTxt, ul.topBtn"
        ):
        s.extract()
    return soup

# 폴리뉴스
def polinews(soup):
    for s in soup.select(" \
            div.top_nav, div.arv_003 div.jour_box, \
            div.theiaStickySidebar div.path_wrap, div.art_top ul.art_info"
        ):
        s.extract()
    rm_by_text(soup, 'p', "폴리뉴스=")
    return soup

# 이코노빌
def econovil(soup):
    for s in soup.select(" \
            td div.View_Info"
        ):
        s.extract()
    return soup

# BBS NEWS
def bbsicokr(soup):
    for s in soup.select(" \
            div.yesno-box, div.BoxDefault_34 strong span"
        ):
        s.extract()
    return soup

# 쿠키뉴스
def kukinews(soup):
    for s in soup.select(" \
            div.navi_v2, div.c011_arv div.util, div.c011_arv div.util2 li, \
            p.copyright, div.m01_arl50 li, div#footer_v2"
        ):
        s.extract()
    rm_by_text(soup, 'span', "SPONSORED")
    return soup

# 코리아헤럴드
def heraldcorp(soup):
    for s in soup.select(" \
            div.wrap div.header, div.ad_2 th, div.ad_161219 ~ div, \
            li.view_top_t2_cate ,div.view_bg div.con_right"
        ):
        s.extract()
    return soup

# UPI뉴스
def upinews(soup):
    for s in soup.select(" \
            div.viewTitle dl dd, div#viewConts>p, div#reply_wrap_btn, \
            div#main div#subCtsRight" 
        ):
        s.extract()
    return soup

# KBS 뉴스
def kbsnews(soup):
    for s in soup.select(" \
            div#content.c-view .blind, span.txt-info em,\
            div.related-articles ~ div, ul.detail-card-font li, \
            div.related-articles, div.detail-component.det-news ~ div" 
        ):
        s.extract()
    return soup

# 브릿지경제
def viva100(soup):
    for s in soup.select(" \
            p.view_top_nvi, div#container div.con_right, div.ads_bottom~div, \
            div[style*='display:none'], div#sitemap div.sitemap_box_news" 
        ):
        s.extract()
    return soup

# 연합뉴스TV
def yonhapnewstv(soup):
    for s in soup.select(" \
            div.article-head-wrap div.article-head div p.subTitle, \
            div.util div.modal, \
            div[itemprop='articleBody']~div"
        ):
        s.extract()
    return soup

# 이데일리
def edaily(soup):
    for s in soup.select(" \
            div.gnb_sub, div.dates ul li p, section#aside_right.aside_right,\
            section.aside_left div.article_newsetc, section#aside_bottom, \
            div#footers"
        ):
        s.extract()
    return soup

#------------------------------------------------------------------------------
# 모듈 테스트 코드
#------------------------------------------------------------------------------
if __name__ == "__main__":
    # # fp_src = open("C:\\harvesta_output\\191012\\1150\\D_K_01\\D_28.txt", 
    # #     "r", encoding="utf-8")
    # # text = fp_src.read()
    # fp_src.close()
    text = "<p>첫 줄</p>\n<p>둘째 줄</p>\n<p>셋쩨 줄</p>"
    text = re.sub(r"</p>", "\n</p>", text)
    print(text)

    soup = BeautifulSoup(text, "html.parser")
