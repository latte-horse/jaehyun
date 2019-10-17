from gensim.models import Word2Vec
import gensim
import pandas as pd
import sys

#######################모델 불러오기!
model1 = Word2Vec.load("model1")
#model11 = Word2Vec.load("model11")
#model2 = Word2Vec.load("model2")
#model21 = Word2Vec.load("model21")



####################### 키워드 넣어 검색!
result1 = model1.most_similar(['노조'], topn = 20)
#result2 = model11.most_similar(['노조'], topn = 20)
#result3 = model2.most_similar(['노조'], topn = 20)
#result4 = model21.most_similar(['노조'], topn = 20)



#######################관련 키워드 20개 뽑기 함수
def keylist(result):
    kolist = []
    for i in range(20):
        kolist.append(result[i][0])
    return kolist
###################### 진한이가 준 키워드...넣어봤찌만 슬프게도 오류가 뜬다.
jin = ['파업' , '운행' , '지하철' , '서울교통공사' , '16' , '노조' , '1' , '선' , '서울' ,
       '예고' , '총파업' , '8' , '14' , '열차' , '요구' , '18' , '오전' , '돌입' , '서울시' , '노동조합' ]


######################각각 키워드(20)별 유사도 표 그리기 함수
def MakeResult(modelkeylist,modelname):
    #행, 열 이름 설정
    df = pd.DataFrame(columns = modelkeylist , index = modelkeylist)
    
    for i in modelkeylist:
        listr = []
        for j in modelkeylist:
            
            listr.append(1 - modelname.similarity(i,j))
        #열 추가! 이렇게 해야 행렬 안에 깔끔~히 들어간다.   
        df[i] =listr
    
    return df


##################### 함수 실행과 함께 print!
sys.stdout = open('./result.txt' , 'w')

a = MakeResult(keylist(result1) , model1)
#b = MakeResult(keylist(result2) , model11)
#c = MakeResult(keylist(result3) , model2)
#d = MakeResult(keylist(result4) , model21)
#e = MakeResult(jin , model1)
print(keylist(result1))
print(a)

#print(keylist(result2))
#print(b)
#print(keylist(result3))
#print(c)
#print(keylist(result4))
#print(d)
#print(jin)
#print(e)
sys.stdout.close()

a.to_csv("a.csv" , mode = 'w' , encoding = 'ms949')
#b.to_csv("b.csv" , mode = 'w' , encoding = 'ms949')
#c.to_csv("c.csv" , mode = 'w' , encoding = 'ms949')
#d.to_csv("d.csv" , mode = 'w' , encoding = 'ms949')

#####################