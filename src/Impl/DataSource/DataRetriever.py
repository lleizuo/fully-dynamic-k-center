import os
import threading
import re
from Base.temp import MsgType
from Impl.DataCache.Cache import Cache

class DataRetriver:
    def __init__(self, config):
        # self.dataCache = dataCache
        self.filePath = config['dataset']
        self.operationPath = config['operation-file']
        self.dataDimension = config['dimension']


    # load data from dataset file
    def loadData(self, cache):  
        script_dir = os.path.dirname(__file__)
        rel_path = "../../Data/dataset1"
        abs_file_path = os.path.join(script_dir, rel_path)
        dataFile = open(abs_file_path, "r")
        line = dataFile.readline()
        while line:
            (x,y) = self.parseData(line)
            if (x,y) is not None:
                self.feedCache(x, y, cache)
            line = dataFile.readline()
        dataFile.close()


    # load operation from operation file
    def getOperations(self):
        operationFile = open(self.operationPath, 'r')
        line = operationFile.readline()
        while line:
            self.parseOperation(line)
            line = operationFile.readline()
        operationFile.close()


    # use regular expression to parse data
    def parseData(self, line):
        r = re.match(r"^\((.*),(.*)\)$", line)
        if r:
            return (float(r.groups()[0]), float(r.groups()[1]))
        return None
        
    # parse operation
    def parseOperation(self, line):
        dp = None
        return dp

    # add the data point into cache
    def feedCache(self, x, y, cache):
        print(x, y)
        cache.feed(x, y)
        pass
