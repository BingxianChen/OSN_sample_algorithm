#!/bin/env python
# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt
from dataImport.facebook_network import FaceData
from sampling import child_graphs,common,improve_MH
from evaluation import degree,draw_network

########### 对网络的度进行分析 ##############

########### 子网的度分布 ##############
def sub_degree():
    f = FaceData()
    G = f.create_graph()                     # 获取原始数据

    BFS = common.BFS(G,10000)
    _plt = degree.degree(G,plt,"Original","k-")         # 绘制原始网络的度分布
    _plt = degree.ego_degree(G,BFS,_plt,"BFS","rh-")         # 随机爬虫子网的度分布
    _plt.legend(loc="upper right")                # 加入图例
    _plt.show()


########### 连续抽取38次样本并求其均值 #############
def multi_sampling():
    f = FaceData()
    G = f.create_graph()                            # 获取原始数据

    _degree = dict()         # 分析重组数据
    chushu = 0
    for i in xrange(38):
        BFS = common.BFS(G,10000)
        for i in BFS:
            _degree[G.degree(i)] = _degree.get(G.degree(i),0) + 1
        chushu += len(BFS)
        print "step ",i

    # 处理数据,取平均的度分布
    x = sorted(_degree.iterkeys())                  #生成x轴序列，从1到最大度
    num = chushu
    y = []
    for i in x:
        y.append(float(_degree[i])/num)

    # 保存数据
    f = open("../compare/degree_plot/Epin_BFS.txt", "w")
    try:
        for i in x:
            f.write(str(i) + " " + str(float(_degree[i])/num) + "\n")
    finally:
        f.close()


multi_sampling()