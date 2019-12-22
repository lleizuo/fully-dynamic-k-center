from Impl.ClusterEngine.DataStructure import DataStructure
from Impl.DataSource.DataRetriever import DataRetriver
from Impl.DataCache.Cache import Cache
import json
def main():
    cache = Cache()
    with open('config.json') as config_file:
        config = json.load(config_file)
    dataSource = DataRetriver(config['dataset'], config['operation-file'])
    dataSource.loadData(cache)
    dataStructure = DataStructure(config['radius'], config['k'])
    dataStructure.simpleClustering(cache.allPoints)
    
    pid = int(input())
    dataStructure.delete(pid)
    
    dummy = input()


if __name__ == "__main__":
    main()