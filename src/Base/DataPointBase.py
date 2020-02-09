import math
class DataPointBase(object):
    def __init__(self, id, x, y):
        self.x = x
        self.y = y
        self.id = id
    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other) -> bool:
        if self.id == other.id:
            return True
        # if self.x == other.x and self.y == other.y:
        #     return True
        return False
    def __repr__(self):
        return "%d: (%.2f, %.2f)" % (self.id, self.x, self.y)
    def dist(self, p):
        return math.sqrt(math.pow((self.x-p.x), 2) + math.pow((self.y-p.y), 2))
