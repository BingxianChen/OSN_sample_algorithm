#!/bin/env python
# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt
from dataImport.facebook_network import FaceData
from sampling import child_graphs

########### 对抽样子网的聚类系数进行评估 ##############
def avg_cluster(G, samp="ori"):
    if samp is "ori":
        return round(nx.average_clustering(G), 4)
    else:
        return round(nx.average_clustering(samp), 4)


################# 对子网进行聚类评估 #################
def sub_graph():
    f = FaceData()
    G = f.create_graph()                     # 获取原始数据

    # rw = child_graphs.random_walk(G,None,10000,"unique")
    mhrw = child_graphs.metropolis_hastings_random_walk(G,None,1000,"unique")

    # print "原始网络的平均聚类系数: ", avg_cluster(G)
    # print "RW 子网的平均聚类系数: ", avg_cluster(G, rw)
    print "MHRW 子网的平均聚类系数: ", avg_cluster(G, mhrw)

########### 对抽样子网的匹配系数进行评估 ##############
def assort(G, samp="ori"):
    if samp is "ori":
        return round(nx.person_assortativity_coefficient(G), 4)
    else:
        return round(nx.degree_assortativity_coefficient(samp), 4)


################# 对子网进行匹配系数评估 #################
def sub_graph_assort():
    f = FaceData()
    G = f.create_graph()                     # 获取原始数据

    rw = child_graphs.random_walk(G,None,1000,"unique")
    mhrw = child_graphs.metropolis_hastings_random_walk(G,None,1000,"unique")

    print "原始网络的匹配系数: ", avg_cluster(G)
    print "RW 子网的匹配系数: ", avg_cluster(G, rw)
    print "MHRW 子网的匹配系数: ", avg_cluster(G, mhrw)


sub_graph_assort()