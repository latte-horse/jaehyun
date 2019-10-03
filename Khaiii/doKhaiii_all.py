#!/usr/bin/python

# doKhaiii.py

import sys
import re
from khaiii import KhaiiiApi

api = KhaiiiApi()

# 전달 인자 읽기 및 파일 패스 생성
if len(sys.argv) < 3:
    print("usage: doKahiii [input file to process] [output file]")
    exit(1)

inputPath = sys.argv[1]
outputPath = sys.argv[2]

# 입력 파일 읽기 및 기본 형태소 분석 수행
f = open(inputPath, "r", encoding='utf-8-sig')
strList = []
while True:
    line = f.readline()

    if not line: break
    if line == "\n": continue

    # 나중에 고도화 및 모듈화 해야할 곳
    ##############################################################
    #형태소 분석 전 전처리 작업 (형태소 분석에 악영향을 주는 기호 삭제)
    line = line.replace("'", "").replace('"', "").replace("‘", "").replace("’", "").replace("“", "").replace('”', "")
    ##############################################################

    for word in api.analyze(line):
        strList.append("{0}".format(word))
f.close()

# 테스트용으로 기본 형태소 분석 결과 파일로 출력(최종결과 비교 분석용; 개발시에만 필요)
f = open(outputPath + ".input", "w")
for string in strList:
    f.writelines(string+"\n")
f.close()

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
        if splited[0] != "" and \
        splited[1][0] != "J" and \
        splited[1] != "SF" and \
        splited[1] != "SE" and \
        splited[1] != "VCP" and \
        splited[1] != "EP" and \
        splited[1] != "EF":
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

# 개발시 편의상 stdout 에 출력
for unit in unitList:
    print(unit)

# 결과 파일로 출력
f = open(outputPath, "w")
for unit in unitList:
    f.writelines(unit + "\n")
f.close()