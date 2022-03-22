import load_dataset
import model

poi_dataset_lines = load_dataset.load()
poi_dataset = []

#=== question 1
quadTree = model.QuadTreeNode()
for row in poi_dataset_lines:
    x, y = row.split(',')
    x = float(x)
    y = float(y)
    node = []
    node.append(x)
    node.append(y)
    quadTree.addNode(node)
print(quadTree.MBR)
print("tree depth: ",quadTree.depth())
print('dataset counts: ', quadTree.nodeNum)
# find cells with no more than 5 points
