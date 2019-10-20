#!/usr/bin/python
#analyza.py

from gensim.models import Word2Vec
from modules import util
from modules import morpheus
from modules import tfidf
import pandas



#------------------------------------------------------------------------------
#  word2vec
#------------------------------------------------------------------------------
def do_edit_test(path):
    # 문서 파일 리스트 생성
    filelist = util.get_filelist(path)

    # 코모란으로 토크나이즈드 문장들 생성
    # sentences = morpheus.sentences_komoran(filelist)
    # sentences = morpheus.sentences_twitter(filelist)
    # sentences = morpheus.sentences_split(filelist)
    sentences = morpheus.sentences_khaiii(filelist)
    # print(sentences)
    

    # model = Word2Vec(lines, 
    #     size=100, window = 2, min_count=30, workers=4, iter=100, sg=1)
    model1 = Word2Vec(
        sentences=sentences, 
        size=100, window = 5, 
        min_count=round(len(filelist)/2), 
        workers=4, iter=100, 
        sg=0,
        hs=0,   
        # negative=20,
        seed = 777
    )
    model2 = Word2Vec(
        sentences=sentences, 
        size=100, window = 5, 
        min_count=round(len(filelist)/2), 
        workers=4, iter=100, 
        sg=0,
        hs=1,
        # negative=5
        seed = 777
    )


    wv1 = model1.wv
    wv2 = model2.wv
    del(model1)
    del(model2)
    

    vocs1 = []
    for key in wv1.vocab:
        vocs1.append(key)
    vocs2 = []
    for key in wv2.vocab:
        vocs2.append(key)
    
    df1 =  pandas.DataFrame(columns = vocs1 , index = vocs1)
    for i in vocs1:
        dists = []
        for j in vocs1:
            dists.append(wv1.similarity(i, j))
        df1[i] = dists
    df2 =  pandas.DataFrame(columns = vocs2 , index = vocs2)
    for i in vocs2:
        dists = []
        for j in vocs2:
            dists.append(wv2.similarity(i, j))
        df2[i] = dists

    # 분석을 위해 임시 저장
    df1.to_csv("d-matrix1.csv", encoding="utf-8")
    df2.to_csv("d-matrix2.csv", encoding="utf-8")

    # for voc in vocs:
    #     print(voc, "\t", sum(df.loc[voc]))

    sumList1 = []
    for voc in vocs1:
        sumList1.append((voc, sum(df1.loc[voc])))
    sumList2 = []
    for voc in vocs2:
        sumList2.append((voc, sum(df2.loc[voc])))

    sumList1.sort(key=lambda x: abs(x[1]), reverse=True)
    sumList2.sort(key=lambda x: abs(x[1]), reverse=True)
 

    for i in range(len(sumList1)):
        # print(sumList1[i])
        print("{}\t{}".format(sumList1[i], sumList2[i]))




#------------------------------------------------------------------------------
#  word2vec을 이용하여 sigwords로 구성된 디스턴스 매트릭스를 생성
#------------------------------------------------------------------------------
def create_distance_df(path, sigwords):
    # 문서 파일 리스트 생성
    filelist = util.get_filelist(path)

    # khaiii로 모든 문서의 토크나이즈드된 문장 리스트 생성
    sents = morpheus.sentences_khaiii(filelist)

    # word2vec으로 단어 벡터들 생성
    model = Word2Vec(
        sentences=sents, 
        size=100, window = 5, 
        min_count=round(len(filelist)/3), 
        workers=4, iter=100, 
        sg=1,
        # hs=1,   
        negative=10,
        seed = 777
    )

    wv = model.wv
    del(model)

    # 전달받은 sigwords 중 model에 포함된 단어를 우선순위 순서로 추려냄
    sigvocs = []
    missvocs = []
    hit = 0
    miss = 0
    for worddic in sigwords:
        try:
            word = worddic['word']
            if wv.vocab[word]:
                sigvocs.append(word)
                hit += 1
            if hit >= 20:
                break
        except:
            missvocs.append(word)
            miss += 1
    # 디버깅용. 추후 삭제.
    print("missed: %d"  % miss)
    for voc in missvocs:
        print(voc)
    

    # 디스턴스 매트릭스를 데이터프레임 형태로 만듦
    distDF =  pandas.DataFrame(columns = sigvocs , index = sigvocs)
    for i in sigvocs:
        dists = []
        for j in sigvocs:
            dist = wv.distance(i, j)
            dists.append(0 if dist < 1.0e-2 else dist)
        distDF[i] = dists
    # 분석을 위해 임시 저장
    distDF.to_csv("d-matrix.csv", encoding="utf-8-sig")

    return distDF


        

#------------------------------------------------------------------------------
#  TF-IDF 의 Term Frequency 를 이용하여 중요 키워드를 내림차순으로 반환
#------------------------------------------------------------------------------
def get_sigwords_by_tf(path, searchword):
    # 검색어를 중요 단어로 인식
    verySigWords = searchword.split(" ")

    # 문서 파일 리스트 생성
    filelist = util.get_filelist(path)

    # 전체 문서 합치기 (개행으로 개별 doc 구분)
    docs = tfidf.get_docs(filelist)

    # 개별 doc 정보 가져오기 [{doc_id: , doc_length: }, ...]
    docInfos = tfidf.get_infos(docs)

    # 빈도수사전 dict list 생성
    freqDictList = tfidf.create_freq_dict(docs)

    # TF 계산
    tfScores = tfidf.compute_tf(docInfos, freqDictList)

    # word를 unique key로 만들어 TF 값을 합산
    mergScores = tfidf.compute_merged_score(tfScores, 'TF_score', verySigWords)

    return mergScores
    
    # # TF-IDF는 이론상으로도, 테스트 상으로도 우리 용도엔 맞지 않아 적용하지 않음
    # # (코드는 완성됨)
    # # IDF 계산
    # idfScores = tfidf.compute_idf(docInfos, freqDictList)

    # # TF-IDF 계산
    # tfidfScores = tfidf.compute_tfidf(tfScores, idfScores)

    
    
#------------------------------------------------------------------------------
#  main
#------------------------------------------------------------------------------
if __name__ == "__main__":

    path = "data/1630/D_K_01"

    # 검색어 추출하기
    searchword = util.get_searchword(path)

    # 대표 키워드 리스트 생성
    sigwords = get_sigwords_by_tf(path, searchword)

    # 디스턴스 매트릭스 생성
    distDF = create_distance_df(path, sigwords)

    


   





    

    