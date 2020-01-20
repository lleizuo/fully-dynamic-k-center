from Base.SetBase import SetBase
from Impl.DataCache import DataPoint as DP
from typing import Set
class Cluster(object):
    def __init__(self, p:DP, points:Set[DP]):
        super().__init__()
        self.center : DP = p
        self.points : Set[DP] = points

    def __repr__(self):
        return "Cluster with center %s, points: %s" % (self.center, self.points)

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
    
    def nextCenter(self) -> DP:
        minDist = float("inf")
        c = None
        for p in self.points:
            if p.distanceTo(self.center) < minDist:
                minDist = p.distanceTo(self.center)
                c = p
        return c
    
    