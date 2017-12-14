#!/bin/env python
# coding=utf-8
import networkx as nx
from dataImport.facebook_network import FaceData
from sampling import child_graphs

def cluster_a_RW():
    f = FaceData()
    G = f.create_graph()                     # 获取原始数据
    count = 3
    for i in xrange(100,12000,1000):
        avg_cluster = []
        avg_train = []
        avg_assort = []
        if count > 0:
            for j in xrange(5):
                rw = child_graphs.random_walk(G,None,i,"unique")
                avg_cluster.append(round(nx.average_clustering(rw), 4))
                avg_train.append(round(nx.transitivity(rw), 4))
                avg_assort.append(round(nx.degree_assortativity_coefficient(rw), 4))
            a = sum(avg_cluster)/len(avg_cluster)
            b = sum(avg_train)/len(avg_train)
            c = sum(avg_assort)/len(avg_assort)
            count -= 1
            print float(i)/1000,a,b,c
        else:
            rw = child_graphs.random_walk(G,None,i,"unique")
            a = round(nx.average_clustering(rw), 4)
            b = round(nx.transitivity(rw), 4)
            c = round(nx.degree_assortativity_coefficient(rw), 4)
            print float(i)/1000,a,b,c
# cluster_a_RW()

def transi_RW():
    f = FaceData()
    G = f.create_graph()                     # 获取原始数据
    count = 3
    for i in xrange(100,12000,1000):
        avg_cluster = []
        if count > 0:
            for j in xrange(5):
                rw = child_graphs.random_walk(G,None,i,"unique")
                avg_cluster.append(round(nx.transitivity(rw), 4))
            a = sum(avg_cluster)/len(avg_cluster)
            count -= 1
            print float(i)/1000,a
        else:
            rw = child_graphs.random_walk(G,None,i,"unique")
            a = round(nx.transitivity(rw), 4)
            print float(i)/1000,a

# transi_RW()

def cluster_transi_MHRW():
    f = FaceData()
    G = f.create_graph()                     # 获取原始数据
    count = 3
    for i in xrange(100,12000,1000):
        avg_cluster = []
        avg_trans = []
        avg_assort = []
        if count > 0:
            for j in xrange(5):
                mh = child_graphs.metropolis_hastings_random_walk(G,None,i,"unique")
                avg_cluster.append(round(nx.average_clustering(mh), 4))
                avg_trans.append(round(nx.transitivity(mh), 4))
                avg_assort.append(round(nx.degree_assortativity_coefficient(mh), 4))
            a = sum(avg_cluster)/len(avg_cluster)
            b = sum(avg_trans)/len(avg_trans)
            c = sum(avg_assort)/len(avg_assort)
            count -= 1
            print float(i)/1000,a,b,c
        else:
            mh = child_graphs.metropolis_hastings_random_walk(G,None,i,"unique")
            a = round(nx.average_clustering(mh), 4)
            b = round(nx.transitivity(mh), 4)
            c = round(nx.degree_assortativity_coefficient(mh), 4)
            print float(i)/1000,a,b,c
# cluster_transi_MHRW()

def cluster_transi_UD():
    f = FaceData()
    G = f.create_graph()                     # 获取原始数据
    count = 3
    for i in xrange(100,12000,1000):
        avg_cluster = []
        avg_trans = []
        avg_assort = []
        if count > 0:
            for j in xrange(5):
                mh = child_graphs.impore_03(G,None,i,"unique")
                avg_cluster.append(round(nx.average_clustering(mh), 4))
                avg_trans.append(round(nx.transitivity(mh), 4))
                avg_assort.append(round(nx.degree_assortativity_coefficient(mh), 4))
            a = sum(avg_cluster)/len(avg_cluster)
            b = sum(avg_trans)/len(avg_trans)
            c = sum(avg_assort)/len(avg_assort)
            count -= 1
            print float(i)/1000,a,b,c
        else:
            mh = child_graphs.impore_03(G,None,i,"unique")
            a = round(nx.average_clustering(mh), 4)
            b = round(nx.transitivity(mh), 4)
            c = round(nx.degree_assortativity_coefficient(mh), 4)
            print float(i)/1000,a,b,c

# cluster_transi_UD()

def cluster_transi_BFS():
    f = FaceData()
    G = f.create_graph()                     # 获取原始数据
    count = 3
    for i in xrange(100,12000,1000):
        avg_cluster = []
        avg_trans = []
        avg_assort = []
        if count > 0:
            for j in xrange(5):
                mh = child_graphs.BFS(G,i)
                avg_cluster.append(round(nx.average_clustering(mh), 4))
                avg_trans.append(round(nx.transitivity(mh), 4))
                avg_assort.append(round(nx.degree_assortativity_coefficient(mh), 4))
            a = sum(avg_cluster)/len(avg_cluster)
            b = sum(avg_trans)/len(avg_trans)
            c = sum(avg_assort)/len(avg_assort)
            count -= 1
            print float(i)/1000,a,b,c
        else:
            mh = child_graphs.BFS(G,i)
            a = round(nx.average_clustering(mh), 4)
            b = round(nx.transitivity(mh), 4)
            c = round(nx.degree_assortativity_coefficient(mh), 4)
            print float(i)/1000,a,b,c

# cluster_transi_BFS()
f = FaceData()
G = f.create_graph()
print round(nx.degree_assortativity_coefficient(G), 4)