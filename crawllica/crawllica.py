#!/usr/bin/python
#crawllica.py

from harvesta import harvesta
from preproca import preproca
import platform
import sys
import subprocess


#------------------------------------------------------------------------------
# MAIN driver code
#------------------------------------------------------------------------------
if __name__ == "__main__":
    #-------------------------------
    # 윈도우에서는 테스트만 돌림
    #-------------------------------
    if platform.system() == "Windows":
        # outPath = "C:\\crawllica_output\\191016\\1710"
        outPath = harvesta.harvest("c:\\crawllica_output")
        doPreproc(outPath)

    
    #--------------------------------
    # 실제 리눅스 실행 환경
    #--------------------------------
    else:
        # 아규먼트 체크
        if len(sys.argv) < 2:
            print("usage: crawllica [output-root path]")
            exit(1)
        
        #----------------------------
        # 수집 / 전처리
        #----------------------------
        # harvesta 실행
        outPath = harvesta.harvest(sys.argv[1])
        # proproca 실행
        preproca.preproc(outPath)

        #----------------------------
        # 분석 -> analyza.py 실행
        #----------------------------
        # outPath = "../data/191020/2200"
        p = subprocess.Popen(["../analyza/analyza.py", outPath])
        p.wait()
        print("모든 작업 완료")

        
