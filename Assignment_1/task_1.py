import load_dataset
from model import MBR
from model import quadtree

poi_dataset_lines = load_dataset.load()
poi_dataset = []


# === task 1
# === question 1
mbr = MBR.MBR()
print("Analyze dataset...")
for row in poi_dataset_lines:
    x, y = row.split(',')
    x = float(x)
    y = float(y)
    mbr.left = x if x < mbr.left else mbr.left
    mbr.right = x if x > mbr.right else mbr.right
    mbr.top = y if y > mbr.top else mbr.top
    mbr.bottom = y if y < mbr.bottom else mbr.bottom
    node = []
    node.append(x)
    node.append(y)
    poi_dataset.append(node)
print("Analyze complete")
print("Target MBR:")
print(mbr)
# === question 2
resolution = 0
grid_idx = {}
is_finish = False
while not is_finish:
    is_finish = True
    v_step = (mbr.right - mbr.left)/pow(2, resolution)
    h_step = (mbr.top - mbr.bottom)/pow(2, resolution)
    for point in poi_dataset:
        point_h_idx = int((point[0]-mbr.left)/v_step) + 1
        point_v_idx = int((mbr.top - point[1])/h_step)
        point_idx = pow(2, resolution)*point_v_idx + point_h_idx
        if point_idx not in grid_idx:
            grid_idx[point_idx] = []
            grid_idx[point_idx].append(point)
        else:
            grid_idx[point_idx].append(point)
            if len(grid_idx[point_idx]) > 128:
                is_finish = False
                break
    if not is_finish:
        resolution += 1
print("Target resolution: ", resolution)
# === question 3
cells_count = 0
for index in grid_idx:
    if len(grid_idx[index]) > 5:
        cells_count += 1
print("Cells count for contains no more than 5 points: ", pow(pow(2, resolution), 2)-cells_count)


# === task 2
# === question 1
quadtree = quadtree.QuadTreeNode()
for point in poi_dataset:
    quadtree.addNode(point)
print("layer")
print(quadtree.depth())
stack = [quadtree]
leafNode = []
while len(stack) > 0:
    tree = stack.pop()
    for subtree in [tree.topLeft, tree.topRight, tree.bottomLeft, tree.bottomRight]:
        if subtree != None:
            stack.append(subtree)
    if tree.isLeaf:
        leafNode.append(tree)
for tree in leafNode:
    print(tree.z_value)