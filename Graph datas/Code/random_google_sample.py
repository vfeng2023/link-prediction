import numpy as np
import networkx as nx
import random

from scipy.sparse import spdiags
from functools import partial

def rwr(x, T, R = 0.2, max_iters = 100):
    '''
    This function will perform the random walk with restart algorithm on a given vector x and the associated
    transition matrix of the network
    
    args:
        x (Array) : Initial vector
        T (Matrix) : Input matrix of transition probabilities
        R (Float) : Restart probabilities
        max_iters (Integer) : The maximum number of iterations
        
    returns:
        This function will return the result vector x
    '''
    
    old_x = x
    err = 1.
    
    for i in range(max_iters):
        x = (1 - R) * (T.dot(old_x)) + (R * x)
        err = np.linalg.norm(x - old_x, 1)
        if err <= 1e-6:
            break
        old_x = x
    return x
  
def run_rwr(g, R, max_iters):
    '''
    This function will run the `rwr` on a network
    
    args:
        g (Network) : This is a networkx network you want to run rwr on
        R (Float) : The restart probability
        max_iters (Integer) : The maximum number of iterations
        
    returns:
        This fuunction will return a numpy array of affinities where each element in the array will represent
        the similarity between two nodes
    '''
    
    A = nx.adjacency_matrix(g, weight = 'weight')
    m,n = A.shape
    
    d = A.sum(axis = 1)
    d = np.asarray(d).flatten()
    d = np.maximum(d, np.ones(n))
    
    invd = spdiags(1.0 / d, 0, m, n)
    T = invd.dot(A)
    
    rwr_fn = partial(rwr, T = T, R = R, max_iters = max_iters)
    
    aff = [rwr_fn(x) for x in np.identity(m)]
    aff = np.array(aff)
    return aff
  
if __name__ == '__main__':
    # for simplicity let's use a fully connected graph and randomly remove edges from it
    n, n_remove = 40, 250

    G = nx.Graph()
    G.add_nodes_from(range(n))
    G = nx.complete_graph(n, create_using=G)
    remove = random.sample(G.edges(),k=n_remove)
    G.remove_edges_from(remove)
    
    # apply random walk with restart on this network
    aff = run_rwr(G, R = 0.2, max_iters=1000)
