import MBR

class Node:
    def __init__(self, index):
        self.index = index


class QuadTreeNode:
    MAX_NODE_NUM = 128

    def __init__(self, isLeaf=True, topLeft=None, topRight=None, bottomLeft=None, bottomRight=None):
        self.MBR = MBR(0, float('inf'), float('inf'), 0)
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.bucket = []
        self.nodeNum = 0
        self.isLeaf = isLeaf

    def addNode(self, nodeIndex):
        self.MBR.right = nodeIndex[0] if self.MBR.right < nodeIndex[0] else self.MBR.right
        self.MBR.left = nodeIndex[0] if self.MBR.left > nodeIndex[0] else self.MBR.left
        self.MBR.top = nodeIndex[1] if self.MBR.top < nodeIndex[1] else self.MBR.top
        self.MBR.bottom = nodeIndex[1] if self.MBR.bottom > nodeIndex[1] else self.MBR.bottom
        self.bucket.append(nodeIndex)
        self.nodeNum += 1
        if self.isLeaf:
            if self.nodeNum >= QuadTreeNode.MAX_NODE_NUM:
                for node in self.bucket:
                    self.addToSubTree(node)
                self.isLeaf = False
        else:
            self.addToSubTree(nodeIndex)

    def addToSubTree(self, node):
        mid_h = (self.MBR.top + self.MBR.bottom)/2
        mid_v = (self.MBR.left + self.MBR.right)/2
        if node[0] <= mid_v and node[1] < mid_h:
            if self.bottomLeft == None:
                self.bottomLeft = QuadTreeNode()
            self.bottomLeft.addNode(node)
        elif node[0] >= mid_v and node[1] < mid_h:
            if self.bottomRight == None:
                self.bottomRight = QuadTreeNode()
            self.bottomRight.addNode(node)
        elif node[0] <= mid_v and node[1] > mid_h:
            if self.topLeft == None:
                self.topLeft = QuadTreeNode()
            self.topLeft.addNode(node)
        elif node[0] >= mid_v and node[1] > mid_h:
            if self.topRight == None:
                self.topRight = QuadTreeNode()
            self.topRight.addNode(node)

    def depth(self):
        depth = 0
        for subtree in [self.topLeft, self.topRight, self.bottomLeft, self.bottomRight]:
            if subtree != None:
                subtree_depth = subtree.depth()
                depth = subtree_depth if subtree_depth > depth else depth
        depth += 1
        return depth
