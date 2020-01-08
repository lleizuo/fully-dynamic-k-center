from Impl.ClusterEngine.DataStructure import DataStructure
from Impl.DataSource.DataRetriever import DataRetriver
from Impl.DataCache.Cache import Cache
from Impl.Stability import HammingDist as Ham
import json
def main():
    cache = Cache()
    with open('config.json') as config_file:
        config = json.load(config_file)
    dataSource = DataRetriver(config['dataset'], config['operation-file'])
    dataSource.loadData(cache)
    dataStructure = DataStructure(config['radius'], config['k'])
    dataStructure.simpleClustering(cache.allPoints)
    dataStructure.show()
    
    if len(dataStructure.unClustered) == 0:
        pid = int(input("input pid of point to be deleted: "))
        c1 = dataStructure.refineForHam()
        deletedP = dataStructure.delete(pid)
        dataStructure.show()
        if len(dataStructure.unClustered)==0 and not (deletedP is None):
            index = dataStructure.retroAdd(deletedP)
            c2 = dataStructure.refineForHam()
            h = Ham.hammingDist(c1, c2)
            dataStructure.retroDelete(deletedP, index)
            print("Stability under Hamming distance is", h)
    
    dummy = input()


if __name__ == "__main__":
    main()