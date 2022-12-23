# from xml.dom.minicompat import NodeList
import numpy
from sklearn.model_selection import train_test_split
import random
import pickle
class Graph:
    """
    Graph object contains a graph. On initialization, it initializes an empty adjacency list. 
    Graph is undirected.
    """
    def __init__(self):
        self.adjList = dict()
        self.edgePrs = []
        self.nodeList = []
        # self.size = -1 # Size = num Nodes
        self.revlist = dict()
        

    def readFromFile(A,filename):
        """
        Builds graph from file containing edge pairs
        """
        with open(filename,'r') as f:
            lines = f.readlines()
            for l in lines:
                l = l.split()
                start = int(l[0])
                target = int(l[1])
                A.addEdge(start,target)
                # A.edgePrs.append((start,target))
        A.nodeList = list(A.adjList.keys())
        A.revlist = dict()
        for k in range(len(A.nodeList)):
            A.revlist[A.nodeList[k]] = k
        # print("revlist",A.revlist)
        # print("edges",A.edgePrs)

    def readFromEdgeList(A,l):
        """
        Builds from list containing tuples of edges between nodes
        """
        for u,v in l:
            A.addEdge(u,v)
        A.nodeList = list(A.adjList.keys())
        A.revlist = dict()
        for k in range(len(A.nodeList)):
            A.revlist[A.nodeList[k]] = k

    def toAdjMat(self, myrev = None):
        if myrev is None:
            myrev = self.revlist
        # mat = numpy.zeros(shape = (self.size,self.size))
        # use the indices of the nodelist to assign things
        # 1. reverse nodelist
        
        # myMat = numpy.zeros((self.size,self.size))
        # for u,v in self.edgePrs:
        #     i1 = revlist[u]
        #     i2 = revlist[v]
        #     myMat[i1,i2] = 1
        #     myMat[i2,i1] = 1
        # return myMat
        
        # 2. create adjmat with length of nodelist
        arr = numpy.zeros(shape=(len(myrev),len(myrev)))
        # print("edgepairs: ",self.edgePrs)
        for u,v in self.edgePrs:
            # print(u,v)
            n1 = myrev[u]
            n2 = myrev[v]
            arr[n1,n2] = 1
            arr[n2,n1] = 1
        return arr
    def addEdge(A,source,target):
        if source not in A.adjList:
            A.adjList[source] = set()

        if target not in A.adjList:
            A.adjList[target] = set()
        if target not in A.adjList[source]:
            A.adjList[source].add(target)
            A.adjList[target].add(source)
            A.edgePrs.append((source,target))
            # A.edgePrs.append((target,source))
        # A.size = max(A.size,max(source,target))

    def getDegree(A,node):
        """
        Returns the degree of a node
        """
        return len(A.adjList[node])

    def getSharedNeighbors(A,u,v):
        """
        Returns the shared neighbors of two nodes
        """
        shared = A.adjList[u].intersection(A.adjList[v])
        # for node in A.adjList[u]:
        #     if node in A.adjList[v]:
        #         shared.append(node)
        return shared
    def getNumberSharedNeighbors(A,u,v):
        """
        Returns the total number of shared neigbors
        """
        return len(A.getSharedNeighbors(u,v))


    def testProbeSplit(A,test_size=0.1):
        """
        Divides the edges into training and probe sets. 90 10 split
        """
        # randomly sample 90% of edges into a train and probe set
        train,probe = train_test_split(A.edgePrs,test_size=test_size)
        # trainsize = len(train)
        # for i in range(trainsize):
        #     u,v = train[i]
        #     train.append((v,u))

        # testsize = len(probe)
        # for i in range(testsize):
        #     u,v = probe[i]
        #     train.append((v,u))
        return train,probe
    # def pageRank(self,transitionMatrix,n1,n2):
    #     i1 = self.revlist[n1]
    #     i2 = self.revlist[n2]
    #     return transitionMatrix[i1,i2] + 
    def toFile(self,name):
        with open(name,'w') as f:
            for u,v in self.edgePrs:
                print(u,v,file=f)
            f.close()
    def getNeigbors(A,node):
        return A.adjList[node]

    def nonexistentLink(A,node):
        randval = random.choice(A.nodeList)
        # print(A.nodeList)
        while randval in A.adjList[node]:
            randval = random.choice(A.nodeList)
            # print("switched")
        return randval
# g = Graph()
# g.readFromFile("lotredges.txt")
# print(g.getDegree(0))
# with open("savedLotr.pkl",'wb') as f:
#     pickle.dump(g,f)
#     f.close()
# print(g.getNumberSharedNeighbors(0,39))
# test,probe = g.testProbeSplit()
# print(len(test),len(probe))