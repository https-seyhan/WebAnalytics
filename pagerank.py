#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: saul
"""
import networkx as nx
import numpy as np
import os
import matplotlib.pylab as plt
from scipy import sparse
from scipy.sparse.linalg import spsolve
os.chdir("/home/saul/pythonWork")

damping = 0.85
beta = 1 - damping
np.seterr(divide = 'ignore')
stmarks = nx.read_gml('stmarks.gml')

print("Marks : ", stmarks)
species = np.array(stmarks.nodes())
print(species)

Adj = nx.to_scipy_sparse_matrix(stmarks, dtype=np.float64) #graph adjacency matrix 

#number of species
print(len(species))

#Get degrees
degrees = np.ravel(Adj.sum(axis=1))
print(degrees)
#And covert the degrees into diagonal matrix
Deginv = sparse.diags(1 / degrees).tocsr()
print(Deginv)

Trans = (Deginv @ Adj).T
print(Trans)

I = sparse.eye(n, format ='csc')
print(I)

pagerank = spsolve(I - damping*Trans, np.full(n, beta/n))
print(pagerank)

def page_rank_plot(in_degrees, pageranks, names, *, annotations = [], **figkwargs):
    fig, ax = plt.subplots(**figkwargs)
    ax.scatter(in_degrees, pageranks, c=[0.835, 0.369, 0], lw=0)
    for name, indeg, pr in zip(names, in_degrees, pageranks):
        if name in annotations:
            text = ax.text(indeg + 0.1, pr, name)
    
    ax.set_ylim(0, np.max(pageranks)*1.1)
    ax.set_xlim(-1, np.max(in_degrees)*1.1)
    ax.set_ylabel('PageRank')
    ax.set_xlabel('In-degrees')
    
interesting = ['detritus', 'phytoplankton', 'benthic algea', 'micro-epiphytes',
               'microfauna', 'zooplankton', 'predatory shrimps', 'meiofuna', 'gulls']

in_degrees = np.ravel(Adj.sum(axis=0))
page_rank_plot(in_degrees, pagerank, species, annotations = interesting)
    
    
    
    
    
    
