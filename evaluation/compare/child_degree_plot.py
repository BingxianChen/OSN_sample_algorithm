#!/bin/env python
# coding=utf-8
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from dataImport.facebook_network import FaceData
from sampling import child_graphs,common,improve_MH
from evaluation import degree,draw_network

########### 对网络的度进行分析 ##############

########### 子网的度分布 ##############
def sub_degree():
    f = FaceData()
    G = f.create_graph()                     # 获取原始数据

    rw = child_graphs.random_walk(G,None,10000,"unique")
    mhrw = child_graphs.metropolis_hastings_random_walk(G,None,10000,"unique")
    _plt = degree.degree(G,plt,"UNI","b--")       # 绘制原始网络的度分布
    _plt = degree.degree(rw,_plt,"RW","k")         # 随机爬虫子网的度分布
    _plt = degree.degree(mhrw,_plt,"MHRW","r-.")
    _plt.legend(loc="upper right")                # 加入图例
    _plt.show()

########### 拓扑网络的度分布 ############
def ego_degree():
    f = FaceData()
    G = f.create_graph()                            # 获取原始数据


    # rw = common.random_walk(G,None,10000,"unique")
    mhrw = common.metropolis_hastings_random_walk(G,None,10000,"unique")
    # bfs = common.BFS(G,None,8000,"unique")
    impore = improve_MH.impore_03(G, None, 10000, "unique")
    _plt = degree.degree(G,plt,"Original","k-")         # 绘制原始网络的度分布
    # _plt = degree.ego_degree(G,bfs,_plt,"ego-bfs","c*")
    # _plt = degree.ego_degree(G,rw,_plt,"ego-RW","k-")
    # _plt = degree.ego_degree(G,mhrw,_plt,"MHRW","b-.")
    _plt = degree.ego_degree(G,mhrw,_plt,"MHRW","bv-")
    # _plt = degree.ego_degree(G,impore,_plt,"UD","r:")
    _plt = degree.ego_degree(G,impore,_plt,"UD","rh-")
    _plt.ylabel(r'$P(k_\upsilon=k) $')
    _plt.xlabel(u'node degree k')
    # _plt.xlim(0,100)
    _plt.legend(loc="upper right")                       # 加入图例
    _plt.show()

########### 原始网络的平均度 ############
def ori_avg_degree():
    f = FaceData()
    G = f.create_graph()                            # 获取原始数据

    rw = common.random_walk(G,None,16000,"unique")
    mhrw = common.metropolis_hastings_random_walk(G,None,16000,"unique")
    bfs = common.BFS(G,None,16000,"unique")
    print "原始网络的平均度为: ", degree.avg_degree(G)
    print "RW抽样得到的平均度为: ", degree.avg_degree(G, rw)
    print "MHRW抽样得到的平均度为: ", degree.avg_degree(G, mhrw)
    print "BFS抽样得到的平均度为: ", degree.avg_degree(G, bfs)

########### 连续抽取38次样本并求其均值 #############
def multi_sampling():
    f = FaceData()
    G = f.create_graph()                            # 获取原始数据

    _degree = dict()         # 分析重组数据
    chushu = 0
    for i in xrange(38):
        mhrw = common.metropolis_hastings_random_walk(G,None,10000,"unique")
        # impore = improve_MH.impore_02(G, None, 10000, "unique")
        for i in mhrw:
            _degree[G.degree(i)] = _degree.get(G.degree(i),0) + 1
        chushu += len(mhrw)
        print "step "

    # 处理数据,取平均的度分布
    x = sorted(_degree.iterkeys())                  #生成x轴序列，从1到最大度
    num = chushu
    y = []
    for i in x:
        y.append(float(_degree[i])/num)

    # 保存数据
    f = open("../compare/degree_plot/dup_Twitter_Mh.txt", "w")
    try:
        for i in x:
            f.write(str(i) + " " + str(float(_degree[i])/num) + "\n")
    finally:
        f.close()

    ##################
    _degree = dict()         # 分析重组数据
    chushu = 0
    for i in xrange(38):
        # mhrw = common.metropolis_hastings_random_walk(G,None,10000,"unique")
        impore = improve_MH.impore_02(G, None, 10000, "unique")
        for i in impore:
            _degree[G.degree(i)] = _degree.get(G.degree(i),0) + 1
        chushu += len(impore)
        print "step "

    # 处理数据,取平均的度分布
    x = sorted(_degree.iterkeys())                  #生成x轴序列，从1到最大度
    num = chushu
    y = []
    for i in x:
        y.append(float(_degree[i])/num)

    # 保存数据
    f = open("../compare/degree_plot/dup_Twitter_Ud.txt", "w")
    try:
        for i in x:
            f.write(str(i) + " " + str(float(_degree[i])/num) + "\n")
    finally:
        f.close()

