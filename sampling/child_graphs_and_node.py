# coding=utf-8
# 采样直接生成原始网络的一个子网
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
#######################   UNWEIGHTED  #########################
###############################################################

####################
def uniform_independent_node_sample(G, size=10, size_type='total'):


    size = __size_type_check(G, size, size_type)

    if size_type == 'total':
        R = np.random.randint(0, G.number_of_nodes(), size)
        return np.array(G.nodes())[R]
    else:
        return random.sample(G.nodes(), size)


####################
def random_walk(G, start_node=None, size=10, size_type='total'):

    size = __size_type_check(G, size, size_type)

    if start_node==None:
        start_node = random.choice(G.nodes())

    if size_type=='unique':
        sample_unique = set([start_node])

    SG = nx.Graph()   # TODO

    sample = [start_node] # TODO
    while True:
        neighbors = nx.neighbors(G, sample[-1])
        u = random.choice(neighbors)
        sample.append(u)
        for i in sample[:-1]:
            if i in G.neighbors(sample[-1]):
                SG.add_edge(i,sample[-1])  # TODO
        # collected enough samples?
        if size_type=='total':
            if len(sample) >= size:
                break
        else:  #i.e., size_type=='unique'
            sample_unique.add(u)
            # print len(sample_unique)
            if len(sample_unique) >= size:
                break
    return SG, sample


####################
def metropolis_hastings_random_walk(G, start_node=None, size=10, size_type='total'):


    size = __size_type_check(G, size, size_type)

    if start_node==None:
        start_node = random.choice(G.nodes())

    sample = [start_node]

    if size_type=='unique':
        sample_unique = set([start_node])

    SG = nx.Graph()  # TODO
    while True:
        u = sample[-1]
        neighbors = nx.neighbors(G, u)

        while True:
            w = random.choice(neighbors)
            if random.random() < float(G.degree(u))/G.degree(w):
                sample.append(w)   # move to w accapted
                for i in sample[:-1]:
                    if i in G.neighbors(sample[-1]):
                        SG.add_edge(i,sample[-1])  # TODO
                SG.add_edge(u,w)
                break
            else:
                sample.append(u)   # move to w rejected - resample the current node (as if followed a self-loop)

        # collected enough samples?
        if size_type=='total':
            if len(sample) >= size:
                sample = sample[:size]  # in case we sampled too many in self-loops
                break
        else: #i.e., size_type=='unique'
            sample_unique.add(w)
            # print len(sample_unique)
            if len(sample_unique) >= size:
                break
    return SG,sample


def impore_03(G, start_node=None, size=10, size_type='total', alpa = 0.1):

    size = __size_type_check(G, size, size_type)

    if start_node==None:
        start_node = random.choice(G.nodes())

    sample = [start_node]

    if size_type=='unique':
        sample_unique = set([start_node])

    SG = nx.Graph()  # TODO
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
                for i in sample[:-1]:
                    if i in G.neighbors(sample[-1]):
                        SG.add_edge(i,sample[-1])  # TODO
                SG.add_edge(u,w)
                break
            else:
                if random.random() < alpa:
                    sample.append(u)
                else:
                    if len(dic.get(G.degree(u))) > 0:
                        v = random.choice(list(dic.get(G.degree(u))))
                        sample.append(v)
                        sample_unique.add(v)
                        for i in sample[:-1]:
                            if i in G.neighbors(sample[-1]):
                                SG.add_edge(i,sample[-1])  # TODO
                        SG.add_edge(u,v)
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
    # return sample
    return SG, sample

####################
# def BFS(G,total):
#     SG = nx.Graph()  # TODO
#     buff = set()
#     seed = random.choice(G.nodes())
#     buff.add(seed)
#     nextnodes =  G.neighbors(seed)
#     for i in nextnodes:
#         if i in buff:
#             nextnodes.remove(i)
#         else:
#             buff.add(i)
#             for j in list(buff)[:-1]:
#                 if j in G.neighbors(i):
#                     SG.add_edge(i,j)  # TODO
#             SG.add_edge(i,seed)
#
# 	while True:
#
# 		refer = set()
# 		for i in nextnodes:
# 			for j in G.neighbors(i):
# 				refer.add(j)
#                 SG.add_edge(i,j)
#
# 		for i in buff:
# 			if i in refer:
# 				refer.remove(i)
# 		nextnodes = list(refer)
#
#
# 		for i in nextnodes:
# 			if i in buff:
# 				if i in nextnodes:
# 					nextnodes.remove(i)
# 			else:
# 				buff.add(i)
#                 for j in list(buff)[:-1]:
#                     if j in G.neighbors(i):
#                         SG.add_edge(i,j)  # TODO
#                         print i,j
# 			if len(buff) >= total:
# 				break
#
#
# 		if len(buff) >= total:
# 			break
#
# 	return list(buff)

def BFS(G,total):
    SG = nx.Graph()
    buff = set()
    seed = random.choice(G.nodes())
    buff.add(seed)
    nextnodes =  G.neighbors(seed)
    for i in nextnodes:
        if i in buff:
            nextnodes.remove(i)
        else:
            buff.add(i)
            SG.add_edge(seed,i)
    while True:

        refer = set()
        for i in nextnodes:
            for j in G.neighbors(i):
                refer.add(j)

        for i in buff:
            if i in refer:
                refer.remove(i)
        nextnodes = list(refer)


        for i in nextnodes:
            if i in buff:
                if i in nextnodes:
                    nextnodes.remove(i)
            else:
                buff.add(i)
                for j in list(buff):
                    if j in G.neighbors(i):
                        SG.add_edge(i,j)  # TODO

            if len(buff) >= total:
                break


        if len(buff) >= total:
            break

    return SG


























