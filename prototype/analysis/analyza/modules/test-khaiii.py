#!/usr/bin/python

import util
from khaiii import KhaiiiApi
import re


path = "../data/1630/D_K_03"
filelist = util.get_filelist(path)


file = filelist[0]

with open(file, 'r', encoding='utf-8') as fp:
    khaiii = KhaiiiApi()
    strList = []
    while True:
        line = fp.readline()

        if not line: 
            break

        if line == "\n": 
            continue

        # 전처리 잘못 된 부분이 있어서 임시로 넣음. 추후 빼도 무관.
        line = re.sub("\xa0", " ", line).strip()
        if line == "" : 
                continue

         # 나중에 고도화 및 모듈화 해야할 곳
        ##############################################################
        #형태소 분석 전 전처리 작업 (형태소 분석에 악영향을 주는 기호 삭제)
        line = line.replace("'", "").replace('"', "").replace("‘", "") \
            .replace("’", "").replace("“", "").replace('”', "").replace \
            ('·', " ")
        words = khaiii.analyze(line)
        for word in words:
            # print(word)
            strList.append("{0}".format(word))

# 나중에 고도화 및 모듈화 해야할 곳
#############################################################################
# unit(의미 있는 어절 단위; 자체정의)
# unit 을 담을 unitList 생성 및 unit parsing 작업 시작
unitList = []
for i, line in enumerate(strList):
    morpParcelList = line.split("\t")[1].replace(
    '"', '').replace("'", "").split(" + ")

    morpMetaList = []
    for elem in morpParcelList:
        splited = elem.split("/")
        if \
            splited[0] != "" and \
            splited[1] != "NP" and \
            splited[1] != "NR" and \
            ( 
                splited[1][0] == "N" or \
                splited[1][0] == "S" or \
                splited[1] == "XSN"
            ):
            morpMetaList.append(splited)

    # 1글자인 경우 일반명사, 고유명사, 외래어만 셋 중 하나가 아닐 경우 스킵
    if len(morpMetaList) == 1 and len(morpMetaList[0][0]) == 1 :
        type = morpMetaList[0][1]
        if type != "NNG" and type != "NNP" and type != "SL" :  continue

    # 기타 일반적인 상황인 경우 계속 수행
    unit = ""
    for elem in morpMetaList:
        unit += elem[0]

    # 결과에서 의미없는 특문 제거
    unit = re.sub('([,.]$)|(^[,.])', '', unit)

    # 최종적으로 () [] 등으로 구분하여 나눈 후 각각 추가
    unitSplit = re.split("[\(\)\[\]\{\} ]", unit)
    for i, elem in enumerate(unitSplit) :
        unitSplit[i] = elem.strip()
    
    if len(unitSplit) > 1 :
        for elem in unitSplit :
            if len(elem) > 0 : unitList.append(elem) 
    else :
        if len(unitSplit[0]) > 0 :
            unitList.append(unitSplit[0])
    

    # 마지막으로 놓친 부분을 한 번 더 검증
    for unit in unitList :
        if re.match(r"[!@#$%^&*():;\[\]\{\}]", unit) != None :
            unitList.remove(unit)
    
#############################################################################

for unit in unitList :
    print(unit, end="\t")
print("")
