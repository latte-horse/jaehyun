


a = [1, 2, 3]
b = ['a', 'b', 'c', 'd', 'e']
c = ['가', '나', '다', '라']
d = [a, b, c]
e = tuple(d)




핫 = zip(*d)
for i in 핫:
    for j in i:
        print(j)
