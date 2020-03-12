from Impl.ClusterEngine.Cluster import Cluster
from Impl.ClusterEngine.UnClustered import UnClustered
from Impl.DataCache.DataPoint import DataPoint
import random
from itertools import chain
from typing import List, Set

class DataStructure(object):
    def __init__(self, r: float, k: int):
        self.radius = r
        self.numOfClusters = k
        self.Clusters : List[Cluster] = []              # list of clusters
        self.unClustered = set()        # set of unclustered points
        self.centers = []               # list of centers
        self.N = 0
        self.T = 0
    
    
    # the 2-appximation clustering algorithm. X is the set of points
    def simpleClustering(self, X:set):
        self.N = len(X)
        self.T = len(X)
        unclusteredPoints = X.copy()
        counter = 0
        while len(unclusteredPoints) > 0 and counter<self.numOfClusters:
            c = random.sample(unclusteredPoints,1)[0]                                # the random selected center
            withIn2r = set(filter(lambda p: p!=c and p.sphereDist(c)<=2*self.radius, 
                                  unclusteredPoints))
            newCluster = Cluster(c, withIn2r)    
            self.Clusters.append(newCluster)
            self.centers.append(c)
            unclusteredPoints = unclusteredPoints.difference(withIn2r)
            unclusteredPoints.discard(c)
            counter += 1
        if len(unclusteredPoints) > 0:
            self.unClustered = unclusteredPoints
        # self.show()

    # insert a datapoint
    def insert(self, p):
        # p = DataPoint(self.T, x, y)
        self.T += 1
        self.N += 1
        i = 0
        for c in self.centers:
            if p.sphereDist(c) <= 2*self.radius:
                self.Clusters[i].insert(p)
                return
            i += 1
        if len(self.centers) < self.numOfClusters:
            self.centers.append(p)
            self.Clusters.append(Cluster(p, set()))
            return
        self.unClustered.add(p)

    def delete(self, pid: int) -> DataPoint:
        for cluster in self.Clusters:
            if cluster.contains(pid):
                cluster.remove(pid)
                # self.T += 1
                self.N -= 1
                return
        try:
            pos = self.centers.index(DataPoint(pid,-1,-1))
        except:
            pos = -1
        if pos >= 0:
            # deletedP = self.centers[pos]
            self.unClustered = self.unClustered.union(set(self.centers[pos+1:]))
            self.centers = self.centers[:pos]
            for cluster in self.Clusters[pos:]:
                self.unClustered = self.unClustered.union(cluster.points)
            # print("ready to recluster points:", len(self.unClustered))
            self.Clusters = self.Clusters[:pos]
            self.reCluster(self.numOfClusters-pos)
            self.T += 1
            self.N -= 1
        elif DataPoint(pid, -1, -1) in self.unClustered:
            self.unClustered.discard(DataPoint(pid, -1, -1))

    def reCluster(self, numOfClusters:int):     # self.unClustered
        counter = 0
        while len(self.unClustered) > 0 and counter<numOfClusters:
            c = random.sample(self.unClustered,1)[0]                                # the random selected center
            withIn2r = set(filter(lambda p: p.sphereDist(c)<=2*self.radius and p!=c, 
                                  self.unClustered))
            newCluster = Cluster(c, withIn2r)    
            self.Clusters.append(newCluster)
            self.centers.append(c)
            self.unClustered = self.unClustered.difference(withIn2r)
            self.unClustered.discard(c)
            counter += 1
        # if len(unclusteredPoints) > 0:
        #     self.unClustered = unclusteredPoints

    # refine for Hamming distance calculation. Include centers in corresponding sets
    def refineForHam(self):
        result : List[set] = []
        for cluster in self.Clusters:
            s = set(p.id for p in cluster.points)
            s.add(cluster.center.id)
            result.append(s)
        if len(self.unClustered) > 0:
            result.append(set(p.id for p in self.unClustered))
        return result
    
    # add back the deleted point to obtain same cardinality for the convenience of computing stability
    def retroAdd(self, deletedPoint:DataPoint) -> int:
        nearestCenter = min(self.centers, key=lambda c: c.sphereDist(deletedPoint))
        if nearestCenter.sphereDist(deletedPoint) <= self.radius:
            index = self.centers.index(nearestCenter)
            return index
        elif len(self.Clusters) < self.numOfClusters:
            self.unClustered.add(DataPoint)
            return -1
        # index = self.centers.index(min(self.centers, key=lambda c: c.sphereDist(deletedPoint)))
        # if index>=0:
            # self.Clusters[index].insert(deletedPoint)
        # return index

    # delete the point inserted in retroAdd
    def retroDelete(self, deletedPoint:DataPoint, index:int) -> int:
        if index>=0:
            self.Clusters[index].remove(deletedPoint.id)
        else:
            self.unClustered.remove(deletedPoint)

    # constant factor algorithm (delete a center)
    def cfDelete(self, pid):
        for cluster in self.Clusters:
            if cluster.contains(pid):
                cluster.remove(pid)
                self.N -= 1
                return
        try:
            pos = self.centers.index(DataPoint(pid, 0, 0))
        except:
            pos = -1
        if pos>=0:
            cluster = self.Clusters[pos]
            p = cluster.nextCenter()
            if p is None:
                del self.centers[pos]
                del self.Clusters[pos]
                return
            self.centers = self.centers[:pos] + [p] + self.centers[(pos+1):]
            self.Clusters[pos].center = p
            self.Clusters[pos].points.remove(p)
            for cluster in self.Clusters[pos:]:
                self.unClustered = self.unClustered.union(cluster.points)
                cluster.points = set()
            self.cfReassign()
        else:
            self.unClustered.discard(DataPoint(pid, -1, -1))

    def cfReassign(self):
        clustered = set()
        for p in self.unClustered:
            index = self.centers.index(min(self.centers, key=lambda c: c.sphereDist(p)))
            if self.centers[index].sphereDist(p) <= 2*self.radius:
                self.Clusters[index].insert(p)
                clustered.add(p)
            elif len(self.centers) < self.numOfClusters:
                self.centers.append(p)
                self.Clusters.append(Cluster(p, set()))
                clustered.add(p)
        self.unClustered = self.unClustered.difference(clustered)
    # def cfReassign(self, R:List[DataPoint], X:Set[DataPoint]):
    #     clusters = []
    #     unclustered = set()
    #     for c in R:
    #         clusters.append(Cluster(c, set()))
    #     for p in X:
    #         index = R.index(min(self.centers, key=lambda c: c.sphereDist(p)))
    #         if R[index].sphereDist(p) <= 2*self.radius:
    #             clusters[index].insert(p)
    #         elif len(self.centers) < self.numOfClusters:
    #             R.append(p)
    #             clusters.append(Cluster(p, set()))
    #         else:
    #             unclustered.add(p)
    #     return (unclustered, clusters)

    def dispose(self):
        result = set(chain.from_iterable(p.points for p in self.Clusters))
        self.Clusters = None
        result = result.union(self.unClustered)
        self.unClustered = None
        result = result.union(set(self.centers))
        self.centers = None
        return result

    def show(self):
        print("radius: %f" % self.radius)
        print("centers: ")
        print("\t%s" % self.centers)
        print("Clusters: ")
        print("\t%s" % self.Clusters)
        print("Unclustered points: ")
        print("\t%s" % self.unClustered)