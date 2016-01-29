import scisoftpy as dnp


class PeakFinder(Object):
    def __init__(self, file):
        self.dataSet = None
        
        self.getDataSet(file)

    def getDataSet(self, fName):
        nxsTree = dnp.io.load(fName)
        dataSet = dnp.asarray(nxsTree['/entry/result/data'])
        self.dataSet = dataSet.squeeze()
    
    def getWedge(self, i):
        return self.dataSet[i,:]