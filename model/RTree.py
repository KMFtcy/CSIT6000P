from . import MBR

class RTreeNode:
    def insert(self, rectangle):
        self.rectangle = rectangle

    @staticmethod
    def info():
        print("test")