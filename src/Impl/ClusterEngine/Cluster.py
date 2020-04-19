from Base.SetBase import SetBase
from Impl.DataCache import DataPoint as DP
from typing import Set
class Cluster(object):
    def __init__(self, c:DP, points):
        super().__init__()
        self.center : DP = c
        self.points : Set[DP] = points if points is not None else set()
        self.rim = max(self.points, key=lambda p : p.sphereDist(self.center)) if len(self.points)>0 else None
        self.radius = self.rim.sphereDist(self.center) if self.rim is not None else 0

    def __repr__(self):
        return "Cluster with center %s, points: %s" % (self.center, self.points)

    # insert a point to the cluster
    def insert(self,p):
        self.points.add(p)
        if self.radius < self.center.sphereDist(p):
            self.rim = p
            self.radius = self.center.sphereDist(p)
    
    # check if a point is in the cluster, cost: O(1)
    def contains(self,pid):
        # if DP.DataPoint(pid,-1,-1) in self.points:
            # return True
        # return False
        return DP.DataPoint(pid,-1,-1) in self.points

    def remove(self,pid):
        self.points.discard(DP.DataPoint(pid,-1,-1))

        # for p in self.points:
        #     if p.id == pid:
        #         self.points.discard(p)
        #         if p.sphereDist(self.center)>=self.radius:
        #             self.radius = max([p.sphereDist(self.center) for p in self.points]) if len(self.points)>0 else 0
        #         break
    
    def nextCenter(self) -> DP:
        minDist = float("inf")
        c = None
        for p in self.points:
            if p.sphereDist(self.center) < minDist:
                minDist = p.sphereDist(self.center)
                c = p
        # print('closest point is: ', c)
        return c
    
    