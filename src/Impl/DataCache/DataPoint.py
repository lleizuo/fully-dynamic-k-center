import math
from Base.DataPointBase import DataPointBase

class DataPoint(DataPointBase):
    def __init__(self, id, x, y):       # id, longitude, latitude
        self.x = (x/360)*(2*math.pi)    # convert to arc
        self.y = (y/360)*(2*math.pi)
        self.id = id

    def __repr__(self):
        return "%d: (%.2f, %.2f)" % (self.id, self.x*360/(2*math.pi), self.y*360/(2*math.pi))
    
    def sphereDist(self, dp) -> float:
        # print(self, dp)
        try:
            return 6371*math.acos(math.sin(self.y)*math.sin(dp.y) + 
                              math.cos(self.y)*math.cos(dp.y)*math.cos(self.x - dp.x))
        except:
            # print (self, dp)
            return float("inf")
