from Impl.ClusterEngine.Cluster import Cluster
from Impl.ClusterEngine.UnClustered import UnClustered
from Impl.DataCache.DataPoint import DataPoint
import random
from itertools import chain
from typing import List, Set

class NestedClustDS(object):
    def __init__(self, R:float, k:int):
        self.R = R
        self.r = R*(0.33)             # 1 / (1 + rt2 + rt6)
        self.k = k
        self.Clusters : List[HighLvlCluster]= []
        self.unClustered = set()
        self.centers = []

    def simpleClustering(self, X:set()):
        self.unClustered = X.copy()
        lowLvlClusters = set()
        while len(self.unClustered)>0:
            c = random.sample(self.unClustered, 1)[0]
            self.unClustered.discard(c)
            within2r = set(filter(lambda p: p!=c and p.sphereDist(c)<=2*self.r, self.unClustered))
            newCluster = Cluster(c, within2r)
            lowLvlClusters.add(newCluster)
            self.unClustered = self.unClustered.difference(within2r)
        cnt = 0
        while cnt<self.k and len(lowLvlClusters)>0:
            randClust = random.sample(lowLvlClusters, 1)[0]
            # randomly select a center for higher level cluster
            if len(randClust.points)>0:
                C = random.sample(randClust.points, 1)[0]
                randClust.points.discard(C)
            else:
                C = randClust.center
                lowLvlClusters.remove(randClust)
            # filter out lower level clusters within 2R of the center
            within2R = list(filter(lambda clst: pntClstDist(C, clst)<=2*self.R, lowLvlClusters))
            newHighLvlClst = HighLvlCluster(C, self.r, within2R)
            self.centers.append(C)
            self.Clusters.append(newHighLvlClst)
            lowLvlClusters = lowLvlClusters.difference(within2R)
            cnt += 1
        self.unClustered = lowLvlClusters


    def insert(self, p):
        for highLvlClst in self.Clusters:
            if p.sphereDist(highLvlClst.center) <= 2*self.R:
                highLvlClst.insert(p)
                return
        for clst in self.unClustered:
            if p.sphereDist(clst.center) <= 2*self.r:
                clst.insert(p)
                return
        newLowLvlClst = Cluster(p, None)
        self.unClustered.add(newLowLvlClst)

    def delete(self, pid):
        for highLvlClst in self.Clusters:
            i = highLvlClst.contains(pid)
            if i>=0:
                highLvlClst.delete(pid, i)
                return
        try:
            centerInd = self.centers.index(DP(pid,0,0))
        except:
            centerInd = 0
        # delete center
        if centerInd>=0:
            lowLvlClusters = self.unClustered.union(set.union(*(set(hlc.clusters) for hlc in self.Clusters[centerInd:])))
            unclstCtrs = self.centers[centerInd:]
            del self.Clusters[centerInd:]
            del self.centers[centerInd:]
            self.reCluster(lowLvlClusters, unclstCtrs)
        # delete unclustered point
        else:
            for llc in self.unClustered:
                if llc.contains(pid):
                    llc.remove(pid)
    
    def reCluster(self, lowLvlClsts, pts):
        cnt = len(self.Clusters)
        while cnt<self.k and len(lowLvlClsts)>0:
            randClust = random.sample(lowLvlClsts, 1)[0]
            if len(randClust.points)>0:
                C = random.sample(randClust.points, 1)[0]
                randClust.points.discard(C)
            else:
                C = randClust.center
                lowLvlClsts.discard(randClust)
            within2R = list(filter(lambda clst: pntClstDist(C, clst)<=2*self.R, lowLvlClsts))
            newHighLvlClst = HighLvlCluster(C, self.r, within2R)
            self.centers.append(C)
            self.Clusters.append(newHighLvlClst)
            lowLvlClsts = lowLvlClsts.difference(within2R)
            cnt += 1
        self.unClustered = lowLvlClsts
        # recollect centers
        for p in pts:
            self.insert(p)
        


class HighLvlCluster(object):
    def __init__(self, c:DataPoint, r:float, clusters:List[Cluster]):
        self.center = c
        self.r = r
        self.clusters = clusters if clusters is not None else []
    def contains(self, pid):
        for i in range(0, len(self.clusters)):
            if self.clusters[i].contains(pid) or self.clusters[i].center.id==pid:
                return i
        return -1
    def insert(self, p):
        for cluster in self.clusters:
            if p.sphereDist(cluster.center) <= 2*self.r:
                cluster.insert(p)
                return True
        return False
    def delete(self, pid, clstId):
        if self.clusters[clstId].center.id == pid:
            self.reCluster(clstId)
            return
        self.clusters[clstId].remove(pid)
    def reCluster(self, clstId):
        X = set.union(*(clst.points for clst in self.clusters[clstId:]))
        X = X.union(set(clst.center for clst in self.clusters[clstId:]))
        del self.clusters[clstId:]
        while len(X)>0:
            c = random.sample(X, 1)[0]
            X.discard(c)
            within2r = set(filter(lambda p: p.sphereDist(c)<=2*self.r and p!=c, X))
            self.clusters.append(Cluster(c, within2r))
            X.discard(c)
            X = X.difference(within2r)


def pntClstDist(p, Clst):
    d = p.sphereDist(Clst.center)
    if d < Clst.radius:
        return 0
    return d #+ Clst.radius