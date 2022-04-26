import sys,getopt
sys.path.append("..")
from model import RTree
import load_dataset

poi_dataset_lines = load_dataset.load()
poi_dataset = []

n = 64
d = 8


def main(argv):
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
    # load data
    for row in poi_dataset_lines:
        x, y = row.split(',')
        x = float(x)
        y = float(y)
        node = []
        node.append(x)
        node.append(y)
        poi_dataset.append(node)
    print("Data load complete")
    RTree.RTreeNode.info()




if __name__=="__main__":
    main(sys.argv[1:])