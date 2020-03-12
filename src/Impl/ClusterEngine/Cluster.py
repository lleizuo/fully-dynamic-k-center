from Base.SetBase import SetBase
from Impl.DataCache import DataPoint as DP
from typing import Set
class Cluster(object):
    def __init__(self, p:DP, points):
        super().__init__()
        self.center : DP = p
        self.points : Set[DP] = points if points is not None else set()

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
            if p.sphereDist(self.center) < minDist:
                minDist = p.sphereDist(self.center)
                c = p
        print('closest point is: ', c)
        return c
    
    