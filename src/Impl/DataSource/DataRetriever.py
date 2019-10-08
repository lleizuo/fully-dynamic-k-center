#!/usr/bin/python
import sys
import thread
from Base.temp import MsgType

class DataRetriver:
    def __init__(self, config, dataCache):
        self.dataCache = dataCache
        self.filePath = config['dataset']
        self.operationPath = config['operation-file']
        self.dataDimension = config['dimension']


    # load data from dataset file
    def loadData(self):  
        dataFile = open(self.filePath, "r")
        line = dataFile.readline()
        while line:
            self.parseData(line)
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


    # parse data
    def parseData(self, line):
        # use regex or something else to parse data to data points
        dp = None
        self.feedCache(MsgType.FULL, dp)
        


    # parse operation
    def parseOperation(self, line):
        dp = None
        self.feedCache(MsgType.DELTA, dp)
        pass


    def feedCache(self, dataType, data):
        try:
            thread.start_new_thread(self.dataCache.insert, (dataType, data))
        except:
            print "Error: unable to create thread"