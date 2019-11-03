import sys
sys.path.append('../../')
import math
from Base.DataPointBase import DataPointBase
class DataPoint(DataPointBase):
    def __init__(self, id, x, y):
        self.x = x
        self.y = y
        self.id = id

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other) -> bool:
        if self.id == other.id:
            return True
        return False
    
    def __repr__(self):
        return "%d: (%.2f, %.2f)" % (self.id, self.x, self.y)

    def distanceTo(self, dp) -> float:
        return math.sqrt(math.pow((self.x-dp.x), 2) + math.pow((self.y-dp.y), 2))


