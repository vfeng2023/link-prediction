import pickle
from typing import *
from graph import *
from math import log10,sqrt
#mygraph: "Graph"= pickle.load('savedLotr.pkl')
def commonNeighborsimilarity(g:"Graph",node1:int,node2:int) -> int:
    """
        Returns a similarity value given two nodes
    """
    return g.getNumberSharedNeighbors(node1,node2)

def hubDepressedsimilarity(g:"Graph",node1:int,node2:int) -> float:
    """
    Return the hub depressed
    """
    sharedneighbors = g.getNumberSharedNeighbors(node1,node2)
    return sharedneighbors/min(g.getDegree(node1),g.getDegree(node2))

def hubpromottedsimilarity(g:"Graph", node1:int, node2:int) -> float:
    sharedneighbors = g.getNumberSharedNeighbors(node1,node2)
    return sharedneighbors/max(g.getDegree(node1),g.getDegree(node2))

def  lhn1similarity(g:"Graph",node1:int,node2:int):
    shared = g.getNumberSharedNeighbors(node1,node2)
    return shared/(g.getDegree(node1) * g.getDegree(node2))

def adamicadarSimilarity(g:"Graph",node1:int,node2:int) -> float:
    """
    Adamic-Adar Index: sum of 1/log(k) of shared neighbors
    """
    shared = g.getSharedNeighbors(node1,node2)
    toRet = 0
    for k in shared:
        if(g.getDegree(k)!=1):
            toRet += 1/(log10(g.getDegree(k)))
    return toRet

def mySimilarityIndex(g:"Graph",node1:int, node2:int):
    """
        Try using size of of shared neighbors as a coefficient to the adamic-adar index
        numbershared/(log product of node1 and node1)
    """
    val = log10(g.getDegree(node1))+log10(g.getDegree(node2))
    if abs(val) < 1e-9:
        return 0
    return g.getNumberSharedNeighbors(node1,node2) / val

def AUC(g:"Graph",simFunc,n=1000) -> float:
    """
    AUC = (n'+0.5n")/n, take n to be the size of the test set
    : Provided the rank of all non-observed links, the AUC value can be interpreted as the probability that a randomly
chosen missing link (i.e., a link in E
P
) is given a higher score than a randomly chosen nonexistent link (i.e., a link in U −E). In
the algorithmic implementation, we usually calculate the score of each non-observed link instead of giving the ordered list
since the latter task is more time consuming.4
Then, at each time we randomly pick a missing link and a nonexistent link to
compare their scores, if among n independent comparisons, there are n
′
times the missing link having a higher score and n
′′
times they have the same score, the AUC value is

    """
    train,test = g.testProbeSplit()
    nprime = 0
    n2prime = 0
    # n = 0
    traingraph = Graph()
    traingraph.readFromEdgeList(train)
    # for each node in test:
    # for i in range(len(test)):
    #     probescore = simFunc(g,test[i][0],test[i][1])
    #     rand = random.randint(1,len(g.adjList))
    #     other = g.nonexistentLink(rand)
    #     nonexistent = simFunc(g,rand,other)
    #     if probescore > other:
    #         nprime += 1
    #     else:
    #         n2prime += 1
    #     n += 1
    # print(n,nprime,n2prime)
    # return (nprime + n2prime/2)/n
    for i in range(n):
        u,v = random.choice(test)
        if u not in traingraph.adjList or v not in traingraph.adjList:
            probescore = 0
        else:
            probescore = simFunc(traingraph,u,v)

        rand = random.choice(traingraph.nodeList)
        other = traingraph.nonexistentLink(rand)
        nonexistent = simFunc(traingraph,rand,other)
        if probescore > nonexistent:
            nprime += 1
        else:
            n2prime += 1
    return (nprime+n2prime/2)/n
        
# g = Graph()
# g.readFromFile("lotredges.txt")
# # print(g.edgePrs)
# aucscore = AUC(g,mySimilarityIndex)
# print(aucscore)
# neighbors45 = g.getNeigbors(45)
# neighbors47 = (g.getNeigbors(47))
# print(g.getSharedNeighbors(45,47))
# print(neighbors45, "deg=",len(neighbors45))
# print(neighbors47,"deg=",len(neighbors47))
# print("common neighbors: ",commonNeighborsimilarity(g,45,47))
# print("hubdpressed: ",hubDepressedsimilarity(g,45,47))
# print("hubpromoted: ",hubpromottedsimilarity(g,45,47))
# print("LHN1 similarity: ",lhn1similarity(g,45,47))
# print("Adamic-Adar: ",adamicadarSimilarity(g,45,47))
# print("Mine: ",mySimilarityIndex(g,45,47))
# print("common neighbors: ",commonNeighborsimilarity(g,0,1))
#  = []
