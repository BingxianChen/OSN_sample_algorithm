#!/bin/env python
# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt
from dataImport.facebook_network import FaceData
from sampling import child_graphs,common
from evaluation import degree,draw_network


def create_graph():
    t = FaceData()
    G = t.create_graph()                     # 获取原始数据
    f = open("../compare/avg_degree/rw.txt", "w")
    try:
        rw = common.random_walk(G,None,8000,"unique")
        avg = float(sum([G.degree(i) for i in rw]))/len(rw)
        f.write("RW_avgDegree ")
        f.write(str(round(avg, 2)))
    finally:
        f.close()

create_graph()