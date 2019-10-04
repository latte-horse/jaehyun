# app.py

from khaiii import KhaiiiApi

api = KhaiiiApi()

filename = "5.txt"
f = open("./data/" + filename, 'r')
strList = []
while True:
    line = f.readline()

    if not line: break
    if line == "\n": continue

    print(line)
    for word in api.analyze(line):
        strList.append("{0}".format(word))
f.close()

f = open("./output/Khaiii_{0}".format(filename), "w")
for string in strList:
    f.writelines(string+"\n")
f.close()

print("Done.")
