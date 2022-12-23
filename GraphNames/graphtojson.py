# convert the graph in formate of {id:{name: "name","edges":[numbers ]}} to a json cytoscape can read
import json
import pickle
with open('idgraph.pkl','rb') as f:
    idgraph = pickle.load(f)

# print(idgraph)
# the graph format is such:
# elements: [] flat array of nodes and edges
# node: {group: "nodes",data:{id: "n0",name:"name"}}
# edge: {group: "edges",data: {id: "n1_n2", source: "nsource",target}}
# for key, value in idgraph.items():
#     print(key,value)
#     break
elements = []
for nodeId, dataDict in idgraph.items():
    toapp = dict()
    toapp["group"] = "nodes"
    toapp["data"] = {
        "id":str(nodeId),
        "name": dataDict["name"]
    }
    elements.append(toapp)
    for e in dataDict["edges"]:
        edgeDict = {
            "group":"edges",
            "data": {
                "id": str(nodeId)+"_"+str(e),
                "source":str(nodeId),
                "target":str(e)
            }
        }
        elements.append(edgeDict)

for i in range(10):
    print(elements[i])
with open("graph.json",'w') as f:
    json.dump(elements,f)