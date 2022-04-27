'''
Date: 2022-04-26 09:04:38
LastEditors: Chaoyang.Tang
LastEditTime: 2022-04-27 03:50:20
FilePath: /CSIT6000P/test.py
'''
from model.MBR import MBR
test = [11,2,3,4,5]

print(test[0:2])
print(test[2:5])

obj = MBR()
test = { 'test':1,'atest5':5, "test2": 2, obj: 100}
print(test)
sort_test = sorted(test.items(), key = lambda kv:(kv[1], kv[0]))
target = sort_test.pop()
print(test.pop(target[0]))
print(list(test.keys()))


# points = [[3,4],[1,2],[5,7],[0,8]]

# points = RTree.mergeSort(points)
# print(points)