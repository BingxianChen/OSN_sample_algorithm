#!/bin/env python
# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt
from dataImport.facebook_network import FaceData
from sampling import child_graphs,common,improve_MH
from evaluation import degree,draw_network

def duplicate_epinions_Mhrw():
    t = FaceData()
    G = t.create_graph()                     # 获取原始数据

    f = open("../compare/avg_degree/dup_Epinion_Mhrw.txt", "w")
    try:
        for i in xrange(100, 10000, 100):
            mhrw = common.metropolis_hastings_random_walk(G, None, i, "unique")
            f.write(str(i) + " " + str(mhrw) + "\n")
    finally:
        f.close()

def duplicate_epinions_UD():
    t = FaceData()
    G = t.create_graph()                     # 获取原始数据

    f = open("../compare/avg_degree/dup_Epinion_UD.txt", "w")
    try:
        for i in xrange(100, 10000, 100):
            mhrw = improve_MH.impore_02(G, None, i, "unique")
            f.write(str(i) + " " + str(mhrw) + "\n")
    finally:
        f.close()

def draw_epinions_dupicate(plt):

    f = open("../compare/avg_degree/dup_Epinion_Mhrw.txt", "r")
    try:
        _x = []
        _y = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            _x.append(x)
            _y.append(y)
    finally:
        f.close()

    f = open("../compare/avg_degree/dup_Epinion_UD.txt", "r")
    try:
        _x_ = []
        _y_ = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            _x_.append(x)
            _y_.append(y)
    finally:
        f.close()

    plt.plot(_x, _y, "b-.", label="MHRW", linewidth=3.0)
    plt.plot(_x_,  _y_, "r-", label="UD", linewidth=3.0)
    plt.set_ylim(0,1)
    plt.set_ylabel("update rate",size=20)
    plt.set_xlabel("number of nodes",size=20)
    plt.text(100, 0.85, "Epinions", fontsize=20)
    plt.legend(loc="upper right")
    # plt.show()
    # plt.savefig("epinions.eps", dpi=300)


def duplicate_twitter_Mhrw():
    t = FaceData()
    G = t.create_graph()                     # 获取原始数据

    f = open("../compare/avg_degree/dup_Twitter_Mhrw.txt", "w")
    try:
        for i in xrange(100, 10000, 100):
            mhrw = common.metropolis_hastings_random_walk(G, None, i, "unique")
            f.write(str(i) + " " + str(mhrw) + "\n")
    finally:
        f.close()

def duplicate_twitter_UD():
    t = FaceData()
    G = t.create_graph()                     # 获取原始数据

    f = open("../compare/avg_degree/dup_Twitter_UD.txt", "w")
    try:
        for i in xrange(100, 10000, 100):
            mhrw = improve_MH.impore_02(G, None, i, "unique")
            f.write(str(i) + " " + str(mhrw) + "\n")
    finally:
        f.close()

def draw_twitter_dupicate(plt):

    f = open("../compare/avg_degree/dup_Twitter_Mhrw.txt", "r")
    try:
        _x = []
        _y = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            _x.append(x)
            _y.append(y)
    finally:
        f.close()

    f = open("../compare/avg_degree/dup_Twitter_UD.txt", "r")
    try:
        _x_ = []
        _y_ = []
        for line in f:
            x, b = line.split(" ")
            y = b.split("\n")[0]
            _x_.append(x)
            _y_.append(y)
    finally:
        f.close()

    plt.plot(_x, _y, "b-.", label="MHRW", linewidth=3.0)
    plt.plot(_x_,  _y_, "r-", label="UD", linewidth=3.0)
    plt.set_ylim(0, 1)
    plt.set_ylabel("update rate",size=20)
    plt.set_xlabel("number of nodes",size=20)
    plt.text(100, 0.85, "Twitter", fontsize=20)
    plt.legend(loc="upper right")
    # plt.show()
    # plt.savefig("twitter.eps", dpi=300)

# duplicate_twitter_Mhrw()
# duplicate_twitter_UD()

fig = plt.figure()
ax1 = plt.subplot(2,1,1)
ax2 = plt.subplot(2,1,2)
draw_twitter_dupicate(ax1)
draw_epinions_dupicate(ax2)
plt.tight_layout()
plt.show()
# duplicate_epinions_UD()
# draw_epinions_dupicate()


