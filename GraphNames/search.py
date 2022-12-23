"""
Does BFS to find shortest link between characters
https://www.geeksforgeeks.org/print-all-shortest-paths-between-given-source-and-destination-in-an-undirected-graph/
"""
from collections import deque
from re import search
import random
# build graph
adjList = {}
with open('graphAdjList.txt',"r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.split(",")
        u = line[0].strip()
        name = line[1].strip()
        adj = list()
        for l in range(2,len(line)):
            l1 = line[l].strip()
            if len(l1) > 0:
                adj.append(l1)
        adjList[u] = dict(name=name,adjacent=adj)
        # print(adjList)
print(len(adjList))
# print(adjList[list(adjList.keys())[0]])
print(len(adjList['/wiki/Gandalf']['adjacent']))
# search
def bfs(sourceId, targetId, adjacencyList):
    """
    sourceId - the start node's Id
    targetId - the target's wiki path
    adjacenyList - dict[str:dict(str:str|list)] the adjaceny list. get adjacenies by adjacencyList[node]['adjacent']
    Conducts bfs to find shortest 
    """
    queue = deque()
    queue.append((sourceId,0)) # keep track of the length of path
    parents = dict()
    while len(queue) > 0:
        node,dist = queue.popleft()
        if node not in parents:
            parents[node] = None
        if node == targetId:
            return parents, dist
        newdist = dist+1
        for adj in adjacencyList[node]['adjacent']:
            if adj not in parents:
                queue.append((adj,newdist))
                parents[adj] = node
    return None

parents,pathLen = bfs('/wiki/Tulkas',"/wiki/Snaga_(orc_of_Mordor)",adjList)
# reconstruct path
path = []
p = "/wiki/Snaga_(orc_of_Mordor)"
while p is not None:
    path.append(p)
    p = parents[p]
path.reverse()
print(path)
print(pathLen)
# average degrees of separation:
# count = 0
# totalLen = 0
# for u in random.sample(list(adjList.keys()),100):
#     for v in random.sample(list(adjList.keys()),100):
#         if u!=v:
#             pathLen = bfs(u,v,adjList)
#             if pathLen is not None:
#                 count += 1
#                 totalLen += pathLen
#         print(count)
#         if 500 < count < 1000:
#             print("Degrees of LOTR universe separation: ",totalLen/count)
#             exit()
# Degrees of LOTR universe separation:  2.8922155688622753 ~ 3