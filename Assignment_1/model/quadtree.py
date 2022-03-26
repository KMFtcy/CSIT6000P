
class MBR:
    def __init__(self, top=0, bottom=float('inf'), left=float('inf'), right=0):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def __repr__(self):
        result = "{\n\tup: " + str(self.top) + '\n'
        result += "\tbottom: " + str(self.bottom) + '\n'
        result += "\tleft: " + str(self.left) + '\n'
        result += "\tright: " + str(self.right) + '\n}'
        return result


class Node:
    def __init__(self, index):
        self.index = index


class QuadTreeNode:
    MAX_NODE_NUM = 5
    MAX_DEPTH = 9

    def __init__(self, MBR=None, z_value=1, node_depth=1, isLeaf=True, topLeft=None, topRight=None, bottomLeft=None, bottomRight=None):
        self.MBR = MBR
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        if node_depth > 0:
            self.node_depth = node_depth
        else:
            self.node_depth = 1
        self.bucket = []
        self.nodeNum = 0
        self.isLeaf = isLeaf
        self.z_value = z_value

    def addNode(self, nodeIndex):
        if nodeIndex[0] > self.MBR.right or nodeIndex[0] < self.MBR.left or nodeIndex[1] > self.MBR.top or nodeIndex[1] < self.MBR.bottom:
            print("node is out of MBR")
            print("node depth:",self.node_depth,", isleaf: ",self.isLeaf, ", x:", nodeIndex[0], ", y:", nodeIndex[1])
            print(self.MBR)
            return
        self.bucket.append(nodeIndex)
        self.nodeNum += 1
        if self.isLeaf:
            if self.nodeNum > QuadTreeNode.MAX_NODE_NUM and self.node_depth < QuadTreeNode.MAX_DEPTH:
                for node in self.bucket:
                    self.addToSubTree(node)
                self.isLeaf = False
        else:
            self.addToSubTree(nodeIndex)

    def addToSubTree(self, node):
        mid_h = (self.MBR.top + self.MBR.bottom)/2
        mid_v = (self.MBR.left + self.MBR.right)/2
        subtree = QuadTreeNode(node_depth=self.node_depth + 1)
        if node[0] <= mid_v and node[1] < mid_h:
            if self.bottomLeft == None:
                self.bottomLeft = subtree
                zvalue_str = str(self.z_value)
                zvalue_str += '1'
                subtree.setZvalue(int(zvalue_str))
                subtree.setMBR(
                    MBR(mid_h, self.MBR.bottom, self.MBR.left, mid_v))
            self.bottomLeft.addNode(node)
        elif node[0] >= mid_v and node[1] > mid_h:
            if self.bottomRight == None:
                self.bottomRight = subtree
                zvalue_str = str(self.z_value)
                zvalue_str += '4'
                subtree.setZvalue(int(zvalue_str))
                subtree.setMBR(
                    MBR(self.MBR.top, mid_h, mid_v, self.MBR.right))
            self.bottomRight.addNode(node)
        elif node[0] < mid_v and node[1] >= mid_h:
            if self.topLeft == None:
                self.topLeft = subtree
                zvalue_str = str(self.z_value)
                zvalue_str += '2'
                subtree.setZvalue(int(zvalue_str))
                subtree.setMBR(
                    MBR(self.MBR.top, mid_h, self.MBR.left, mid_v))
            self.topLeft.addNode(node)
        elif node[0] > mid_v and node[1] <= mid_h:
            if self.topRight == None:
                self.topRight = subtree
                zvalue_str = str(self.z_value)
                zvalue_str += '3'
                subtree.setZvalue(int(zvalue_str))
                subtree.setMBR(
                    MBR(mid_h, self.MBR.bottom,  mid_v, self.MBR.right))
            self.topRight.addNode(node)

    def depth(self):
        depth = 0
        for subtree in [self.topLeft, self.topRight, self.bottomLeft, self.bottomRight]:
            if subtree != None:
                subtree_depth = subtree.depth()
                depth = subtree_depth if subtree_depth > depth else depth
        depth += 1
        return depth

    def setZvalue(self, z_value):
        self.z_value = z_value

    def setMBR(self, MBR):
        self.MBR = MBR
