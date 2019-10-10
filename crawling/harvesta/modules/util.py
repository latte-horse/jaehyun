# -*- coding: utf-8 -*-
#util.py

def insertDFRow(df, keyword_source, keywords, i, news_source, news_list):
    for j, news in enumerate(news_list):
        df.loc[len(df.index)] = [keyword_source, keywords, i, news_source, j, news['title'], news['link']]

        
