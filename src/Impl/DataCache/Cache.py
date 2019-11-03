from Impl.DataCache.DataPoint import DataPoint

class Cache(object):
    def __init__(self):
        self.allPoints = set()
        self.num = 0
    def feed(self, x, y):
        dp = DataPoint(self.num, x, y)
        self.num += 1
        self.allPoints.add(dp)
    