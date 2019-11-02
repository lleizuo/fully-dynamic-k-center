class SetBase(object):
    def __init__(self):
        self.numOfPoints = 0
        self.set = set()
    def contains(self, pid):
        if self.set.__contains__(pid):
            return True
        return False
    def add(self,pid):
        self.set.add(pid)
        self.numOfPoints += 1