#!/bin/env python
# coding=utf-8
import networkx as nx
import numpy as np
import random

###############################################################
##################   AUXILIARY FUNCTIONS  #####################
###############################################################

#####################
def __size_type_check(G, size, size_type):

    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise nx.NetworkXException("No support for multigraphs yet!")

    size = int(size)   #just in case, gets crazy when floats are given

    if size_type != 'unique' and size_type != 'total':
        raise nx.NetworkXException("size_type must be either 'unique' or 'total'!")
    if size_type=='unique' and size > G.number_of_nodes()/2:
        raise nx.NetworkXException("Too many nodes to collect (more than half in the graph)!")
    return size


############################
def weighted_independent_sample(item_weight, size=1):



    if type(item_weight)==type({}):
        items,weights = zip(*item_weight.items())
        items = np.array(items)
    elif type(item_weight) == list:    # list of couples (item,weight)
        items,weights = zip(*item_weight)
        items = np.array(items)
    elif type(item_weight)==type(np.array([])):
        if len(item_weight.shape)!=2:
            print item_weight
            raise ValueError('item_weight matrix is not 2 dimentional')
        if item_weight.shape[1]==2:
            items = item_weight[:,0]
            weights = item_weight[:,1]
        elif item_weight.shape[0]==2:
            items = item_weight[0,:]
            weights = item_weight[1,:]
        else:
            raise ValueError('item_weight is not 2xn or nx2 matrix')
    else:
        raise ValueError('item_weight not understood')


    weights_cum = np.cumsum(weights)
    if size==1:
        R = np.random.rand()*weights_cum[-1]
        return items[np.searchsorted(weights_cum, R)]
    else:
        R = np.random.rand(size)*weights_cum[-1]
        return items[np.searchsorted(weights_cum, R)]

###############################################################
#######################   BFS  #########################
###############################################################

####################
def BFS(G, start_node=None, size=10, size_type='total'):

    size = __size_type_check(G, size, size_type)

    if start_node==None:
        start_node = random.choice(G.nodes())

    if size_type=='unique':
        sample_unique = set([start_node])

    sample = [start_node]

    bfs = nx.bfs_successors(G, sample[-1])
    nodes = set()
    for k,v in bfs.iteritems():
        nodes.add(k)
        for i in v:
            nodes.add(i)
        if len(nodes) > size:
            break
    return list(nodes)








###############################################################
#######################   UNWEIGHTED  #########################
###############################################################

# 改进第一步-----降低度为1的节点的抓取概率,失败---原因是产生偏移了
# 低度节点的入样需要选则等概抽样
# 对于爬取过的节点需要设计缓冲算法以及等概算法
####################
def impore_01(G, start_node=None, size=10, size_type='total'):


    size = __size_type_check(G, size, size_type)

    if start_node==None:
        start_node = random.choice(G.nodes())

    sample = [start_node]

    if size_type=='unique':
        sample_unique = set([start_node])

    # reget = [None,start_node]
    num = 0
    while True:
        u = sample[-1]
        neighbors = nx.neighbors(G, u)
        while True:
            if len(neighbors) == 2:
                # 前一个节点的所有邻居
                # 这个地方需要好好改一下从
                # ns = nx.neighbors(G, sample[-2])
                # sample.append(sample[-1]) #
                # sample_unique.add(sample[-1])
                # for i in ns:
                #     if G.degree(i) < 10:
                #         sample.append(i)
                #         sample_unique.add(i)
                # if sample[-1] != sample[-2]:
                #     sample.append(random.choice(ns))
                # sample_unique.add(sample[-1])
                num += 1
                # break
            w = random.choice(neighbors)
            if random.random() < float(G.degree(u))/G.degree(w):
                sample.append(w)   # move to w accapted
                sample_unique.add(w)
                # reget.append(w)
                break
            else:
                sample.append(u)   # move to w rejected - resample the current node (as if followed a self-loop)
                # if G.degree(w) > G.degree(u):
                #     neighbors.remove(w)

        # collected enough samples?
        if size_type=='total':
            if len(sample) >= size:
                sample = sample[:size]  # in case we sampled too many in self-loops
                break
        else: #i.e., size_type=='unique'
            if len(sample_unique) >= size:
                break
    print "duplicate: ",round(float(len(sample_unique))/len(sample), 4)
    print num
    return sample

# 第二次改进-- 目标:减少低度节点的过度入样!利用缓存队列----改进成功
########################################
def impore_02(G, start_node=None, size=10, size_type='total'):

    size = __size_type_check(G, size, size_type)

    if start_node==None:
        start_node = random.choice(G.nodes())

    sample = [start_node]

    if size_type=='unique':
        sample_unique = set([start_node])

    # 字典存储访问过的节点的邻节点度数信息-----key:度数,value:节点列表
    dic = dict()
    for i in xrange(5000):
        dic[i] = set()
    while True:
        u = sample[-1]
        neighbors = nx.neighbors(G, u)

        # 存储当前节点的邻居节点及其度数信息
        for i in neighbors:
            dic.get(G.degree(i)).add(i)
        while True:
            w = random.choice(neighbors)
            if random.random() < float(G.degree(u))/G.degree(w):
                sample.append(w)   # move to w accapted
                sample_unique.add(w)
                break
            else:
                if len(dic.get(G.degree(u))) > 0:
                    v = random.choice(list(dic.get(G.degree(u))))
                    sample.append(v)
                    sample_unique.add(v)
                else:
                    sample.append(u)   # move to w rejected - resample the current node (as if followed a self-loop)

        # collected enough samples?
        if size_type=='total':
            if len(sample) >= size:
                sample = sample[:size]  # in case we sampled too many in self-loops
                break
        else: #i.e., size_type=='unique'
            if len(sample_unique) >= size:
                break
    # print "duplicate: ",round(float(len(sample_unique))/len(sample), 4)
    # return round(float(len(sample_unique))/len(sample), 4)
    return sample

# 第三次改进-- 目标:提高收敛速度,
########################################
def impore_03(G, start_node=None, size=10, size_type='total', alpa = 0.2):

    size = __size_type_check(G, size, size_type)

    if start_node==None:
        start_node = random.choice(G.nodes())

    sample = [start_node]

    # if size_type=='unique':
    #     sample_unique = set([start_node])
    sample_unique = set([start_node])

    # 字典存储访问过的节点的邻节点度数信息-----key:度数,value:节点列表
    dic = dict()
    for i in xrange(5000):
        dic[i] = set()
    while True:
        u = sample[-1]
        neighbors = nx.neighbors(G, u)

        # 存储当前节点的邻居节点及其度数信息
        for i in neighbors:
            dic.get(G.degree(i)).add(i)
        while True:
            w = random.choice(neighbors)
            if random.random() < float(G.degree(u))/G.degree(w):
                sample.append(w)   # move to w accapted
                sample_unique.add(w)
                break
            else:
                if random.random() < alpa:
                    sample.append(u)
                else:
                    if len(dic.get(G.degree(u))) > 0:
                        v = random.choice(list(dic.get(G.degree(u))))
                        sample.append(v)
                        sample_unique.add(v)
                    else:
                        sample.append(u)   # move to w rejected - resample the current node (as if followed a self-loop)

        # collected enough samples?
        if size_type=='total':
            if len(sample) >= size:
                sample = sample[:size]  # in case we sampled too many in self-loops
                break
        else: #i.e., size_type=='unique'
            if len(sample_unique) >= size:
                break
    # print "duplicate: ",round(float(len(sample_unique))/len(sample), 4)
    # return round(float(len(sample) - len(sample_unique))/len(sample_unique), 4)
    return sample
