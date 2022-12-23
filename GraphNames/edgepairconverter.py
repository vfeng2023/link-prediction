import pickle
with open('idgraph.pkl','rb') as f:
    graph = pickle.load(f)

count = 0
# for key, val in graph.items():
    # print(key,val)
    # if count == 10:
    #     break
    # count += 1

with open("lotredges.txt",'w') as f2:
    for key, data in graph.items():
        for adj in data['edges']:
            print(key,adj,file=f2)
    f2.close()