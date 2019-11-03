from Base.SetBase import SetBase
from Impl.DataCache import DataPoint as DP
class Cluster(object):
    def __init__(self, pid:int, points:set):
        super().__init__()
        self.center = pid
        self.points = points

    # insert a point to the cluster
    def insert(self,p):
        self.points.add(p)
    
    # check if a point is in the cluster, cost: O(1)
    def contains(self,pid):
        if DP.DataPoint(pid,-1,-1) in self.points:
            return True
        return False

    def remove(self,pid):
        self.points.discard(DP.DataPoint(pid,-1,-1))
    
    