"""
converts the elements in graph to numbers and ids, writes the graph (ids) and links to the id txt
"""

graphAdj = []
idToLink = dict() # dict mapping int to dict of name : string, url: string
linkToId = dict()
with open("graphAdjList.txt", "r") as f:
    lines = f.readlines()
    myId = 0
    for l in lines:
        l = l.split(",")
        url = l[0]
        name = l[1]
        idToLink[myId] = {
            "url": l[0],
            "name":l[1]
        }
        
        linkToId[url] = myId
        myId+= 1
        graphAdj.append()
        