######## 绘制度分布图 #########
def draw_degree_unDup():

    f = open("../compare/degree_plot/undup_Twitter_Mh.txt", "r")
    try:
        x_Tw_Mh = []
        y_Tw_Mh = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Tw_Mh.append(x)
            y_Tw_Mh.append(y)
    finally:
        f.close()

    f = open("../compare/degree_plot/undup_Twitter_Ud.txt", "r")
    try:
        x_Tw_Ud = []
        y_Tw_Ud = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Tw_Ud.append(x)
            y_Tw_Ud.append(y)
    finally:
        f.close()

    f = open("../compare/degree_plot/Twitter_Ori.txt", "r")
    try:
        x_Tw_ori = []
        y_Tw_ori = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Tw_ori.append(x)
            y_Tw_ori.append(y)
    finally:
        f.close()

    #######

    f = open("../compare/degree_plot/undup_Epin_Mh.txt", "r")
    try:
        x_Ep_Mh = []
        y_Ep_Mh = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Ep_Mh.append(x)
            y_Ep_Mh.append(y)
    finally:
        f.close()

    f = open("../compare/degree_plot/undup_Epin_Ud.txt", "r")
    try:
        x_Ep_Ud = []
        y_Ep_Ud = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Ep_Ud.append(x)
            y_Ep_Ud.append(y)
    finally:
        f.close()

    f = open("../compare/degree_plot/Epin_Ori.txt", "r")
    try:
        x_Ep_ori = []
        y_Ep_ori = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Ep_ori.append(x)
            y_Ep_ori.append(y)
    finally:
        f.close()

    fig = plt.figure()
    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,3)
    ax3 = plt.subplot(2,2,2)
    ax4 = plt.subplot(2,2,4)

    ax1.loglog(x_Tw_Mh, y_Tw_Mh, "bv-", label="MHRW", linewidth=3.0, alpha=0.5)
    ax1.loglog(x_Tw_Ud, y_Tw_Ud, "rh-.", label="UD", linewidth=3.0, alpha=0.6)
    ax1.loglog(x_Tw_ori,y_Tw_ori,"k-",label = "Original",linewidth=4.0, alpha=0.6)  #在双对数坐标轴上绘制度分布曲线
    ax1.legend(loc="upper right")
    ax1.set_ylabel(r'$P(k_\upsilon=k) $')
    ax1.set_xlabel(u'node degree k\n (a)')
    ax1.text(1.5,10**(-5.5),"Twitter",fontsize=20)

    ax2.loglog(x_Ep_Mh, y_Ep_Mh, "bv-", label="MHRW", linewidth=3.0, alpha=0.5)
    ax2.loglog(x_Ep_Ud, y_Ep_Ud, "rh-.", label="UD", linewidth=3.0, alpha=0.6)
    ax2.loglog(x_Ep_ori,y_Ep_ori,"k-",label = "Original",linewidth=4.0, alpha=0.6)  #在双对数坐标轴上绘制度分布曲线
    ax2.legend(loc="upper right")
    ax2.set_ylabel(r'$P(k_\upsilon=k) $')
    ax2.set_xlabel(u'node degree k\n (c)')
    ax2.text(1.5,10**(-5.5),"Epinions",fontsize=20)



    ################## 包含重复节点的度分布 ###############
    f = open("../compare/degree_plot/dup_Twitter_Mh.txt", "r")
    try:
        _x_Tw_Mh = []
        _y_Tw_Mh = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            _x_Tw_Mh.append(x)
            _y_Tw_Mh.append(y)
    finally:
        f.close()

    f = open("../compare/degree_plot/dup_Twitter_Ud.txt", "r")
    try:
        _x_Tw_Ud = []
        _y_Tw_Ud = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            _x_Tw_Ud.append(x)
            _y_Tw_Ud.append(y)
    finally:
        f.close()


    #######

    f = open("../compare/degree_plot/dup_Epin_Mh.txt", "r")
    try:
        _x_Ep_Mh = []
        _y_Ep_Mh = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            _x_Ep_Mh.append(x)
            _y_Ep_Mh.append(y)
    finally:
        f.close()

    f = open("../compare/degree_plot/dup_Epin_Ud.txt", "r")
    try:
        _x_Ep_Ud = []
        _y_Ep_Ud = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            _x_Ep_Ud.append(x)
            _y_Ep_Ud.append(y)
    finally:
        f.close()


    ax3.loglog(_x_Tw_Mh, _y_Tw_Mh, "bv-", label="MHRW", linewidth=3.0, alpha=0.5)
    ax3.loglog(_x_Tw_Ud, _y_Tw_Ud, "rh-.", label="UD", linewidth=3.0, alpha=0.6)
    ax3.loglog(x_Tw_ori,y_Tw_ori,"k-",label = "Original",linewidth=4.0, alpha=0.6)  #在双对数坐标轴上绘制度分布曲线
    ax3.legend(loc="upper right")
    ax3.set_ylabel(r'$P(k_\upsilon=k) $')
    ax3.set_xlabel(u'node degree k\n (b)')
    ax3.text(1.5,10**(-5.5),"Twitter",fontsize=20)

    ax4.loglog(_x_Ep_Mh, _y_Ep_Mh, "bv-", label="MHRW", linewidth=3.0, alpha=0.5)
    ax4.loglog(_x_Ep_Ud, _y_Ep_Ud, "rh-.", label="UD", linewidth=3.0, alpha=0.6)
    ax4.loglog(x_Ep_ori,y_Ep_ori,"k-",label = "Original",linewidth=4.0, alpha=0.6)  #在双对数坐标轴上绘制度分布曲线
    ax4.legend(loc="upper right")
    ax4.set_ylabel(r'$P(k_\upsilon=k) $')
    ax4.set_xlabel(u'node degree k\n (d)')
    ax4.text(1.5,10**(-5.5),"Epinions",fontsize=20)

    plt.tight_layout()
    plt.show()

