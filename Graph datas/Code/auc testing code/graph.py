from xml.dom.minicompat import NodeList
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

    def readFromEdgeList(A,l):
        """
        Builds from list containing tuples of edges between nodes
        """
        for u,v in l:
            A.addEdge(u,v)
        A.nodeList = list(A.adjList.keys())
    

    def addEdge(A,source,target):
        if source not in A.adjList:
            A.adjList[source] = set()

        if target not in A.adjList:
            A.adjList[target] = set()
        if target not in A.adjList[source]:
            A.adjList[source].add(target)
            A.adjList[target].add(source)
            A.edgePrs.append((source,target))

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


    def testProbeSplit(A):
        """
        Divides the edges into training and probe sets. 90 10 split
        """
        # randomly sample 90% of edges into a train and probe set
        train,probe = train_test_split(A.edgePrs,test_size=0.1)
        return train,probe

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
            print("switched")
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