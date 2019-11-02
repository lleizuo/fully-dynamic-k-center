import sys
sys.path.append('../../')
from Base.DataPointBase import DataPointBase
class DataPoint(DataPointBase):
    def __init__(self, id, x, y):
        self.x = x
        self.y = y
        self.id = id

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def distanceTo(self, dp):
        return (self.x-dp.x)^2 + (self.y-dp.y)^2


