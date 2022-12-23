from matplotlib import test
from NodeSimilarities import *
from graph import *
from typing import *
testfuncs = [commonNeighborsimilarity,hubDepressedsimilarity,
hubpromottedsimilarity,lhn1similarity,adamicadarSimilarity,mySimilarityIndex]

filename = input("Give name of graph to evaluate: ")
# averageOver = int(input("Average over how many times? "))

g:"Graph" = Graph()
g.readFromFile(filename)
# print(448 in g.nodeList)
# print(sorted(g.nodeList))
# for k in range(0,458):
#     if k not in g.nodeList:
#         print(k)
with open(filename+'.precision2.txt','w') as file:
    for f in testfuncs:
        avg = 0 # averaged over 10 runs
        numruns = 10
        name = f.__name__
        for i in range(numruns):
        
            myPres=precision(g,f)
            avg += myPres
        avg /= numruns
        print(name,myPres,file=file)
    file.close()