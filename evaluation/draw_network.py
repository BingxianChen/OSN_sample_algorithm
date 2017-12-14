#!/bin/env python
# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt

def draw_gragh(G,plt):
    nx.draw(G,with_labels=True) # networkx draw()
    plt.draw() # pyplot draw()
    return plt