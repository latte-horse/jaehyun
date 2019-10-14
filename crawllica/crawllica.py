# -*- coding: utf-8 -*-
#!/usr/bin/python
#crawllica.py

from harvesta import harvesta
from preproca import preproca

def doCrawlling(path):
    outPath = harvesta.harvest("path")
    print(outPath)
    return outPath

def  doPreproc(path):
    preproca.preproc(path)


if __name__ == "__main__":
    # outPath = doCrawlling("c:\\crawllica_output")

    outPath = "C:\\crawllica_output\\191014\\1320"
    doPreproc(outPath)
    