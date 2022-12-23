import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
filename = "lotrembeddings.eb"# "lotrembeddings.eb"# input("Name of the embedding file: ")

idtoIdx = dict()
with open(filename,"r") as f:
    lines = f.readlines()
    n, emb_size = tuple(map(int,lines[0].split()))
    all_embeddings = []
    for i in range(1, n+1):
        line = lines[i]
        vals = line.split()
        myId = int(vals[0])
        all_embeddings.append(list(map(float,vals[1:])))
        idtoIdx[myId] = len(all_embeddings)-1

    arr = np.array(all_embeddings)
# open the embedding file

idnames = {}
orderedIds = []
with open("idtoname.csv","r") as f:
    lines = f.readlines()
    for line in lines:
        charId, name = line.split(",")
        charId = int(charId)
        idnames[charId] = name.strip()
        orderedIds.append(charId)

# list of top 10 idx and names of the idx
# top50 = [idtoIdx[orderedIds[i]] for i in range(50)]
# top50Names = [idnames[i] for i in top50]
# call pca
# plt = matplotlib.pyplot.figure()
model = PCA(n_components=50)
model.fit(arr)
results = model.transform(arr)
print("PCA done!")
# call tsne on the results to get pro di
tmodel = TSNE(perplexity=50,early_exaggeration=50,learning_rate="auto")
plotVals = tmodel.fit_transform(results)
print("TNSE Done")
plt.rcParams["figure.figsize"] = (20,20)
plt.scatter(plotVals[:,0],plotVals[:,1])
# annotate the points
for i in range(len(orderedIds)):
    if orderedIds[i] in idtoIdx:
        idx = idtoIdx[orderedIds[i]]
        name = idnames[orderedIds[i]]
        plt.annotate(name,plotVals[idx],fontsize=7)

# plt.set_figwidth(10)
# plt.set_figheight(10)
plt.savefig("lotrplot.png",dpi=300)
# plt.show()