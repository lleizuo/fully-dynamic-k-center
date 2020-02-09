from Impl.DataCache.DataPoint import DataPoint

class Cache(object):
    def __init__(self):
        self.allPoints = set()
        self.num = 0
        self.removed = -1
        self.inserted = None
    def feed(self, x, y):
        dp = DataPoint(self.num, x, y)
        self.num += 1
        self.allPoints.add(dp)
        self.inserted = dp
    def remove(self, id):
        self.allPoints.remove(DataPoint(id, 0, 0))
        self.removed = id
    