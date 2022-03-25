import load_dataset
from model import MBR
from model import quadtree
import random

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
        grid_idx = {}
        resolution += 1
print("Target resolution: ", resolution)
# === question 3
cells_count = 0
for index in grid_idx:
    if len(grid_idx[index]) > 5:
        cells_count += 1
print("Cells count for contains no more than 5 points: ",
      pow(pow(2, resolution), 2)-cells_count)


# === task 2
# === question 1
print("=== create quadtree and z_value")
quadtree = quadtree.QuadTreeNode()
for point in poi_dataset:
    quadtree.addNode(point)
print("quadtree created")
# === question 2
print("=== create z_value index")
stack = [quadtree]
zvalue_index = {}
while len(stack) > 0:
    tree = stack.pop()
    for subtree in [tree.bottomLeft, tree.topLeft, tree.bottomRight, tree.topRight]:
        if subtree != None:
            stack.append(subtree)
    if tree.isLeaf:
        zvalue_index[tree.z_value] = tree.bucket
zvalue_index = sorted(zvalue_index)
print("z_value index created")


# === task 3
# === question 1
def search_grid_idx_windows(grid_idx, mbr, resolution, x_low, y_low, x_high, y_high):
    # get (x_low,y_low) and (x_high,y_high) index in grid
    v_step = (mbr.right - mbr.left)/pow(2, resolution)
    h_step = (mbr.top - mbr.bottom)/pow(2, resolution)
    low_point_h_idx = int((x_low-mbr.left)/v_step) + 1
    low_point_v_idx = int((mbr.top - y_low)/h_step)
    low_point_idx = pow(2, resolution)*low_point_v_idx + low_point_h_idx
    high_point_h_idx = int((x_high-mbr.left)/v_step) + 1
    high_point_v_idx = int((mbr.top - y_high)/h_step)
    high_point_idx = pow(2, resolution)*high_point_v_idx + high_point_h_idx
    # catch grid
    grid_result = []
    grid_height = int((low_point_idx - high_point_idx)/resolution) + 1
    grid_width = (high_point_idx + grid_height * resolution) - low_point_idx
    search_pointer = high_point_idx - grid_width
    while search_pointer != low_point_idx:
        for i in range(grid_width + 1):
            if search_pointer + i in grid_idx:
                grid_result.append(grid_idx[search_pointer + i])
        search_pointer += resolution
    # catch point in grid result
    point_result = []
    for grid in grid_result:
        point_result += grid
    return point_result
# === question 2
def search_zvalue_idx_windows(zvalue_index,x_low, y_low, x_high, y_high):
    result = []
    return result
# === question 3
for i in range(20):
    print("=== search ", i+1)
    x_low = mbr.left + random.random() * (mbr.right - mbr.left)
    y_low = mbr.bottom + random.random() * (mbr.top - mbr.bottom)
    x_high = x_low + random.random() * (mbr.right - x_low)
    y_high = y_low + random.random() * (mbr.top - y_low)
    print("x_low: ",x_low,", y_low: ", y_low)
    print("x_high: ",x_high, ", y_high: ",y_high)
    print("points counts result from grid index: ",len(search_grid_idx_windows(grid_idx, mbr,
      resolution, x_low, y_low, x_high, y_high)))
