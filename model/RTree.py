from .MBR import MBR
from .Point import Point
from . import RTree
import sys
import math


class RTree:

    """
    The function __init__() is a special function that is called when an object is created from a
    class and it allows the class to initialize the attributes of the class.

    :param n: The maximum number of points in leaf node
    :param d: A non-leaf node can have a maximum of d subtrees
    """

    def __init__(self, n=64, d=8):
        self.n = n
        self.d = d
        self.mbr = MBR()
        self.children = []
        self.point_pool = []  # leaf objects.
        self.parent = None

    @staticmethod
    def mergeSort(points):
        # merge process
        def merge(left, right):
            result = []  # save merge result
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i].index[0] <= right[j].index[0]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result = result + left[i:] + right[j:]  # add the rest elements
            return result
        # recursive
        if len(points) <= 1:
            return points
        mid = len(points) // 2
        left = RTree.mergeSort(points[:mid])
        right = RTree.mergeSort(points[mid:])
        return merge(left, right)

    @staticmethod
    def mergeSortTrees(trees):
        # merge process
        def merge(left, right):
            result = []  # save merge result
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i].mbr.left <= right[j].mbr.left:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result = result + left[i:] + right[j:]  # add the rest elements
            return result
        # recursive
        if len(trees) <= 1:
            return trees
        mid = len(trees) // 2
        left = RTree.mergeSortTrees(trees[:mid])
        right = RTree.mergeSortTrees(trees[mid:])
        return merge(left, right)

    def insert(self, point: Point):
        # choose a reasonable leaf node to add the point
        leafNode = RTree.chooseLeaf(point, self)
        # add to leaf node, if the node can not contains no more points, split
        leafNode.point_pool.append(point)
        x = point.index[0]
        y = point.index[1]
        leafNode.mbr.left = x if x < leafNode.mbr.left else leafNode.mbr.left
        leafNode.mbr.right = x if x > leafNode.mbr.right else leafNode.mbr.right
        leafNode.mbr.top = y if y > leafNode.mbr.top else leafNode.mbr.top
        leafNode.mbr.bottom = y if y < leafNode.mbr.bottom else leafNode.mbr.bottom
        newNode = None
        if len(leafNode.point_pool) > self.n:
            leafNode, newNode = RTree.splitLeafNode(leafNode)
        # pass up the change, if node has been splited, apply to the new node too
        root = RTree.adjustTreeFromLeaf(leafNode, newNode)
        return root

    @staticmethod
    def splitLeafNode(treeNode: RTree):
        # split node depends on x coordinate
        pointPoolLen = len(treeNode.point_pool)
        newNode = RTree(treeNode.n, treeNode.d)
        fullPool = treeNode.point_pool
        # order point by x value
        fullPool = RTree.mergeSort(fullPool)
        # split points
        treeNode.point_pool = fullPool[0:round(pointPoolLen/2)]
        newNode.point_pool = fullPool[round(pointPoolLen/2):pointPoolLen]
        # modify mbr
        treeNode.mbr = MBR()
        for point in treeNode.point_pool:
            x = point.index[0]
            y = point.index[1]
            treeNode.mbr.left = x if x < treeNode.mbr.left else treeNode.mbr.left
            treeNode.mbr.right = x if x > treeNode.mbr.right else treeNode.mbr.right
            treeNode.mbr.top = y if y > treeNode.mbr.top else treeNode.mbr.top
            treeNode.mbr.bottom = y if y < treeNode.mbr.bottom else treeNode.mbr.bottom
        for point in newNode.point_pool:
            x = point.index[0]
            y = point.index[1]
            newNode.mbr.left = x if x < newNode.mbr.left else newNode.mbr.left
            newNode.mbr.right = x if x > newNode.mbr.right else newNode.mbr.right
            newNode.mbr.top = y if y > newNode.mbr.top else newNode.mbr.top
            newNode.mbr.bottom = y if y < newNode.mbr.bottom else newNode.mbr.bottom
        return treeNode, newNode

    @staticmethod
    def splitMidNode(treeNode: RTree):
        newNode = RTree(treeNode.n, treeNode.d)
        childrenLen = len(treeNode.children)
        fullPool = treeNode.children
        # order child tree by mbr
        fullPool = RTree.mergeSortTrees(fullPool)
        # split tree
        treeNode.children = fullPool[0:round(childrenLen/2)]
        newNode.children = fullPool[round(childrenLen/2):childrenLen]
        # modify mbr
        treeNode.mbr = MBR()
        for node in [treeNode, newNode]:
            for child in node.children:
                childMBR = child.mbr
                node.mbr.left = childMBR.left if childMBR.left < node.mbr.left else node.mbr.left
                node.mbr.right = childMBR.right if childMBR.right > node.mbr.right else node.mbr.right
                node.mbr.top = childMBR.top if childMBR.top > node.mbr.top else node.mbr.top
                node.mbr.bottom = childMBR.bottom if childMBR.bottom < node.mbr.bottom else node.mbr.bottom
                # assign new parent
                child.parent = node
        return treeNode, newNode

    @staticmethod
    def chooseLeaf(point, treeNode: RTree) -> RTree:
        if len(treeNode.children) > 0:
            # choose the child that keep the smallest size
            minIncreament = sys.float_info.max
            targetChild = treeNode
            for child in treeNode.children:
                mbr = MBR(child.mbr.top, child.mbr.bottom,
                          child.mbr.left, child.mbr.right)
                origin_size = (mbr.right-mbr.left)*(mbr.top-mbr.bottom)
                x = point.index[0]
                y = point.index[1]
                mbr.left = x if x < mbr.left else mbr.left
                mbr.right = x if x > mbr.right else mbr.right
                mbr.top = y if y > mbr.top else mbr.top
                mbr.bottom = y if y < mbr.bottom else mbr.bottom
                new_size = (mbr.right-mbr.left)*(mbr.top-mbr.bottom)
                increment = new_size-origin_size
                if increment < minIncreament:
                    minIncreament = increment
                    targetChild = child
            return RTree.chooseLeaf(point, targetChild)
        return treeNode

    @staticmethod
    def adjustTreeFromLeaf(leafNode: RTree, newLeafNode: RTree = None):
        N = leafNode
        NN = newLeafNode
        while True:
            # stop if it is root node
            if N.parent == None:
                break
            parent = N.parent
            # 调整父结点条目的最小边界矩形
            for child in parent.children:
                childMBR = child.mbr
                parent.mbr.left = childMBR.left if childMBR.left < parent.mbr.left else parent.mbr.left
                parent.mbr.right = childMBR.right if childMBR.right > parent.mbr.right else parent.mbr.right
                parent.mbr.top = childMBR.top if childMBR.top > parent.mbr.top else parent.mbr.top
                parent.mbr.bottom = childMBR.bottom if childMBR.bottom < parent.mbr.bottom else parent.mbr.bottom
            # 向上传递结点分裂
            if NN != None:
                parent.children.append(NN)
                NN.parent = parent
                childMBR = NN.mbr
                childMBR = child.mbr
                parent.mbr.left = childMBR.left if childMBR.left < parent.mbr.left else parent.mbr.left
                parent.mbr.right = childMBR.right if childMBR.right > parent.mbr.right else parent.mbr.right
                parent.mbr.top = childMBR.top if childMBR.top > parent.mbr.top else parent.mbr.top
                parent.mbr.bottom = childMBR.bottom if childMBR.bottom < parent.mbr.bottom else parent.mbr.bottom
                NN = None
            if len(parent.children) > parent.d:
                parent, newParent = RTree.splitMidNode(parent)
                NN = newParent
            N = parent
        if NN != None:
            newRoot = RTree(N.n, N.d)
            newRoot.children.append(N)
            newRoot.children.append(NN)
            N.parent = newRoot
            NN.parent = newRoot
            for child in newRoot.children:
                childMBR = child.mbr
                newRoot.mbr.left = childMBR.left if childMBR.left < newRoot.mbr.left else newRoot.mbr.left
                newRoot.mbr.right = childMBR.right if childMBR.right > newRoot.mbr.right else newRoot.mbr.right
                newRoot.mbr.top = childMBR.top if childMBR.top > newRoot.mbr.top else newRoot.mbr.top
                newRoot.mbr.bottom = childMBR.bottom if childMBR.bottom < newRoot.mbr.bottom else newRoot.mbr.bottom
            N = newRoot
        return N

    def height(self):
        if len(self.children) == 0:
            return 1
        height = 0
        for child in self.children:
            sub_height = child.height()
            if sub_height > height:
                height = sub_height
        return sub_height + 1

    def numOfNonLeaf(self):
        if len(self.children) == 0:
            return 0
        count = 0
        for child in self.children:
            count += child.numOfNonLeaf()
        return count + 1

    def numOfLeaf(self):
        if len(self.children) == 0:
            return 1
        count = 0
        for child in self.children:
            count += child.numOfLeaf()
        return count

    def numOfPoints(self):
        if len(self.children) == 0:
            return len(self.point_pool)
        count = 0
        for child in self.children:
            count += child.numOfPoints()
        return count

    def getPointsByMBR(self, mbr):
        if len(self.children) == 0:
            return self.point_pool
        result = []
        for child in self.children:
            if MBR.isIntersect(mbr, child.mbr):
                result += child.getPointsByMBR(mbr)
        return result

    def getPointsByCircle(self, point, radius):
        if len(self.children) == 0:
            return self.point_pool
        result = []
        for child in self.children:
            if MBR.isIntersectByCircle(child.mbr, point, radius):
                result += child.getPointsByCircle(point, radius)
        return result

    def rule1(self, ABL, point):
        finish = False
        while not finish:
            finish = True
            for i in range(len(ABL)):
                for j in range(len(ABL)):
                    if i == j:
                        continue
                    if ABL[i]["mindist"] > ABL[j]["minmaxdist"]:
                        finish = False
                        ABL.pop(i)
                        break
                if not finish:
                    break
        return ABL

    def rule2(self, ABL, result, point):
        result_point = result[-1]
        for obj in ABL:
            if Point.distance(point, result_point) > obj["minmaxdist"]:
                result.pop()
                break
        return result

    def rule3(self, ABL, result, point):
        result_point = result[-1]
        for obj in ABL:
            if Point.distance(point, result_point) < obj["mindist"]:
                ABL.remove(obj)
        return ABL

    # def knnSearch(self, point, k):
    #     temp_queue = []
    #     temp_queue.append(self)
    #     result_set = {}

    #     while len(temp_queue) > 0:
    #         tree = temp_queue.pop()
    #         if len(tree.children) > 0:
    #             for child in tree.children:
    #                 temp_queue.append(child)
    #         else:
    #             for target_point in tree.point_pool:
    #                 dist = Point.distance(point, target_point)
    #                 if len(result_set) < k:
    #                     result_set[target_point] = dist
    #                 else:
    #                 # sort result set
    #                     sort_result = sorted(result_set.items(), key = lambda kv:kv[1])
    #                     max_point = sort_result.pop()
    #                     if max_point[1] > dist:
    #                         result_set.pop(max_point[0])
    #                         result_set[target_point] = dist
    #     return list(result_set.keys()), []


    def knnSearch(self, point, k):
        points_num = self.numOfPoints()
        if k > points_num:
            print("not support")
            return [],[]
        main_mbr = self.mbr
        scale_ratio = (k/points_num) ** 0.5
        radius = ((main_mbr.right - main_mbr.left) * (main_mbr.top -
                  main_mbr.bottom) * scale_ratio / math.pi) ** 0.5
        search_range_record = []
        search_range_record.append(radius)

        result = []
        while len(result) < k:
            result = []
            ABL = [
                {
                    "tree": self,
                    "mindist": 0,
                    "minmaxdist": 0
                }
            ]  # point must be in the root
            while len(ABL) > 0:
                obj = ABL.pop()
                tree = obj["tree"]
                if len(tree.children) > 0:
                    newBranchs = []
                    for child in tree.children:
                        if MBR.isIntersectByCircle(child.mbr, point, radius):
                            newBranchs.append(child)
                    # sort by mindist
                    newBranchs = sorted(
                        newBranchs, key=lambda kv: -MBR.getMindist(kv.mbr, point))
                    # append into stack
                    for newBranch in newBranchs:
                        newMinDist = MBR.getMindist(newBranch.mbr, point)
                        newMinMaxDist = MBR.getMinMaxDist(newBranch.mbr, point)
                        ABL.append(
                            {
                                "tree": newBranch,
                                "mindist": newMinDist,
                                "minmaxdist": newMinMaxDist
                            }
                        )
                else:
                    # if it is leafnode, use point pool to update result
                    for pool_point in tree.point_pool:
                        if Point.distance(point, pool_point) <= radius:
                            result.append(pool_point)
                    while len(result) > k:
                        max_dist = 0
                        max_idx = 0
                        for idx in range(len(result)):
                            dist = Point.distance(result[idx], point)
                            if dist > max_dist:
                                max_dist = dist
                                max_idx = idx
                        result.pop(max_idx)
                # if len(result) == k:
                #     ABL = self.rule1(ABL, point)
                #     result = self.rule2(ABL, result, point)
                #     ABL = self.rule3(ABL, result, point)
            if len(result) < k:
                radius *= 2
                search_range_record.append(radius)

        return result, search_range_record
