import os
import re

class DataRetriver:
    def __init__(self, filePath, operationPath):
        # self.dataCache = dataCache
        self.filePath = filePath
        self.operationPath = operationPath
        # self.dataDimension = config['dimension']


    # load data from dataset file
    def loadData(self, cache, maxRecords):  
        script_dir = os.path.dirname(__file__)
        rel_path = "../../" + self.filePath
        abs_file_path = os.path.join(script_dir, rel_path)
        dataFile = open(abs_file_path, "r")
        line = dataFile.readline()
        i = 0
        while line and i<maxRecords:
            r = self.parseData(line, r"([0-9]+)[\t ]+(.+) (.+)")
            if r is not None:
                cache.feed(r[0], r[1])
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
    def parseData(self, line, p):
        # r = re.match(r"^\((.*),(.*)\)$", line)
        r = re.match(p, line)
        if r:
            return (float(r.groups()[1]), float(r.groups()[2]))
        # else:
        #     print("\n\n\n", line, "\n\n\n")
        return None
        
    # parse operation
    def parseOperation(self, line):
        dp = None
        return dp
