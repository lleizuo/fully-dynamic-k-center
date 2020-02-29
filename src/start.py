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
    dataSource.loadData(cache, config['max-records'])
    dataStructure = tryCluster(config['dmin'], config['dmax'], config['sigma'], config['k'], cache.allPoints)
    # dataStructure.show()
    print("done")
    cmd = input().split()
    while len(cmd) > 0:
        if cmd[0] == "insert":
            dataStructure = insert(dataStructure, float(cmd[1]), float(cmd[2]))
        elif cmd[0] == "delete":
            dataStructure = delete(dataStructure, int(cmd[1]))
        elif cmd[0] == "compute":
            dataStructure = compute(dataStructure)
        else:
            print("invalid command")
        # dataStructure.show()
        cmd = input().split()


def tryCluster(dmin:float, dmax:float, sigma:float, k:int, X:set):
	i = 1
	r = pow(1+sigma, i)
	while r < dmin:
		i += 1
		r = pow(1+sigma, i)
	while r <= dmax:
		dataStructure = DataStructure(r, k)
		dataStructure.simpleClustering(X)
		if len(dataStructure.unClustered) > 0:
			X = dataStructure.dispose()
			i += 1
			r = pow(1+sigma, i)
			continue
		return dataStructure

def delete(L:DataStructure, pid:int):
    if len(L.unClustered) == 0:
        L.delete(pid)
    return L

def insert(L:DataStructure, x:float, y:float):
    if len(L.unClustered) == 0:
        L.insert(x, y)
    return L

def compute(L:DataStructure):
    if len(L.unClustered) == 0:
        print("---------- Stability of deletion----------")
        pid = int(input("input pid of point to be deleted: "))
        c1 = L.refineForHam()
        deletedP = L.delete(pid)
        if len(L.unClustered)==0 and (deletedP is not None):
            index = L.retroAdd(deletedP)
            c2 = L.refineForHam()
            h = Ham.hammingDist(c1, c2)
            L.retroDelete(deletedP, index)
            print("Stability under Hamming distance is", h)
        else:
            print("Unable to calculate stability")
    else:
        print("Unable to calculate stability")
    return L



if __name__ == "__main__":
    main()