from Impl.ClusterEngine.NestedClustDS import NestedClustDS
from Impl.DataSource.DataRetriever import DataRetriver
from Impl.DataCache.Cache import Cache
import json
import time

def main():
    cache = Cache()
    dataSource = DataRetriver("Data/timestamped_gps_coordinate.txt", "")
    action = dataSource.loadData(cache, 10000)
    next(action)
    print("finish loading initial data")
    dummy = input()

    L = tryCluster(2000, 20038000, 0.1, 10, cache.allPoints)
    print("finish clustering. Radius: ", L.R)
    print(L.centers, "\ndone")
    dummy = input()
    sldWin(action, L, cache)

def tryCluster(dmin, dmax, sig, k, X:set):
    i = 1
    r = pow(1+sig, i)
    while r < dmin:
	    i += 1
	    r = pow(1+sig, i)
    while r <= dmax:
	    L = NestedClustDS(r, k)
	    L.simpleClustering(X)
	    if len(L.unClustered) > 0:
	    	i += 1
	    	r = pow(1+sig, i)
	    	continue
	    return L

def sldWin(action, L:NestedClustDS, cache:Cache):
    # f = open("output", "w")
    cnt = 0
    start = time.time()
    while cnt<10000:
        next(action)
        L.insert(cache.inserted)
        L.delete(cache.removed)
        # print("Insert: %s, Delete: %s\n" % (cache.inserted, cache.removed))
        cnt += 1
        # dummy = input()
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()