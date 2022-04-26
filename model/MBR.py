from . import MBR


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

    """
    If the left edge of the first rectangle is to the right of the right edge of the second rectangle, or the bottom edge of the first rectangle is above the top edge of the second rectangle, then the rectangles do not intersect

    :param mbr1: the first MBR
    :type mbr1: MBR
    :param mbr2: the MBR that we want to check if it intersects with mbr1
    :type mbr2: MBR
    :return: A boolean value.
    """
    @staticmethod
    def isIntersect(mbr1: MBR, mbr2: MBR):
        newLeft = max(mbr1.left, mbr2.left)
        newBottom = max(mbr1.bottom, mbr2.bottom)
        newRight = min(mbr1.right, mbr2.right)
        newTop = min(mbr1.top, mbr2.top)
        return not ((newLeft > newRight) or (newBottom > newTop))
