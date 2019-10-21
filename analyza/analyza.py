#!/usr/bin/python
#analyza.py


import sys
import os
import json
import cx_Oracle
from modules import *


#------------------------------------------------------------------------------
#  MAIN driver code
#------------------------------------------------------------------------------
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Woops... Somthing went wrong...")
        print("[Usage]: analyza.py [source-dir path]")
        exit(1)
    path = sys.argv[1]
    path = path[:len(path)-1] if path[len(path)-1] == "/" else path
    dirlist = util.get_dirlist(path)

    searchWords = []
    visual_data = []
    # idx = 0
    for dir_ in dirlist:
        try:
            # 그룹 정보 생성(검색어 디렉토리 명 ex: D_K_01)
            group = dir_[dir_.rfind("/")+1:]

            # 검색어 추출하기
            searchword = util.get_searchword(dir_)
            
            # 로그
            print("분석 시작: {}\t{}".format(dir_, searchword))

            # 대표 키워드 리스트 생성
            (docs, sigwords) = tfidf.get_sigwords_by_tf(dir_, searchword)

            # 디스턴스 매트릭스 생성
            distDF = word2veca.create_distance_df(docs, sigwords, 20)

        except Exception as e:
            print(e)

        else:
            # exception 가능성이 있는 작업들이 모두 끝난 후에야
            # DATABASE에 넣을 자료들을 준비한다.

            searchWords.append({'key' : group, 'searchword' : searchword})

            # 시각화 정보 컬럼 데이터 만들기 json 형식
            nodes = []
            colnames = list(distDF.columns)
            for i, colname in enumerate(colnames):
                for word in sigwords:
                    if colname == word['word']:
                        nodes.append({
                            'group' : group,
                            'id' : group+"_"+("%02d"%(i+1)),
                            'word' : colname,
                            'val' : word['TF_score']
                        })
            visual_data.append({
                'nodes' : nodes,
                'dmatrix' : distDF.to_csv()
            })

        finally:
            None
            # 테스트 코드
            # idx += 1
            # if idx > 1: break


    #--------------------------------------------------------------------------
    # DATABASE 컬럼 데이터 생성
    #--------------------------------------------------------------------------
    divIdx = path.rfind("/")
    yymmdd = int(path[divIdx-6:divIdx])
    hhmm = int(path[divIdx+1:])
    searchword =  json.dumps(searchWords, ensure_ascii=False)
    visdata = json.dumps(visual_data, ensure_ascii=False)
    # 테스트 저장
    with open(os.path.join(path, "visdata.txt"), "w", encoding="utf-8-sig") \
    as fp:
        fp.write(visdata)

    #--------------------------------------------------------------------------
    #  Oracle Database에 Insert
    #--------------------------------------------------------------------------
    os.putenv('NLS_LANG', '.UTF8')
    con = cx_Oracle.connect(config.oracle_connection)
    cur = con.cursor()
    statement = "".join([
            "insert into latte_timeline(yymmdd, hhmm, searchword, visdata) ",
            "values (:1, :2, :3, :4)"])
    cur.execute(statement, (yymmdd, hhmm, searchword, visdata))
    cur.close()
    con.commit()
    con.close()

    # 입력 확인 테스트 코드
    con = cx_Oracle.connect(config.oracle_connection)
    cur = con.cursor()
    statement = "".join([
            "select * from latte_timeline where yymmdd = :1 and hhmm = :2"    
    ])
    cur.execute(statement, (yymmdd, hhmm))
    for row in cur:
        print(row)
    cur.close()
    con.close()


    # #----------------------------------------
    # # 개별 키워드 테스트 루틴 - 디버깅시 필요!
    # #----------------------------------------
    # path = "../../data/timeline/191017/1630/D_K_01/"
    # path = path[:len(path)-1] if path[len(path)-1] == "/" else path

    # # 검색어 추출하기
    # searchword = util.get_searchword(path)
    # print(searchword)

    # # 대표 키워드 리스트 생성
    # (docs, sigwords) = tfidf.get_sigwords_by_tf(path, searchword)

    # # 디스턴스 매트릭스 생성
    # distDF = word2veca.create_distance_df(docs, sigwords, 20)
    # print(distDF)
    # #----------------------------------------



    


   





    

    