"""
    Goals for id assignment:
    Current state of graphAdjList.txt: you have a list node nodes, with the url, title, followed by neighbors
    Goal: create an dictionary with numeric id mapping to name and edges
    Then, convert the dictionary to a json format than can be used to graph in cytoscape
    Cytoscape formating: https://js.cytoscape.org/#notation/elements-json
"""
import pickle
with open('graphAdjList.txt','r') as myFile:
    myLines = myFile.readlines()
    currId = 0
    idgraph = dict() # dict(int:{name: "namestring",edges})
    urltoid = dict() # get numeric id from url
    idtourl = dict() # get url from numeric id
    for line in myLines:
        line = [s.strip() for s in line.split(",") if not s.isspace() and len(s) > 0]
        print(line)
        # input()
        url = line[0]
        # print(url)
        name = line[1]
        edges = list(set(line[2:]))
        idgraph[currId] = dict(name=name,edges=edges)
        urltoid[url] = currId
        idtourl[currId] = url
        currId += 1

# print(idgraph)
for id in idgraph:
    for i in range(len(idgraph[id]["edges"])):
        edgeurl = idgraph[id]["edges"][i]
        # print(edgeurl)
        # if edgeurl not in urltoid:
        #     urltoid[edgeurl] = currId
        #     idtourl[currId] = edgeurl
        #     idgraph[id] = dict(name=edgeurl[6:],edges=[])

        idgraph[id]["edges"][i] = urltoid[edgeurl]

count = 0
for key, value in idgraph.items():
    print(key,value)
    count += 1
    if count == 10:
        break

pickle.dump(idgraph,open("idgraph.pkl","wb"))
pickle.dump(idtourl,open("idtourl.pkl","wb"))
pickle.dump(urltoid,open("urltoid.pkl","wb"))