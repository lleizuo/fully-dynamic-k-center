from Impl.ClusterEngine.DataStructure import DataStructure
from Impl.DataSource.DataRetriever import DataRetriver
from Impl.DataCache.Cache import Cache
def main():
    cache = Cache()
    dataSource = DataRetriver({'dataset':'dataset1',
                               'operation-file':'',
                               'dimension':2})
    dataSource.loadData(cache)
    dataStructure = DataStructure(2, 2)
    dataStructure.simpleClustering(cache.allPoints)

if __name__ == "__main__":
    main()