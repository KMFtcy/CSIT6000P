'''
Date: 2022-04-26 09:04:38
LastEditors: Chaoyang.Tang
LastEditTime: 2022-04-27 16:06:39
FilePath: /CSIT6000P/test.py
'''
from model.MBR import MBR
from model.Point import Point

point1 = Point(index=[0,0])
point2 = Point(index=[3,4])
print(Point.distance(point1,point2))

target = [1,3,5]
test = [2,3,5,6,7,8,9,10]

m = 1
for i in range(len(test)):
    if test[i] < m:
        continue
    test.insert(i,m)
    test.pop()
    break
print(test)



obj = MBR()
test = { 'test':1,'atest5':5, "test2": 2, obj: 100}
print(test)
sort_test = sorted(test.items(), key = lambda kv:(kv[1], kv[0]))
target = sort_test.pop()
print(test.pop(target[0]))
print(sort_test)
print(list(test.keys()))

# if k length buffer is full prune
# if len(result) >= k:
#     # rule 1
#     prune_list = []
#     for i in range(len(ABL)):
#         for j in range(i+1,len(ABL)):
#             i_statis_obj = list(ABL[i].values())[0]
#             j_statis_obj = list(ABL[j].values())[0]
#             if i_statis_obj["mindist"] > j_statis_obj["minmaxdist"]:
#                 prune_list.append(j)
#             elif j_statis_obj["mindist"] > i_statis_obj["minmaxdist"]:
#                 prune_list.append(i)
#                 break # i is no longer qualified break
#     prune_list = list(set(prune_list))
#     prune_list = sorted(prune_list)
#     for i in range(len(prune_list)):
#         ABL.pop(prune_list[i]-i)
    # rule 2
