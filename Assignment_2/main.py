import sys,getopt
sys.path.append("..")
from model.RTree import RTree
from model.Point import Point
import load_dataset
import random
import matplotlib.pyplot as plt
import os
import queue
import time
import statistics

poi_dataset_lines = load_dataset.load()
poi_dataset = []

n = 256
d = 8
query_times = 30


def main(argv):
    # get command args
    try:
        opts, args = getopt.getopt(argv,"n:d:")
    except getopt.GetoptError:
        print('need -n -d')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-n':
            print("n =", arg)
        elif opt in ("-d"):
            print(opt)

    x_cor = []
    y_cor = []
    # === Task 1
    # load data
    for dataset_len in [int(len(poi_dataset_lines)/2),len(poi_dataset_lines)]:
        poi_dataset = []
        print("Ddataset length:", dataset_len)
        for i in range(dataset_len):
            row = poi_dataset_lines[i]
            x, y = row.split(',')
            x = float(x)
            y = float(y)
            node_index = []
            node_index.append(x)
            node_index.append(y)
            point = Point(index = node_index)
            poi_dataset.append(point)
            # prepare plot
            x_cor.append(x)
            y_cor.append(y)
        for n in [64, 256]:
            for d in [8,32]:
                rt = RTree(n,d)
                for point in poi_dataset:
                    rt = rt.insert(point)
                print("=== R tree: n = %d, d = %d"%(n,d))
                print("height:",rt.height())
                print("number of non leaf node:",rt.numOfNonLeaf())
                print("number of leaf node:",rt.numOfLeaf())

    # Task 2
    n = 256
    d = 8
    rt = RTree(n,d)
    for point in poi_dataset:
        rt = rt.insert(point)
    mbr = rt.mbr
    k = 1
    running_time = 3
    # do the 30 queries
    print("=== Query")
    for i in range(query_times):
        print("---")
        print("%d query"%(i+1))
        x_low = mbr.left + random.random() * (mbr.right - mbr.left)
        y_low = mbr.bottom + random.random() * (mbr.top - mbr.bottom)
        target_point = Point(index = [x_low,y_low])
        # search
        tree_running_time = []
        exhaustiveSearch_running_time = []
        statis = {}
        for j in range(running_time):
            print("%d running"%(j+1))
            T1 = time.perf_counter()
            knn_tree_result, search_range_record, statis = rt.knnSearch(target_point,k)
            T2 =time.perf_counter()
            tree_running_time.append(T2 - T1)
            T3 =time.perf_counter()
            knn_exhuastive_result = exhaustiveSearch(target_point,k,poi_dataset)
            T4 =time.perf_counter()
            exhaustiveSearch_running_time.append(T4-T3)
            isPass = drawResultPoint(target_point,knn_tree_result,knn_exhuastive_result)
        print("=== RTree Statis")
        print("- max running time:", max(tree_running_time))
        print("- min running time:", min(tree_running_time))
        print("- average running time:", statistics.mean(tree_running_time))
        print('number of points calculated distance: %d' % (statis["point_cal_distance"]))
        print('number of mbrs pruned by rule 1: %d' % (statis["rule1_pruned_count"]))
        print('number of mbrs pruned by rule 2: %d' % (statis["rule2_pruned_count"]))
        print('number of mbrs pruned by rule 3: %d' % (statis["rule3_pruned_count"]))
        print("=== Exhaustive Search Statis")
        print("- max running time:", max(exhaustiveSearch_running_time))
        print("- min running time:", min(exhaustiveSearch_running_time))
        print("- average running time:", statistics.mean(exhaustiveSearch_running_time))

    print("draw plot")
    plt.scatter(x_cor,y_cor, s= 2)
    # Get the current reference
    ax = plt.gca()
    # Create a Rectangle patch
    # from matplotlib.patches import Rectangle
    # temp_queue = queue.Queue()
    # temp_queue.put(rt)
    # while not temp_queue.empty():
    #     tree = temp_queue.get()
    #     if len(tree.children) > 0:
    #         for child in tree.children:
    #             temp_queue.put(child)
    #     else:
    #         the_mbr = tree.mbr
    #         # tree region rectangle
    #         rect = Rectangle(
    #             (the_mbr.left,the_mbr.bottom),
    #             the_mbr.right-the_mbr.left,
    #             the_mbr.top-the_mbr.bottom,
    #             linewidth=1,edgecolor='r',facecolor='none')
    #         ax.add_patch(rect)
    #         plt.savefig('../test2.jpg')
            # input("press any button")
    # draw seach range
    plt.scatter([target_point.index[0]], [target_point.index[1]],
        c ="yellow",
        linewidths = 2,
        marker ="^",
        edgecolor ="red",
        s = 50)
    print("draw search range")
    for i in range(len(search_range_record)):
        circle = plt.Circle(
            (target_point.index[0], target_point.index[1]),
            search_range_record[i],
            color='r', fill=False)
        ax.add_patch(circle)
        plt.savefig('../test2.jpg')


def printTree(node, blk):
    for i in range(blk):
        print(" ", end="")
    print("|-*")
    for child in node.children:
        printTree(child,blk+1)

def exhaustiveSearch(point,k, dataset):
    result_set = {}
    for target_point in dataset:
        dist = Point.distance(point, target_point)
        if len(result_set) < k:
            result_set[target_point] = dist
        else:
        # sort result set
            sort_result = sorted(result_set.items(), key = lambda kv:kv[1])
            max_point = sort_result.pop()
            if max_point[1] > dist:
                result_set.pop(max_point[0])
                result_set[target_point] = dist
    return list(result_set.keys())

def drawResultPoint(target_point,treeResult, exhaustiveResult):
    treeResult = sorted(treeResult, key= lambda kv:kv.index[0])
    exhaustiveResult = sorted(exhaustiveResult, key= lambda kv:kv.index[0])
    print("result from tree:")
    treeResult_x = []
    treeResult_y = []
    ehsResult_x = []
    ehsResult_y = []
    # check if it is correct
    isPass = True
    for i in range(len(treeResult)):
        if Point.distance(treeResult[i],target_point) != Point.distance(exhaustiveResult[i],target_point):
            isPass = False
    if not isPass:
        print("!!!!!!!!!!!!!!!!!!!")
        print("no god please no")
    # print result
    for point in treeResult:
        print("- " + "[", point.index[0], ",",point.index[1],"]: " + str(Point.distance(point,target_point)))
        treeResult_x.append(point.index[0])
        treeResult_y.append(point.index[1])
    # plt.scatter(treeResult_x, treeResult_y, c ="red",
    #         linewidths = 1,
    #         marker ="s",
    #         s = 30)
    # plt.scatter(ehsResult_x, ehsResult_y, c ="black",
    #         linewidths = 1,
    #         marker ="s",
    #         s = 30)
    print("result from exhaustive search:")
    for point in exhaustiveResult:
        print("- " + "[", point.index[0], ",",point.index[1],"]: " + str(Point.distance(point,target_point)))
        ehsResult_x.append(point.index[0])
        ehsResult_y.append(point.index[1])
    return isPass


if __name__=="__main__":
    main(sys.argv[1:])