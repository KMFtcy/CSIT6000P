import sys,getopt
sys.path.append("..")
from model.RTree import RTree
from model.Point import Point
import load_dataset

poi_dataset_lines = load_dataset.load()
poi_dataset = []

n = 64
d = 8


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

    rt = RTree(n,d)
    # load data
    for row in poi_dataset_lines:
        x, y = row.split(',')
        x = float(x)
        y = float(y)
        node_index = []
        node_index.append(x)
        node_index.append(y)
        point = Point(index = node_index)
        poi_dataset.append(node_index)
        rt = rt.insert(point)
    print("Data load complete")
    print(rt.height())
    print(rt.numOfNonLeaf())
    print(rt.numOfLeaf())
    print(rt.numOfPoints(), len(poi_dataset))


def printTree(node, blk):
    for i in range(blk):
        print(" ", end="")
    print("|-*")
    for child in node.children:
        printTree(child,blk+1)



if __name__=="__main__":
    main(sys.argv[1:])