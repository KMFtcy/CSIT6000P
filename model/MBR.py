from . import MBR
from . import Point


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

    @staticmethod
    def isIntersectByCircle(mbr: MBR, centre: Point.Point, radius):
        dist = MBR.getMindist(mbr, centre)
        if dist > radius:
            return False
        else:
            return True

    @staticmethod
    def getMindist(mbr: MBR, point: Point.Point):
        x = point.index[0]
        y = point.index[1]
        top = mbr.top
        bottom = mbr.bottom
        left = mbr.left
        right = mbr.right
        if x <= left and y > top:
            return ((x-left) ** 2 + (y-top) ** 2) ** 0.5
        if x > left and x <= right and y > top:
            return y - top
        if x > right and y >= top:
            return ((x-right) ** 2 + (y-top) ** 2) ** 0.5
        if x > right and y < top and y >= bottom:
            return x - right
        if x >= right and y < bottom:
            return ((x-right) ** 2 + (y-bottom) ** 2) ** 0.5
        if x >= left and x < right and y < bottom:
            return bottom - y
        if x < left and y <= bottom:
            return ((x-left) ** 2 + (y-bottom) ** 2) ** 0.5
        if x < left and y <= top and y > bottom:
            return left - x
        return 0

    @staticmethod
    def getMinMaxDist(mbr: MBR, point: Point.Point):
        x = point.index[0]
        y = point.index[1]
        top = mbr.top
        bottom = mbr.bottom
        left = mbr.left
        right = mbr.right
        if left < x and x < right and bottom < y and y < top:
            return 0
        # TODO: 可能有坑，没有考虑点在mbr中情况
        corner1 = Point.Point(index=[mbr.left, mbr.top])
        corner2 = Point.Point(index=[mbr.left, mbr.bottom])
        corner3 = Point.Point(index=[mbr.right, mbr.top])
        corner4 = Point.Point(index=[mbr.right, mbr.bottom])
        result = Point.Point.distance(point, corner1)
        for corner in [corner2, corner3, corner4]:
            dist = Point.Point.distance(point, corner)
            if dist < result:
                result = dist
        return result