######## 误差函数 ########
# mean 是原始网络的属性
# evaluate 是估计的网络属性
def Error_function(mean,evaluate_x,evaluate_y):
    C = list()
    for i in xrange(len(evaluate_x)):
        E = float(mean[int(evaluate_x[i])])
        x = float(evaluate_y[i])
        C.append(float(abs(E - x))/E)
    return C

######## 数据均匀化 ######
def smoon(y):
    smoly = list()
    smoly = y[0:10]
    for i in xrange(10,len(y) - 1):
        sm = float(y[i-1] + y[i] + y[i+1])/3
        smoly.append(sm)

    smoly.append(y[-1])
    return smoly

####### CDF 函数 ########
def cdf(y):
    y_num = [float(i) for i in y]
    return np.cumsum(y_num)




######## 绘制度分布图误差图 #########
def draw_degree_unDup_error():

    f = open("../compare/degree_plot/undup_Twitter_Mh.txt", "r")
    try:
        x_Tw_Mh = []
        y_Tw_Mh = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Tw_Mh.append(x)
            y_Tw_Mh.append(y)
    finally:
        f.close()

    f = open("../compare/degree_plot/undup_Twitter_Ud.txt", "r")
    try:
        x_Tw_Ud = []
        y_Tw_Ud = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Tw_Ud.append(x)
            y_Tw_Ud.append(y)
    finally:
        f.close()

    f = open("../compare/degree_plot/Twitter_Ori.txt", "r")
    try:
        x_Tw_ori = []
        y_Tw_ori = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Tw_ori.append(x)
            y_Tw_ori.append(y)
    finally:
        f.close()

    #######

    f = open("../compare/degree_plot/undup_Epin_Mh.txt", "r")
    try:
        x_Ep_Mh = []
        y_Ep_Mh = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Ep_Mh.append(x)
            y_Ep_Mh.append(float(y)*5/4)
    finally:
        f.close()

    f = open("../compare/degree_plot/undup_Epin_Ud.txt", "r")
    try:
        x_Ep_Ud = []
        y_Ep_Ud = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Ep_Ud.append(x)
            y_Ep_Ud.append(float(y)*5/4)
    finally:
        f.close()

    f = open("../compare/degree_plot/Epin_Ori.txt", "r")
    try:
        x_Ep_ori = []
        y_Ep_ori = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Ep_ori.append(x)
            y_Ep_ori.append(y)
    finally:
        f.close()

    f = open("../compare/degree_plot/Epin_BFS.txt", "r")
    try:
        x_Ep_bfs = []
        y_Ep_bfs = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Ep_bfs.append(x)
            y_Ep_bfs.append(y)
    finally:
        f.close()

    f = open("../compare/degree_plot/Twitter_BFS.txt", "r")
    try:
        x_Tw_bfs = []
        y_Tw_bfs = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            x_Tw_bfs.append(x)
            y_Tw_bfs.append(y)
    finally:
        f.close()

    fig = plt.figure()
    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,3)
    ax3 = plt.subplot(2,2,2)
    ax4 = plt.subplot(2,2,4)

    Err_Tw_Mh = Error_function(y_Tw_ori,x_Tw_Mh,y_Tw_Mh)
    sm_Tw_Mh = smoon(smoon(smoon(Err_Tw_Mh)))


    ax1.semilogx(x_Tw_Mh[:200], sm_Tw_Mh[:200], "bv-", label="MHRW", linewidth=3.0, alpha=0.9)
    ax1.semilogx(x_Tw_Ud[:200], smoon(smoon(smoon(Error_function(y_Tw_ori,x_Tw_Ud,y_Tw_Ud))))[:200], "rh-.", label="UD", linewidth=3.0, alpha=0.9)
    ax1.semilogx(x_Tw_bfs[:200], smoon(smoon(smoon(smoon(Error_function(y_Tw_ori,x_Tw_bfs,y_Tw_bfs)))))[:200], "g.", label="BFS", linewidth=4.0, alpha=0.9)
    # ax1.loglog(x_Tw_ori,y_Tw_ori,"k-",label = "Original",linewidth=4.0, alpha=0.6)  #在双对数坐标轴上绘制度分布曲线
    ax1.axis([0,200,0,2])
    ax1.legend(loc="upper left")
    ax1.set_ylabel(u'NMSE',size=15)
    ax1.set_xlabel(u'Twitter node degree k\n (a)',size=15)
    # ax1.text(1.5,10**(-5.5),"Twitter",fontsize=20)

    ax2.semilogx(x_Ep_Mh[:200], smoon(smoon(smoon(Error_function(y_Ep_ori,x_Ep_Mh,y_Ep_Mh))))[:200], "bv-", label="MHRW", linewidth=3.0, alpha=0.9)
    ax2.semilogx(x_Ep_Ud[:200], smoon(smoon(smoon(Error_function(y_Ep_ori,x_Ep_Ud,y_Ep_Ud))))[:200], "rh-.", label="UD", linewidth=3.0, alpha=0.9)
    ax2.semilogx(x_Ep_bfs[:200], smoon(smoon(smoon(Error_function(y_Ep_ori,x_Ep_bfs,y_Ep_bfs))))[:200], "g.", label="BFS", linewidth=4.0, alpha=0.9)
    # ax2.plot(x_Ep_ori,y_Ep_ori,"k-",label = "Original",linewidth=4.0, alpha=0.6)  #在双对数坐标轴上绘制度分布曲线
    ax2.axis([0,200,0,5.5])
    ax2.legend(loc="upper left")
    ax2.set_ylabel(u'NMSE',size=15)
    ax2.set_xlabel(u'Epinions node degree k\n (c)',size=15)
    # ax2.text(1.5,10**(-5.5),"Epinions",fontsize=20)



    ################## 包含重复节点的度分布 ###############
    # f = open("../compare/degree_plot/dup_Twitter_Mh.txt", "r")
    # try:
    #     _x_Tw_Mh = []
    #     _y_Tw_Mh = []
    #     for line in f:
    #         x, b = line.split(" ")
    #         y = b.split("\n")[0]
    #         _x_Tw_Mh.append(x)
    #         _y_Tw_Mh.append(y)
    # finally:
    #     f.close()
    #
    # f = open("../compare/degree_plot/dup_Twitter_Ud.txt", "r")
    # try:
    #     _x_Tw_Ud = []
    #     _y_Tw_Ud = []
    #     for line in f:
    #         x, b = line.split(" ")
    #         y = b.split("\n")[0]
    #         _x_Tw_Ud.append(x)
    #         _y_Tw_Ud.append(y)
    # finally:
    #     f.close()
    #
    #
    # #######
    #
    # f = open("../compare/degree_plot/dup_Epin_Mh.txt", "r")
    # try:
    #     _x_Ep_Mh = []
    #     _y_Ep_Mh = []
    #     for line in f:
    #         x, b = line.split(" ")
    #         y = b.split("\n")[0]
    #         _x_Ep_Mh.append(x)
    #         _y_Ep_Mh.append(y)
    # finally:
    #     f.close()
    #
    # f = open("../compare/degree_plot/dup_Epin_Ud.txt", "r")
    # try:
    #     _x_Ep_Ud = []
    #     _y_Ep_Ud = []
    #     for line in f:
    #         x, b = line.split(" ")
    #         y = b.split("\n")[0]
    #         _x_Ep_Ud.append(x)
    #         _y_Ep_Ud.append(y)
    # finally:
    #     f.close()


    ax3.plot(x_Tw_Mh, cdf(y_Tw_Mh), "bv-", label="MHRW", linewidth=3.0, alpha=0.5)
    ax3.plot(x_Tw_Ud, cdf(y_Tw_Ud), "rh-.", label="UD", linewidth=3.0, alpha=0.6)
    ax3.plot(x_Tw_bfs,cdf(y_Tw_bfs),"g.",label = "BFS",linewidth=4.0, alpha=0.6)  #在双对数坐标轴上绘制度分布曲线
    ax3.plot(x_Tw_ori,cdf(y_Tw_ori),"k-",label = "Original",linewidth=4.0, alpha=0.9)  #在双对数坐标轴上绘制度分布曲线
    ax3.axis([0,200,0,1])
    ax3.legend(loc="lower right")
    ax3.set_ylabel(u'CDF',size=15)
    ax3.set_xlabel(u'Twitter node degree k\n (b)',size=15)
    # ax3.text(1.5,10**(-5.5),"Twitter",fontsize=20)

    ax4.plot(x_Ep_Mh, cdf(y_Ep_Mh), "bv-", label="MHRW", linewidth=3.0, alpha=0.5)
    ax4.plot(x_Ep_Ud, cdf(y_Ep_Ud), "rh-.", label="UD", linewidth=3.0, alpha=0.6)
    ax4.plot(x_Ep_bfs,cdf(y_Ep_bfs),"g.",label = "BFS",linewidth=4.0, alpha=0.9)  #在双对数坐标轴上绘制度分布曲线
    ax4.plot(x_Ep_ori,cdf(y_Ep_ori),"k-",label = "Original",linewidth=4.0, alpha=0.9)  #在双对数坐标轴上绘制度分布曲线
    ax4.axis([0,200,0,1])
    ax4.legend(loc="lower right")
    ax4.set_ylabel(u'CDF',size=15)
    ax4.set_xlabel(u'Epinions node degree k\n (d)',size=15)
    # ax4.text(1.5,10**(-5.5),"Epinions",fontsize=20)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    # sub_degree()
    # ego_degree()
    # ori_avg_degree()
    # multi_sampling()
    # draw_degree_unDup()
    draw_degree_unDup_error()