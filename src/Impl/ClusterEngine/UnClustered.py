from Base.SetBase import SetBase
class UnClustered(SetBase):
    def __init__(self, unclusterdPoints):
        super.__init__(self)
        self.set = unclusterdPoints
        self.numOfPoints = unclusterdPoints.__length__()