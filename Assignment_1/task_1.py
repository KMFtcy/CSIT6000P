import load_dataset
from model import quadtree

poi_dataset_lines = load_dataset.load()
poi_dataset = []

# === question 1
Tree = quadtree.QuadTreeNode()
for row in poi_dataset_lines:
    x, y = row.split(',')
    x = float(x)
    y = float(y)
    node = []
    node.append(x)
    node.append(y)
    Tree.addNode(node)
print("Target MBR:")
print(Tree.MBR)
print("Target resolution: ", Tree.depth()-1)
# find cells with no more than 5 points
cells_count = 0
tree_stack =[Tree]
while len(tree_stack) >0:
    tree = tree_stack.pop()
    if tree.isLeaf:
        if tree.nodeNum <= 5:
            cells_count += 1
        continue
    for subtree in [tree.topLeft, tree.topRight, tree.bottomLeft, tree.bottomRight]:
            if subtree != None:
                tree_stack.append(subtree)
print("Cells count for contains no more than 5 points: ", cells_count)

# === question 2