# from matplotlib.pyplot import sci
import numpy as np
import scipy
import itertools
import scipy.sparse as sparse
import scipy.io as spio
import random
from typing import *
from graph import Graph
import statistics
"""
Purpose of pagerank_V2.py is to use existing framework (Graph class) to do testing.
Procedural, but no concepteual modifications
"""
# for i in range(0,edges.shape[0]//2+1):
#     for j in range(edges.shape[1]//2):
#         edges[i,j] = edges[j,i]

# print(type(edges))
# print(edges)
# find A
# horz axis is the 
def split(edges:"scipy.sparse.coo_matrix"):
    """
    returns a list of probe set edges, and test set edges.
    returns testrange, proberange
    m x n
    """
    # figure out how to divide the edges in the matrix 
    # 
    idxs = list(range(edges.getnnz()))
    random.shuffle(idxs)
    tenp = len(idxs)//10
    testrange = idxs[:tenp]
    proberange = idxs[tenp:]
    return testrange, proberange

def pagerank(edges,max_iter=100,tol=1.0e-6):
    colSum = np.sum(edges,axis=0)
    # print(colSum)
    # exit()
    A = edges/colSum
    p = 0.15
    N = A.shape[0]
    M = (1-p)*A + p/N

    # print(M)
    # print(colSum.shape)
    # print(A)
    # find M
    # find the pagerank vector --> Satisfys (M-I)x = 0
    # find Mx = x
    # power method
    
    # print(N)
    x = np.ones(shape=(N,1))/N
    # use the power method to approximate pagerank vector
    for i in range(max_iter):
        prev = x
        new_x = M@x
        x = new_x
        err = np.linalg.norm(x,ord=1)
        if err < tol:
            return x
    return M,x


def randwalkwrestart(edges,c=0.9):
    """
    Returns the matrix that gets you the steady state matrix starting from x
    M = (1-c)*(I-cP) # c varies between 0 and 1
    """
    N = edges.shape[0]
    P = edges/np.sum(edges,axis=0)
    invComp = np.linalg.inv(np.identity(N)-c*P)
    M = (1-c) * invComp
    return M
# result = randwalkwrestart(edges)
# print(result[1,4])
# result = pagerank(edges)
# print(result)

def AUC(edgeMat:"Graph",n=1000,c=0.9) -> float:
    """
    edgeMat is the coo format
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
    nprime = 0
    ndoubleprime = 0
    # random pair from edge matrix
    # denseEdge = edgeMat.toarray()
    train,probe = edgeMat.testProbeSplit()
    print(len(train),len(probe))
    traingraph = Graph()
    traingraph.readFromEdgeList(train)
    #traingraph = edgeMat
    probegraph = Graph()
    probegraph.readFromEdgeList(probe)
    # transMat,_ = pagerank(traingraph.toAdjMat(myrev=edgeMat.revlist))
    # transMat,_ = pagerank(edgeMat.toAdjMat())
    transMat = randwalkwrestart(traingraph.toAdjMat(myrev=edgeMat.revlist),c=c)
    # print(transMat)
    print()
    # print(pagerank(edgeMat.toAdjMat())[0])
    for owo in range(n):
        # pick random edge pair
        i1,i2 = random.choice(probegraph.edgePrs)
        source, target = edgeMat.revlist[i1],edgeMat.revlist[i2]
        # print("Source: ",source)
        # choose nonexistent link
        n1,n2 = random.sample(edgeMat.nodeList,2)
        while n1 in edgeMat.adjList[n2]:
            n1, n2 = random.sample(edgeMat.nodeList,2)
        # print(transMat)
        # do the score thing
        n1 = edgeMat.revlist[n1]
        n2 = edgeMat.revlist[n2]
        # print(type(source))
        existScore = transMat[source,target] + transMat[target,source]
        
        nonScore = transMat[n1,n2] + transMat[n2,n1]
        if existScore > nonScore:
            nprime += 1
        else:
            ndoubleprime += 1
            # print("hello")
    return (nprime + ndoubleprime/2)/n
# read matrix
# filename = "mammalia-dolphin-florida-social.edges"# input("Graph filename: ")
# graph = Graph()
# graph.readFromFile(filename)
# with open(filename,'r') as f:
#     adjMat = spio.mmread(f)
# set the weights correctly
# edges = (adjMat > 0).toarray()
# edges = edges.astype(int)
# tmat,_ = pagerank(edges)
# print(tmat)
# with open(filename+".pagerankaucwrtc.csv","w") as f:

#     i = 0.1
#     print("c,AUC score for ",filename,",standard deviation",file=f)
#     numberruns = 30
#     scores = 0
#     while i < 1:
#         avg = 0
#         scores = []
#         for k in range(numberruns):
#             result = AUC(graph,c=i)
#             avg += result
#             scores.append(result)
#         stddev = statistics.stdev(scores)
#         print(i, avg/numberruns,stddev,file=f)
#         print(avg/numberruns)
#         i += 0.1
#     f.close()


def precision(graph:"Graph",L=100):
    """
    Lr/L, number correct nodes out of total nodes
    """
    # split into train and test
    L = min(len(graph.adjList),L) 
    train,test = graph.testProbeSplit()
    traingraph = Graph()
    traingraph.readFromEdgeList(train)
    transMat = randwalkwrestart(graph.toAdjMat(myrev=graph.revlist),c=0.9)
    print(transMat)
    settestedge = set(test)
    # pair them up and score the pairs
    possedges = itertools.combinations(traingraph.nodeList,2)
    # take top L and calc precision
    scorelist = []
    scoredict = dict()
    for u,v in possedges:
        # score = myFunc(traingraph,u,v)
        n1 = graph.revlist[u]
        n2 = graph.revlist[v]
        score = transMat[n1][n2] + transMat[n2,n1]
        scoredict[u,v] = score
        scorelist.append((u,v))

    scorelist.sort(reverse=True,key=lambda a:scoredict[a])
    Lr = 0
    for k in range(L):
        u,v = scorelist[k]
        if (u,v) in settestedge or (v,u) in settestedge:
            Lr += 1
            print('counted')
    return Lr/L

# filename = "eco-florida.edges"# input("Graph filename: ")
# graph = Graph()
# graph.readFromFile(filename)
# print(precision(graph))