#!/bin/env python
# coding=utf-8

import networkx as nx
import matplotlib.pyplot as plt
from dataImport.facebook_network import FaceData
from sampling import common,improve_MH
import numpy as np

# 对算法的收敛性进行分析做图
class ConVer:

    # 初始化构造函数 x 为作图的横坐标, limit为收敛的条件
    def __init__(self, x, limit):
        f = FaceData()
        self.G = f.create_graph()                     # 获取原始数据
        self.plt = plt
        self.x = x
        self.limit = limit

    # 返回节点度小于等于 limit 值的全网占比,用于参考基线
    def avg_ref(self):

        baseline1 = 0.1                                # 节约运算时间 用得到的固定数据
        baseline2 = -0.1
        self.plt.plot((0,self.x), (baseline1,baseline1), "k--", linewidth=2.0, )
        self.plt.plot((0,self.x), (baseline2,baseline2), "k--", linewidth=2.0, label="Baseline")

    # Z检验输入的是度的列表,输出的是Z值得列表和相应的横坐标值
    def Z_test(self,list_x):
        X = np.array(list_x)
        length = len(X)
        Z = []
        Xa = X[:10]
        Xb = X[50:100]
        Z.append((np.mean(Xa)-np.mean(Xb))/np.sqrt(np.var(Xa)+np.var(Xb)))
        for i in xrange(length/50,length,length/50):
            Xa = X[:i/10]
            Xb = X[i/2:i]
            Z.append((np.mean(Xa)-np.mean(Xb))/np.sqrt(np.var(Xa)+np.var(Xb)))
        return [100] + range(length/50,length,length/50),Z

    # 记录抽样过程中节点度小于等于 limit 值的抽样占比的变化过程,samples是所选的抽样算法, lengend为是否加入图例
    def record_con(self, sample="MHRW", lengend=False):

        # 在G中抽取节点
        if sample == "MHRW":
            nodes = common.metropolis_hastings_random_walk(self.G, None, self.x, "total")
        elif sample == "RW":
            nodes = common.random_walk(self.G, None, self.x, "total")
        elif sample == "BFS":
            nodes = common.BFS(self.G, self.x)
        else:
            nodes = improve_MH.impore_03(self.G, None, self.x, "total")
        x = range(self.x)  # 横坐标
        y = []
        list_x = []
        for i in nodes:
            list_x.append(self.G.degree(i))
        x,y = self.Z_test(list_x)

        if sample == "MHRW":
            if lengend is True:
                self.plt.plot(x, y, c='b',marker='v', label="MHRW", linewidth=1.0)
            else:
                self.plt.plot(x, y, c='b',marker='v', linewidth=1.0)
        elif sample == "RW":
            if lengend is True:
                self.plt.plot(x, y, c='m',marker='*', label="RW", linewidth=1.0)
            else:
                self.plt.plot(x, y, c='m',marker='*', linewidth=1.0)
        elif sample == "BFS":
            if lengend is True:
                self.plt.plot(x, y, c='g',marker='s', label="BFS", linewidth=1.0)
            else:
                self.plt.plot(x, y, c='g',marker='s', linewidth=1.0)
        else:
            if lengend is True:
                self.plt.plot(x, y, c='r',marker='o', label="UD", linewidth=1.0)
            else:
                self.plt.plot(x, y, c='r',marker='o', linewidth=1.0)
    # 贴上标签
    def lengend(self):
        self.plt.legend(loc="lower right")
        self.plt.xlabel("number of nodes", size=20)
        self.plt.ylabel("Convergence value", size=20)

if __name__=="__main__":
    c = ConVer(20000, 12)
    c.avg_ref()
    # c.record_con("MHRW")
    # c.record_con("MHRW")
    c.record_con("MHRW", True)
    # c.record_con("im")
    # c.record_con("im")
    c.record_con("im", True)
    # c.record_con("RW")
    # c.record_con("RW")
    c.record_con("RW", True)
    # c.record_con("BFS")
    # c.record_con("BFS")
    c.record_con("BFS", True)
    c.lengend()
    c.plt.show()