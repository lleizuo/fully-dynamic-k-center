import HammingDist as Ham
from typing import List

class StabilityCalculator(object):
    def calculate(self, clustering1:List[set], clustering2:List[set]):
        h = Ham.hammingDist(clustering1, clustering2)
        return h