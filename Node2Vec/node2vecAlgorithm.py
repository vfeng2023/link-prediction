from randwalkgraph import *
from typing import *
from gensim.models import Word2Vec
def getWalks(graph:"RandWalkGraph",l,r, p,q):
    walks = []
    for i in range(r):
        print("Walk ",i," obtained")
        for u in graph.nodeList:
            walk = graph.weightedWalk(u,l,p,q)
            # walk = graph.randomWalkwithRestart(u,l,0.1)
            # print("Walk: ",walk)
            walks.append(walk)
    return walks
def learnFeatures(graph:"RandWalkGraph",d,r,l,k,p,q,filename = "embeddings.eb"):
    """
    graph = G
    Dimensions = d
    Walks per Node = r
    Length of walks = l
    Context size = k
    Parameters p and q
    """
    walks = getWalks(graph,l,r,p,q)
    print("Training model")
    print(len(graph.edgePrs))
    # print(len(walks))
    model = Word2Vec(sentences=walks,vector_size=d,window=k,min_count=1,workers=4,epochs=10)
    print("Model done training!")
    model.wv.save_word2vec_format(filename)

def readFromFeatures(filename):
    """
    Takes embedding file as input
    Readsd from that embedding file
    """
    nodeToEmbedding = dict()
    with open(filename,"r") as f:
        lines = f.readlines()
        n, emb_size = tuple(map(int,lines[0].split()))
        all_embeddings = []
        for line in lines[1:]:
            # line = lines[i]
            # vals = line.split()
            # myId = int(vals[0])
            # all_embeddings.append(list(map(float,vals[1:])))
            # idtoIdx[myId] = len(all_embeddings)-1
            line = line.split()
            node = int(line[0])
            emd = np.array(list(map(float,line[1:])))
            nodeToEmbedding[node] = emd
    return nodeToEmbedding
    # arr = np.array(all_embeddings)
def main():
    graphname = "lotredges.txt"# input("Graph filename: ")
    myGraph = RandWalkGraph()
    myGraph.readFromFile(graphname)
    learnFeatures(myGraph,128,10,80,10,1,1)


if __name__=="__main__":
    main()



    