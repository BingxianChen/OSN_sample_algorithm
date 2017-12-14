
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# In[98]:

def extract(name):
    f = open("{0}.txt".format(name), "r")
    cluster = []
    trasi = []
    assort = []
    try:
        for line in f:
            cluster.append(line.split(" ")[1])
            trasi.append(line.split(" ")[2])
            assort.append(line.split(" ")[3][:-1])
    finally:
        f.close()
        return [cluster,trasi,assort]
    
MHRW = extract("MHRW")
UD = extract("UD")
BFS = extract("BFS")
RW = extract("RW")



def cluser():
    num = round(float(100)/81306,4)
    X = [num,]
    for i in xrange(11):
        num += round(float(1000)/81306,4)
        X.append(round(num,4))
    # print UD[0]
    plt.scatter(X,MHRW[0],s=100,c='b',marker='v',label = 'MHRW')
    plt.scatter(X,UD[0],s=100,c='r',marker='o',label = 'UD')
    plt.scatter(X,BFS[0],s=100,c='g',marker='s',label = 'BFS')
    plt.scatter(X,RW[0],s=100,c='m',marker='*',label = 'RW',)
    plt.plot([0,0.13],[0.5653, 0.5653],c='k',linewidth=3.0,label = 'ori')
    plt.xlabel('sampling rate',fontsize=15)
    plt.ylabel('clustering',fontsize=15)
    plt.xlim([-0.005,0.14])
    plt.ylim([-0.5,0.5])
    plt.legend(loc='center right')
    plt.show()
# cluser()


def trans():
    num = round(float(100)/81306,4)
    X = [num,]
    for i in xrange(11):
        num += round(float(1000)/81306,4)
        X.append(round(num,4))
    # print UD[0]
    plt.scatter(X,MHRW[1],s=50,c='b',marker='v',label = 'MHRW')
    plt.scatter(X,UD[1],s=50,c='r',marker='o',label = 'UD')
    plt.scatter(X,BFS[1],s=50,c='g',marker='s',label = 'BFS')
    plt.scatter(X,RW[1],s=50,c='m',marker='*',label = 'RW')
    plt.plot([0,0.13],[0.1706, 0.1706],c='k',linewidth=3.0,label = 'Original')
    plt.xlabel('sampling rate',fontsize=15)
    plt.ylabel('transitivity',fontsize=15)
    plt.xlim([-0.005,0.14])
    plt.legend()
    plt.show()
# trans()


def assort():
    num = round(float(100)/81306,4)
    X = [num,]
    for i in xrange(11):
        num += round(float(1000)/81306,4)
        X.append(round(num,4))
    # print UD[0]
    plt.scatter(X,MHRW[2],s=50,c='b',marker='v',label = 'MHRW')
    plt.scatter(X,UD[2],s=50,c='r',marker='o',label = 'UD')
    plt.scatter(X,BFS[2],s=50,c='g',marker='s',label = 'BFS')
    plt.scatter(X,RW[2],s=50,c='m',marker='*',label = 'RW')
    plt.plot([0,0.13],[-0.039, -0.039],c='k',linewidth=3.0,label = 'Original')
    plt.xlabel('sampling rate',fontsize=15)
    plt.ylabel('Assortativity',fontsize=15)
    plt.xlim([-0.005,0.14])
    plt.legend()
    plt.show()
assort()





