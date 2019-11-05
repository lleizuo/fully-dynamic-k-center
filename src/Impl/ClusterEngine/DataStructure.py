from Impl.ClusterEngine.Cluster import Cluster
from Impl.ClusterEngine.UnClustered import UnClustered
from Impl.DataCache.DataPoint import DataPoint
import random

class DataStructure(object):
    def __init__(self, r: float, k: int):
        self.radius = r
        self.numOfClusters = k
        self.Clusters = []
        self.unClustered = set()
        self.centers = []
    
    
    # the 2-appximation clustering algorithm. X is the set of points
    def simpleClustering(self, X:set):
        unclusteredPoints = X
        counter = 0
        while len(unclusteredPoints) > 0 and counter<self.numOfClusters:
            c = random.sample(unclusteredPoints,1)[0]                                # the random selected center
            withIn2r = set(filter(lambda p: p.distanceTo(c)<=2*self.radius, 
                                  unclusteredPoints))
            newCluster = Cluster(c, withIn2r)    
            self.Clusters.append(newCluster)
            self.centers.append(c)
            unclusteredPoints = unclusteredPoints.difference(withIn2r)
            counter += 1
        if len(unclusteredPoints) > 0:
            self.unClustered = unclusteredPoints
        self.show()

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
                break
        pos = self.centers.index(DataPoint(pid,-1,-1))
        if pos >= 0:
            self.centers = self.centers[:pos]
            for cluster in self.Clusters[:pos]:
                self.unClustered = self.unClustered.union(cluster.points)
            self.Clusters = self.Clusters[:pos]
            self.reCluster(self.unClustered, self.numOfClusters-pos+1)

    def reCluster(self, clusters, numOfClusters):
        pass

    def show(self):
        print("centers: ")
        print("\t%s" % self.centers)
        print("Clusters: ")
        print("\t%s" % self.Clusters)
        print("Unclustered points: ")
        print("\t%s" % self.unClustered)