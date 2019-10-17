from konlpy.tag import Komoran
import os
from gensim.models import Word2Vec
import tensorflow as tf
import gensim
import re

komoran = Komoran(userdic = './user_dic.txt')


##########################################절대경로 표시 
def allfiles(path):
    res = []

    for root, dirs, files in os.walk(path):
        rootpath = os.path.join(os.path.abspath(path), root)

        for file in files:
            filepath = os.path.join(rootpath, file)
            res.append(filepath)

    return res

result = allfiles("C:/바탕화면/SAMPLE~1")

koko1 = []
del koko1[:]


##함수 사용해서 폴더 속의 파일 모두 가져오기!

for filelist in result:
    try:
        doc = open(filelist , encoding = 'UTF8').read()


    #koko1.append(komoran.nouns(doc))
        testr =  komoran.nouns(doc)
        kkk = []
        for i in range(len(testr)):
            
            if(len(testr[i]) >= 2):
                kkk.append(testr[i])
        koko1.append(kkk)
    except Exception as e:
        print(e)

        #koko1.extend(komoran.nouns(doc)) extend는 안된다! 이유는 python은 글자를 배열로 인식해서 하나하나 짜겐다.
        #koko2.append(komoran.morphs(doc))
        #komoran 에 메소드 nouns(명사추출), morphs(형태소추출) tagset(품사설명 부착), pos(품사설명부착)

    



model1 = Word2Vec(koko1 , size = 200 ,  window = 2 , iter = 100 , sg = 1 , workers = 3 )
#model2 = Word2Vec(koko2, size = 200 ,  window = 2 , iter = 100 , sg = 1 , workers = 3 )
model11 = Word2Vec(koko1 , size = 200 ,  window = 2 , iter = 100 , sg = 0 , workers = 3)
#model21 = Word2Vec(koko2, size = 200 ,  window = 2 , iter = 100 , sg = 0 , workers = 3)
##########################################
#size =  한 단어당 몇 차원 벡터?
#window = 앞뒤 몇개의 단어와 비교?
#min_count = 최소 등장 회수 이하는 제외
#sg = CBOW(= 0) , skip-gram(= 1)




########################################### 키워드('노조')와 연관된 단어 모음 20개
# positive 관련높은 것 negative 관련 없는 것

kokoresult1 = model1.most_similar(positive = ["지하철파업"] ,  topn = 20 )
kokoresult11 = model11.most_similar(positive = ["지하철파업"] ,  topn = 20 )
#kokoresult2 = model11.most_similar(positive = ["지하철파업"] ,  topn = 20 )
#kokoresult21 = model21.most_similar(positive = ["1호선"] ,  topn = 20 )

print(kokoresult1)
print(kokoresult11)
#print(kokoresult2)
#print(kokoresult21)



########################################## 분석 모델 저장 장소
model1.save('model1')
model11.save('model11')
#model2.save('model2')
#model21.save('model21')

########################################## 저장한 모델 읽어서 이용
#model = gensim.models.Word2Vec.load('model')