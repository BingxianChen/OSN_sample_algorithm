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
def BFS(G, total=100, start_node=None):
    buff = set()
    if start_node == None:
        start_node = random.choice(G.nodes())
	buff.add(start_node)
	nextnodes =  G.neighbors(start_node)
	for i in nextnodes:
		if i in buff:
			nextnodes.remove(i)
		else:
			buff.add(i)
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

			if len(buff) >= total:
				break


		if len(buff) >= total:
			break

	return list(buff)



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
        start_node = weighted_independent_sample(G.degree())

    if size_type=='unique':
        sample_unique = set([start_node])

    sample = [start_node]
    while True:
        neighbors = nx.neighbors(G, sample[-1])
        u = random.choice(neighbors)
        sample.append(u)

        # collected enough samples?
        if size_type=='total':
            if len(sample) >= size:
                break
        else:  #i.e., size_type=='unique'
            sample_unique.add(u)
            if len(sample_unique) >= size:
                break
    # return round(float(len(sample) - len(sample_unique))/len(sample_unique), 4)
    return sample


####################
def metropolis_hastings_random_walk(G, start_node=None, size=10, size_type='total'):


    size = __size_type_check(G, size, size_type)

    if start_node==None:
        start_node = random.choice(G.nodes())

    sample = [start_node]

    if size_type=='unique':
        sample_unique = [start_node]

    while True:
        u = sample[-1]
        neighbors = nx.neighbors(G, u)

        while True:
            w = random.choice(neighbors)
            if random.random() < float(G.degree(u))/G.degree(w):
                sample.append(w)   # move to w accapted
                break
            else:
                sample.append(u)   # move to w rejected - resample the current node (as if followed a self-loop)

        # collected enough samples?
        if size_type=='total':
            if len(sample) >= size:
                sample = sample[:size]  # in case we sampled too many in self-loops
                break
        else: #i.e., size_type=='unique'
            if w not in sample_unique:
                sample_unique.append(w)
            if len(sample_unique) >= size:
                break
    # print "duplicate: ",round(float(len(sample_unique))/len(sample), 4)
    # return round(float(len(sample_unique))/len(sample), 4)
    # return round(float(len(sample) - len(sample_unique))/len(sample_unique), 4)
    return sample



####################
def random_walk_stationary_distribution(G):


    if type(G) != nx.Graph:
        raise nx.NetworkXException("G must be a simple undirected graph!")

    if not nx.is_connected(G):
        raise nx.NetworkXException("G is not connected!")

    tot = 2. * G.number_of_edges()
    pi = {}
    for v in G:
        pi[v] = G.degree(v) / tot
    return pi


###############################################################
#####################  WEIGHTED GRAPH  ########################
###############################################################


####################
def __set_node_weights(G):        #may be useful at some point
    try:
        for u in G:
            G.node[u]['weight'] = sum(G[u][v]['weight'] for v in G[u])
    except:
        raise ValueError("G[u][v]['weight'] probably not defined for some edge")
    return

####################
def __weighted_graph_changed(G):

    __set_node_weights(G)

    try:
        G.__WINS_nodes = np.array(G.nodes())
        G.__WINS_weights_cum = np.cumsum( np.array([G.node[v]['weight'] for v in G.__WINS_nodes]) )
    except:
        raise ValueError("G.node[v]['weight'] probably not defined")

    G.__node = {}
    for v in G:
        G.__node[v] = {}

####################
def weighted_independent_node_sample(G, size=10, size_type='total', graph_changed=True):


    size = __size_type_check(G, size, size_type)

    if graph_changed:
        __weighted_graph_changed(G)

    if size_type=='total':
        R = np.random.rand(size)*G.__WINS_weights_cum[-1]
        sample = G.__WINS_nodes[np.searchsorted(G.__WINS_weights_cum, R)]
        return sample
    else:          # size_type=='unique'
        R = np.random.rand(size)*G.__WINS_weights_cum[-1]
        sample = list(G.__WINS_nodes[np.searchsorted(G.__WINS_weights_cum, R)])
        while len(set(sample))<size:
            R = np.random.rand(size/2)*G.__WINS_weights_cum[-1]
            sample.extend(G.__WINS_nodes[np.searchsorted(G.__WINS_weights_cum, R)])

        while len(set(sample))>size:
            sample.pop()
        return np.array(sample)

####################
def weighted_random_walk(G, start_node=None, size = 10, size_type='total', graph_changed=True):

    size = __size_type_check(G, size, size_type)

    if graph_changed:
        __weighted_graph_changed(G)

    if start_node==None:
        start_node = weighted_independent_node_sample(G, size=1, size_type='total', graph_changed=False)[0]

    if size_type=='unique':
        sample_unique = set([start_node])

    sample = [start_node]
    if size==1:
        return np.array(sample)

    while True:
        u = sample[-1]
        Gu = G.__node[u]
        if not Gu.has_key('W'):
            Gu['W'] = np.cumsum([G[u][v]['weight'] for v in G[u]])
            Gu['N'] = list(G[u])
        i = np.searchsorted(Gu['W'] , random.random()*Gu['W'][-1])
        u = Gu['N'][i]
        sample.append(u)

        if size_type=='total':
            if len(sample)==size:
                break
        else:   # size_type=='unique'
            sample_unique.add(u)
            if len(sample_unique) >= size:
                break

    return np.array(sample)


###############################################################
#######################   ESTIMATORS  #########################
###############################################################



####################
def estimate_size(G, sample, sample_type, label):


    if type(G) != nx.Graph:
        raise nx.NetworkXException("G must be a simple undirected graph!")

    if sample_type not in ('uniform', 'random_walk', 'weighted'):
        raise nx.NetworkXException("Parameter sample_type '%s' not understood. Use 'uniform', 'random_walk' or 'weighted'." % sample_type)


    values = {}
    if type(label) in (list,set):
        node_category_set = set(label)
        for v in sample:
            if v in  node_category_set:
                values[v] = 1
            else:
                values[v] = 0
    else:
        for v in sample:
            if G.node[v]['label']==label:
                values[v] = 1
            else:
                values[v] = 0

    s = estimate_mean(G, values, sample, sample_type)

    if s==0.:
        return None
    else:
        return s



####################
def estimate_mean(G, values, sample, sample_type, label = None):


    if type(G) != nx.Graph:
        raise nx.NetworkXException("G must be a simple undirected graph!")

    if sample_type not in ('uniform', 'random_walk', 'weighted'):
        raise nx.NetworkXException("Parameter sample_type '%s' not understood. Use 'uniform', 'random_walk' or 'weighted'." % sample_type)


    if label == None:    # overall mean
        sample_in_category = sample
    elif type(label) in (list,set):
        node_category_set = set(label)
        sample_in_category = [v for v in sample if v in node_category_set]
    else:              # label refers to G.node[v]['label']
        sample_in_category = [v for v in sample if G.node[v]['label']==label]


    if len(sample_in_category)==0:
        return None
    else:
        if sample_type=='uniform':
            return sum(1.*values[v] for v in sample_in_category) /  len(sample_in_category)
        elif sample_type=='random_walk':
            return sum(1.*values[v]/G.degree(v) for v in sample_in_category) / sum(1./G.degree(v) for v in sample_in_category)
        elif sample_type=='weighted':
            return sum(1.*values[v]/G.node[v]['weight'] for v in sample_in_category) / sum(1./G.node[v]['weight'] for v in sample_in_category)
        