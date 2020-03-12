from Impl.ClusterEngine.DataStructure import DataStructure
from Impl.DataSource.DataRetriever import DataRetriver
from Impl.DataCache.Cache import Cache
from Impl.Stability import HammingDist as Ham
from Impl.Visualization.test import Plotter
import json
import multiprocessing as mp

def main():
    cache = Cache()
    with open('config.json') as config_file:
        config = json.load(config_file)
    dataSource = DataRetriver(config['dataset'], config['operation-file'])
    action = dataSource.loadData(cache, config['max-records'])
    next(action)
    print("finish loading initial data")
    dummy = input()

    dataStructure = tryCluster(config['dmin'], config['dmax'], config['sigma'], config['k'], cache.allPoints)
    print("finish clustering. Radius: ", dataStructure.radius)
    print(dataStructure.centers, "\ndone")
    dummy = input()
    if config['recluster-method']==1:
        testCf(dataStructure, action, cache)
    elif config['calc-stab']==True and config['visualize']==True:
        processCalcVsl(action, dataStructure, cache, config['draw-interval'])
    elif config['calc-stab']==True and config['visualize']==False:
        processCalc(action, dataStructure, cache)
    elif config['calc-stab']==False and config['visualize']==True:
        processVsl(action, dataStructure, cache, config['draw-interval'])
    else:
        processSld(action, dataStructure, cache)



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
			i += 1
			r = pow(1+sigma, i)
			continue
		return dataStructure

def processCalcVsl(action, L:DataStructure, cache:Cache, d:int):
    mp.set_start_method("forkserver")
    pl = Plotter()
    i = 0
    while True:
        if i%d==0:
            pl.plot(L)
        i += 1
        next(action)
        c1 = L.refineForHam()
        L.insert(cache.inserted)
        L.delete(cache.removed)
        c2 = L.refineForHam()
        print('Removed:', cache.removed, 'Inserted:', cache.inserted, 'stab:', Ham.hammingDist(c1, c2))
        dummy = input()
    pl.plot(L=None, finished=True)

def processVsl(action, L:DataStructure, cache:Cache, d:int):
    mp.set_start_method("forkserver")
    pl = Plotter()
    i = 0
    while True:
        if i%d==0:
            print("Sending centers1:", L.centers)
            pl.plot(L)
        i+=1
        next(action)
        print('Removed:', cache.removed, 'Inserted:', cache.inserted)
        L.insert(cache.inserted)
        print(L.Clusters)
        L.delete(cache.removed)
        print(L.Clusters)
        dummy = input()
    pl.plot(L=None, finished=True)
        

def processCalc(action, L:DataStructure, cache:Cache):
    while True:
        next(action)
        if cache.removed in [c.id for c in L.centers]:
            c1 = L.refineForHam()
            L.insert(cache.inserted)
            L.delete(cache.removed)
            c2 = L.refineForHam()
            # print(L.Clusters)
            stab = Ham.ari(c1, c2)
            if(stab<1):
                print('Removed:', cache.removed, 'Inserted:', cache.inserted,)
                print('stab:%.8f' % stab)
                print(L.centers)
        else:
            L.insert(cache.inserted)
            L.delete(cache.removed)
        # dummy = input()

def processSld(action, L:DataStructure, cache:Cache):
    while True:
        next(action)
        L.insert(cache.inserted)
        L.delete(cache.removed)
        print('Removed:', cache.removed, 'Inserted:', cache.inserted)
        dummy = input()

def testCf(L:DataStructure, action, cache):
    # print(L.centers)
    # print([len(cluster.points) for cluster in L.Clusters])
    # print('')
    while True:
        next(action)
        if cache.removed in [c.id for c in L.centers]:
            print('Removed:', cache.removed, 'Inserted:', cache.inserted)
            c1 = L.refineForHam()
            L.insert(cache.inserted)
            L.cfDelete(cache.removed)
            c2 = L.refineForHam()
            print(L.centers)
            # print([len(cluster.points) for cluster in L.Clusters])
            print('stab:%.8f'%Ham.ari(c1,c2))
            # dummy = input()
        else:
            L.insert(cache.inserted)
            L.cfDelete(cache.removed)


if __name__ == "__main__":
    main()