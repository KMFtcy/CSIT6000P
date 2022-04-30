from mimetypes import init


class Point:
    def __init__(self,index = []):
        self.index = index

    @staticmethod
    def distance(point1, point2):
        index1 = point1.index
        index2 = point2.index
        if len(index1) != len(index2):
            raise Exception("different dimensions points")
        distance = 0
        for i in range(len(index1)):
            distance += (index1[i]-index2[i]) ** 2
        distance = distance ** 0.5
        return distance

    # def __repr__(self):
    #     result = "["
    #     for index in self.index:
    #         result += index + ","
    #     result += "]"
    #     return result