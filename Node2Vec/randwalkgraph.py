import graph
import numpy as np
import random
from typing import *
class RandWalkGraph(graph.Graph):
    def __init__(self):
        super().__init__()

    
    def aliasSample(self,neighborSet,startnode, prevNode,p,q):
        """
        https://www.keithschwarz.com/darts-dice-coins/
        1/p if dtx = 0
        1 if dtx = 1
        1/q if dtx = 2
        """
        # assign weights to the each of the nodes in start nodes
        vals = list(neighborSet)
        if prevNode > 0:
            prevSet = self.getNeigbors(prevNode)
        else:
            prevSet = set()
        unnormedProbs = []
        for v in vals:
            if v == prevNode:
                unnormedProbs.append(1/p)
            elif v in prevSet:
                unnormedProbs.append(1)
            else:
                unnormedProbs.append(1/q)
        probVec = np.array(unnormedProbs)
        probVec/=sum(probVec)
        # randomly sample an index from this set of nodes
        choiceIdx = np.random.choice(probVec.shape[0],p=probVec)
        return vals[choiceIdx]
        
        
    def weightedWalk(self,x,length,p,q):
        """
        Returns a sequence of random walks starting at node x, weighted by the parameters p and q
        x = starting node
        length = length of random walk
        p,q = parameters to weight graph
        """
        walk = [x]
        for i in range(length):
            curr = walk[-1]
            possNext = self.getNeigbors(curr)
            prev = -1
            if len(walk) >= 2:
                prev = walk[-2]
            s = self.aliasSample(possNext,curr,prev,p,q)
            walk.append(s)
        return walk
    def randomWalkwithRestart(self,x:int,length:int,c:float=0.9) -> List[int]:
        """
        Implements a random walk with restart, in contrast to the Weighted Random Walk used by the original Node2Vec paper
        Probability c that surfer goes to next node, probability 1-c that surfer returns to start node. Returns a list containing the walks
        """
        walk = [x]
        for i in range(length):
            curr = walk[-1]
            possNext = list(self.getNeigbors(curr))
            r = np.random.rand()
            if r < c:
                walk.append(random.choice(possNext))
            else:
                walk.append(x)
        return walk



        