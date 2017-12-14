#!/bin/env python
# coding=utf-8

import networkx as nx
import matplotlib.pyplot as plt
from dataImport.facebook_network import FaceData
from sampling import common,improve_MH

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

        fre_degree = nx.degree_histogram(self.G)      # 获取网络中每个度的节点数量,返回list,列表的位置即节点的度
        baseline = round(float(sum(fre_degree[0:self.limit+1]))/sum(fre_degree), 3)
        # baseline = 0.412                                # 节约运算时间 用得到的固定数据
        x = range(self.x)
        y = [baseline for i in x]
        self.plt.plot(x, y, "k", linewidth=5.0, label="Baseline")
        # self.plt.show()

    # 记录抽样过程中节点度小于等于 limit 值的抽样占比的变化过程,samples是所选的抽样算法, lengend为是否加入图例
    def record_con(self, sample="MHRW", lengend=False):

        # 在G中抽取节点
        if sample == "MHRW":
            nodes = common.metropolis_hastings_random_walk(self.G, None, 10000, "total")
        elif sample == "RW":
            nodes = common.random_walk(self.G, None, 10000, "total")
        elif sample == "BFS":
            nodes = common.BFS(self.G, 10000)
        else:
            nodes = improve_MH.impore_03(self.G, None, 10000, "total")
        x = range(self.x)  # 横坐标
        y = []
        numerator = 0    # 分子
        denominator = 0  # 分母
        for i in nodes[0:self.x]:
            denominator += 1
            if self.G.degree(i) <= self.limit:
                numerator += 1
            y.append(float(numerator)/denominator)

        if sample == "MHRW":
            if lengend is True:
                self.plt.plot(x, y, "b--", label="MHRW", linewidth=3.0)
            else:
                self.plt.plot(x, y, "b--", linewidth=3.0)
        elif sample == "RW":
            if lengend is True:
                self.plt.plot(x, y, "g:", label="RW", linewidth=3.0)
            else:
                self.plt.plot(x, y, "g:", linewidth=3.0)
        elif sample == "BFS":
            if lengend is True:
                self.plt.plot(x, y, "c-.", label="BFS", linewidth=3.0)
            else:
                self.plt.plot(x, y, "c-.", linewidth=3.0)
        else:
            if lengend is True:
                self.plt.plot(x, y, "r-", label="UD", linewidth=3.0)
            else:
                self.plt.plot(x, y, "r-", linewidth=3.0)
    # 贴上标签
    def lengend(self):
        self.plt.legend(loc="upper right")
        self.plt.xlabel("number of nodes", size=20)
        self.plt.ylabel("Convergence value", size=20)

if __name__=="__main__":
    c = ConVer(10000, 12)
    c.avg_ref()
    c.record_con("MHRW")
    c.record_con("MHRW")
    c.record_con("MHRW", True)
    c.record_con("im")
    c.record_con("im")
    c.record_con("im", True)
    c.record_con("RW")
    c.record_con("RW")
    c.record_con("RW", True)
    c.record_con("BFS")
    c.record_con("BFS")
    c.record_con("BFS", True)
    c.lengend()
    c.plt.show()