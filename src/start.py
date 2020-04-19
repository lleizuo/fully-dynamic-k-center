from Impl.ClusterEngine.DataStructure import DataStructure
from Impl.DataSource.DataRetriever import DataRetriver
from Impl.DataCache.Cache import Cache
from Impl.Stability import HammingDist as Ham
from Impl.Stability.Consistency import *
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
    if config['recluster-method']==0:
        if config['calc-stab']==True and config['stab-measure']==0:
            processCalc(action, dataStructure, cache)
        elif config['calc-stab']==True and config['stab-measure']==1:
            processCst(action, dataStructure, cache)
        elif config['visualize']==True:
            processVsl(action, dataStructure, cache, config['draw-interval'])
    elif config['recluster-method']==1:
        processCf(dataStructure, action, cache)




def tryCluster(dmin:float, dmax:float, sigma:float, k:int, X:set):
	i = 1
	r = pow(1+sigma, i)
	while r < 2000:
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
            # print("Sending centers1:", L.centers)
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
    f = open("output", "w")
    while True:
        next(action)
        if cache.removed in [c.id for c in L.centers]:
            c1 = L.refineForHam()
            L.insert(cache.inserted)
            L.delete(cache.removed)
            c2 = L.refineForHam()
            stab = Ham.ari(c1, c2)
            f.write('Removed: %s, Inserted: %s\n' % (cache.removed, cache.inserted))
            f.write('stab:%.8f\n' % stab)
            f.flush()
        else:
            L.insert(cache.inserted)
            L.delete(cache.removed)
        # dummy = input()
    f.close()

def processSld(action, L:DataStructure, cache:Cache):
    while True:
        next(action)
        L.insert(cache.inserted)
        L.delete(cache.removed)
        print('Removed:', cache.removed, 'Inserted:', cache.inserted)
        dummy = input()

def processCf(L:DataStructure, action, cache):
    f = open('output', 'w')
    while True:
        next(action)
        if cache.removed in [c.id for c in L.centers]:
            # print('Removed:', cache.removed, 'Inserted:', cache.inserted)
            c1 = L.refineForHam()
            L.insert(cache.inserted)
            L.cfDelete(cache.removed)
            c2 = L.refineForHam()
            stab = Ham.ari(c1, c2)
            f.write('Removed: %s, Inserted: %s\n' % (cache.removed, cache.inserted))
            f.write('stab:%.8f\n' % stab)
            f.flush()
        else:
            L.insert(cache.inserted)
            L.cfDelete(cache.removed)
    f.close()

def processCst(action, L:DataStructure, cache:Cache):
    f = open("output", "w")
    T = 0
    cumu = 0
    while True:
        next(action)
        if cache.removed in [c.id for c in L.centers]:
            centerSet1 = set(c.id for c in L.centers)
            L.insert(cache.inserted)
            L.delete(cache.removed)
            centerSet2 = set(c.id for c in L.centers)
            consistency = len(centerSet2.difference(centerSet1))
            cumu += consistency
            f.write("time T: %d, center diff: %d, cumulative diff: %d\n" % (T, consistency, cumu))
            f.flush()
        else:
            L.insert(cache.inserted)
            L.delete(cache.removed)
        T += 1   
    f.close()


if __name__ == "__main__":
    main()