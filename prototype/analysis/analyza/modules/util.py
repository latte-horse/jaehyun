#util.py

from konlpy.tag import Komoran
import re


def getlines(filelist):
    komoran = Komoran()
    lines = []
    for i, file in enumerate(filelist):
        with open(file, 'r', encoding='utf-8') as fp:
            while True:
                try:
                    line = fp.readline()
                    if not line: 
                        break

                    line = re.sub("\xa0", " ", line).strip()
                    if line == "" : 
                        continue

                    tokens = komoran.nouns(line)
                    if len(tokens) == 0: 
                        continue

                    lines.append(komoran.nouns(line))

                except Exception as e:
                    print(e)
                    continue
    return lines