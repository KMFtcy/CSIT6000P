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