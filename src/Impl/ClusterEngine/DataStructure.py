from Impl.ClusterEngine.Cluster import Cluster
from Impl.ClusterEngine.UnClustered import UnClustered

class DataStructure(object):
    def __init__(self, r):
        self.radius = r
        self.Clusters = []
        self.unClustered = set()
        self.centers = []
    
    def createCluster(self, p):     # p is a DataPoint
        self.Clusters.append(Cluster(p.id))
    
    def insert(self, p):
        for c in self.centers:
            if p.distanceTo(c) <= 2*self.radius:
                # self.Clusters.insert(p)
                return
        self.unClustered.add(p)

    def delete(self, pid):
        for cluster in self.Clusters:
            if cluster.contains(pid):
                cluster.remove(pid)
                break
        for i in range(0,len(self.centers)):
            if self.centers[i] == pid:
                del self.centers[i:]
                self.reCluster(self.Clusters[i:])
                break

    def reCluster(self,clusters):
        pass
