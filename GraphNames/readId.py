"""
Purpose of this file is to put the id and names into a txt format
"""
import pickle
idgraph = pickle.load(open("idgraph.pkl","rb"))
count = 0
for key in idgraph:
    print(idgraph[key])
    count += 1
    if count == 10:
        break

# sort the id by number of edges
idlist = list(idgraph.keys())
idlist.sort(key=lambda a:len(idgraph[a]["edges"]),reverse=True)
# 1. write to file separated by "," id -- name
with open("idtoname.csv","w") as f:
    for identifier in idlist:
        print(identifier,",",idgraph[identifier]["name"].encode("UTF-8").decode("UTF-8"),file=f)

