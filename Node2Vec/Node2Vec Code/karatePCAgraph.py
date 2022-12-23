import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
filename = input("Name of the embedding file: ")

with open(filename,"r") as f:
    lines = f.readlines()
    n, emb_size = tuple(map(int,lines[0].split()))
    all_embeddings = []
    for i in range(1, n+1):
        line = lines[i]
        all_embeddings.append(list(map(float,line.split()[1:])))

    arr = np.array(all_embeddings)

# call pca
model = PCA(n_components=50)
model.fit(arr)
results = model.transform(arr)
print("PCA done!")
# call tsne on the results to get pro di
tmodel = TSNE(perplexity=50,early_exaggeration=24)
plotVals = tmodel.fit_transform(results)
print("TNSE Done")
plt.scatter(plotVals[:,0],plotVals[:,1])
plt.show()