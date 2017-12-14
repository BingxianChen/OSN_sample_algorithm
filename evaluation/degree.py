#!/bin/env python
# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import collections

# 采样生成的子网络度分布
def degree(G,plt,label,style = "b--"):
    _degree = nx.degree_histogram(G)          #返回图中所有节点的度分布序列
    print "step 1"
    x = range(len(_degree))                   #生成x轴序列，从1到最大度
    print "step 2"
    num = float(sum(_degree))
    print "step 3"
    y = [z/num for z in _degree]
    print "step 4"
    #  # 绘制拟合曲线
    # c=np.polyfit(x,y,4)
    # yy=np.polyval(c,x)
    # x_new=np.linspace(0, 100, 8000)
    # f_liner=np.polyval(c,x_new)
    # plt.loglog(x_new,f_liner,style,label = label,linewidth=2.0)  #在双对数坐标轴上绘制度分布曲线

    plt.loglog(x,y,style,label = label,linewidth=3.0)  #在双对数坐标轴上绘制度分布曲线
    return plt

# 采样生成的拓扑网络度分布
def ego_degree(G,samp,plt,label,style = "b--"):
    _degree = dict()
    for i in samp:
        _degree[G.degree(i)] = _degree.get(G.degree(i),0) + 1
    print "step 1"
    x = sorted(_degree.iterkeys())                  #生成x轴序列，从1到最大度
    print "step 2"
    num = len(samp)
    print "step 3"
    y = []
    for i in x:
        y.append(float(_degree[i])/num)
    print "step 4"
    # # 绘制拟合曲线
    # c=np.polyfit(x,y,4)
    # yy=np.polyval(c,x)
    # x_new=np.linspace(0, 100, 8000)
    # f_liner=np.polyval(c,x_new)
    # plt.loglog(x_new,f_liner,style,label = label,linewidth=2.0)  #在双对数坐标轴上绘制度分布曲线
    plt.loglog(x,y,style,label = label,linewidth=3.0)  #在双对数坐标轴上绘制度分布曲线
    return plt

# 网络的平均度
def avg_degree(G, samp="ori"):
    if samp is "ori":
        _degree = nx.degree_histogram(G)          #返回图中所有节点的度分布序列
        num = 0
        for i in xrange(len(_degree)):              # 每个节点的度相加,再除以节点总数
            num += _degree[i]*i
        return round(float(num)/sum(_degree), 4)
    else:
        num = 0
        for i in samp:
            num += G.degree(i)
        return round(float(num)/len(samp), 4)