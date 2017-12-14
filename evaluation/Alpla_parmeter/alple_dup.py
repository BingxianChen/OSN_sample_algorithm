#!/bin/env python
# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt
from dataImport.facebook_network import FaceData
from sampling import child_graphs,common,improve_MH
from evaluation import degree,draw_network

########### 算法的参数分析 ##############

def alpha_press():
    f = FaceData()
    G = f.create_graph()                     # 获取原始数据

    impore = improve_MH.impore_03(G, None, 10000, "unique")
    # print round(1/impore - 1, 4)
    # 保存数据
    f = open("../compare/alpha_dup/a_dup.txt", "w")
    try:
        for i in xrange(5,100,5):
            i = float(i)/100
            print i
            dup = 0
            for j in xrange(0,10):
                dup += improve_MH.impore_03(G, None, 10000, "unique",alpa=i)
            dup /= 10
            f.write(str(i) + " " + str(dup) + "\n")
            print dup
    finally:
        f.close()

def compare_press():
    f = FaceData()
    G = f.create_graph()                     # 获取原始数据

    rw = common.random_walk(G,None,10000,"unique")
    mhrw = common.metropolis_hastings_random_walk(G,None,10000,"unique")
    # print round(1/impore - 1, 4)
    # 保存数据
    f = open("../compare/alpha_dup/com_dup.txt", "w")
    try:
        f.write(str("rw") + " " + str(rw) + "\n")
        f.write(str("mhrw") + " " + str(mhrw) + "\n")
    finally:
        f.close()

def alpha_draw():
    f = open("../compare/alpha_dup/a_dup.txt", "r")
    try:
        x_ud = []
        y_ud = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_ud.append(x)
            y_ud.append(y)
    finally:
        f.close()


    x_rw = [float(i)/100 for i in xrange(5,101,5)]
    y_rw = [0.4371 for i in xrange(5,101,5)]

    x_mhrw = [float(i)/100 for i in xrange(5,101,5)]
    y_mhrw = [2.8204 for i in xrange(5,101,5)]

    plt.plot(x_rw, y_rw, "k--", label="RW", linewidth=6.0)
    plt.plot(x_mhrw, y_mhrw, "r-.", label="MHRW", linewidth=6.0)
    plt.plot(x_ud, y_ud, "bv-", label="UD", linewidth=4.0)
    plt.legend(loc="center left")
    plt.ylabel(r'repetition rate', size=20)
    plt.xlabel(r'$\alpha$',size=30)
    plt.xlim(0,1.05)
    plt.text(1.5,10**(-5.5),"Twitter",fontsize=20)

    plt.show()

if __name__ == "__main__":
    alpha_draw()