from randwalkgraph import *
import node2vecAlgorithm
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from node2vecAlgorithm import *
"""
Logistic regression testing:
- Read graph
- split
- get graph's embeddings
- combine with op
- label as such: has edge -- 1. No edge -- 0
    - use equal number of edge and no edge
- train logreg
- predict on the test set by computing AUC
"""
gr = RandWalkGraph()
filename = input("Give graph file name: ")
gr.readFromFile(filename)



# read from edge list
embeddingNames = input("embedding file name: ")
def splitGraph(train,test,p,q,embeddingNames):
    """
    Function that gets the relevant structures
    Returns traingraph,test,classifier,nodeToEmb
    """
    traingraph = RandWalkGraph()
    traingraph.readFromEdgeList(train)
    # - get graph's embeddings
    d, r, l, k = 128, 10, 80, 10
    
    learnFeatures(traingraph, d, r, l, k, p, q, filename=embeddingNames)
    nodeToEmb = readFromFeatures(embeddingNames)
    # print(nodeToEmb.keys())
    # build the nonexistent set
    count = 0
    nonexistentset = set()
    while count < len(traingraph.nodeList):
        n1 = random.choice(traingraph.nodeList)
        n2 = traingraph.nonexistentLink(n1)
        if (n1, n2) not in nonexistentset and (n2, n1) not in nonexistentset:
            nonexistentset.add((n1, n2))
            count += 1
    nonexistentlist = list(nonexistentset)
    # - combine with op
    op = np.multiply
    trainX = []
    ylabels = []
    # add the nonexistent links and existent links to the trainX array
    for edgeSet in traingraph.edgePrs, nonexistentlist:
        label = 1
        if edgeSet is nonexistentlist:
            label = 0
        for u, v in edgeSet:
            rep = op(nodeToEmb[u], nodeToEmb[v])
            trainX.append(rep)
            ylabels.append(label)
    trainX = np.array(trainX)
    ylabels = np.array(ylabels)

    classifier = LogisticRegression()
    classifier.fit(trainX, ylabels)
    # - label as such: has edge -- 1. No edge -- 0
    #     - use equal number of edge and no edge
    # - train logreg
    # - predict on the test set by computing AUC
    results = classifier.predict(trainX)
    return traingraph,test,classifier,nodeToEmb

def AUC(traingraph:"RandWalkGraph",test,classifier:LogisticRegression,operator,nodeToEmb,n=1000) -> float:
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
    # train,test = g.testProbeSplit()
    nprime = 0
    n2prime = 0
    # n = 0
    # traingraph = RandWalkGraph()
    # traingraph.readFromEdgeList(train)
    for i in range(n):
        u,v = random.choice(test)
        if u not in traingraph.adjList or v not in traingraph.adjList:
            probescore = 0
        else:
            uemb = nodeToEmb[u]
            vemb = nodeToEmb[v]
            probescore = classifier.predict(np.expand_dims(operator(uemb,vemb),axis=0))

        rand = random.choice(traingraph.nodeList)
        other = traingraph.nonexistentLink(rand)
        nonexistent = classifier.predict(np.expand_dims(operator(nodeToEmb[rand],nodeToEmb[other]),axis=0))
        if probescore > nonexistent:
            nprime += 1
        else:
            n2prime += 1
    return (nprime+n2prime/2)/n

bestAUC = 0
bestP, bestQ = 1,1
with open(filename+"parametersearch.txt","w") as f:
    print("p q AUC",file=f)
    for p in [0.5,0.25,1,4]:
        for q in [0.5,0.25,1,4]:
            train, test = gr.testProbeSplit()
            traingraph,test,classifier,nodeToEmb = splitGraph(train,test,p,q,embeddingNames)
            op = np.multiply
            auc = AUC(traingraph,test,classifier,op,nodeToEmb,n=1000)
            if auc > bestAUC:
                bestAUC = auc
                bestP,bestQ = p,q
            print(p,q,auc,file=f)
        

print("Best: ",bestP,bestQ,bestAUC)