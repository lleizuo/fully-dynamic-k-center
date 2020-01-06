from Impl.ClusterEngine.Cluster import Cluster
from Impl.ClusterEngine.UnClustered import UnClustered
from Impl.DataCache.DataPoint import DataPoint
import random
from typing import List

class DataStructure(object):
    def __init__(self, r: float, k: int):
        self.radius = r
        self.numOfClusters = k
        self.Clusters : List[Cluster] = []              # list of clusters
        self.unClustered = set()        # set of unclustered points
        self.centers = []               # list of centers
    
    
    # the 2-appximation clustering algorithm. X is the set of points
    def simpleClustering(self, X:set):
        unclusteredPoints = X
        counter = 0
        while len(unclusteredPoints) > 0 and counter<self.numOfClusters:
            c = random.sample(unclusteredPoints,1)[0]                                # the random selected center
            withIn2r = set(filter(lambda p: p.distanceTo(c)<=2*self.radius and p!=c, 
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
        i = 0
        for c in self.centers:
            if p.distanceTo(c) <= 2*self.radius:
                self.Clusters[i].insert(p)
                return
            i += 1
        self.unClustered.add(p)

    def delete(self, pid: int):
        for cluster in self.Clusters:
            if cluster.contains(pid):
                cluster.remove(pid)
                self.show()
                return
        pos = self.centers.index(DataPoint(pid,-1,-1))
        if pos >= 0:
            self.unClustered = self.unClustered.union(set(self.centers[pos+1:]))
            self.centers = self.centers[:pos]
            for cluster in self.Clusters[pos:]:
                self.unClustered = self.unClustered.union(cluster.points)
            self.Clusters = self.Clusters[:pos]
            self.reCluster(self.numOfClusters-pos)
            self.show()

    def reCluster(self, numOfClusters:int):     # self.unClustered
        counter = 0
        while len(self.unClustered) > 0 and counter<numOfClusters:
            c = random.sample(self.unClustered,1)[0]                                # the random selected center
            withIn2r = set(filter(lambda p: p.distanceTo(c)<=2*self.radius and p!=c, 
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
        return result
    
    # add back the deleted point to obtain same cardinality for the convenience of computing stability
    def retroAdd(self, deletedPoint:DataPoint) -> int:
        index = self.centers.index(min(self.centers, key=lambda c: c.distanceTo(deletedPoint)))
        if index>=0:
            self.Clusters[index].insert(deletedPoint)
        return index

    def retroDelete(self, deletedPoint:DataPoint, index:int) -> int:
        self.Clusters[index].remove(deletedPoint.id)

    def show(self):
        print("centers: ")
        print("\t%s" % self.centers)
        print("Clusters: ")
        print("\t%s" % self.Clusters)
        print("Unclustered points: ")
        print("\t%s" % self.unClustered)