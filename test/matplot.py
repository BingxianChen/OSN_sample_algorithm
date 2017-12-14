#!/bin/env python
# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt
from dataImport.facebook_network import FaceData
from sampling import child_graphs,common
from evaluation import degree,draw_network

########### bfs ############
def bfs_text():
    f = FaceData()
    G = f.create_graph()                            # 获取原始数据

    bfs = common.BFS(G, None, 5000, "total")
    print len(bfs)

def draw():
    x=[1,1,1,1]
    y=[1,2,3,4]
    plt.plot(x,y)
    plt.ylabel(r'$P(k_\upsilon=k) $')
    plt.show()

def create_graph():

    # f = open("../dataSet/twitter_combined.txt", "r")
    f = open("../dataSet/soc-Epinions1.txt", "r")
    count = 0
    for line in f:
        a,b =  line.split("\t")
        print (a,b.split("\r")[0])
        # print (line.split(" ")[0], line.split(" ")[-1][:-1])
        count += 1

create_graph()


































