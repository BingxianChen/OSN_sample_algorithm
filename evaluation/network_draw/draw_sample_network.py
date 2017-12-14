#!/bin/env python
# coding=utf-8
import networkx as nx
from dataImport.draw_data import FaceData
import matplotlib.pyplot as plt
from sampling import common,child_graphs,child_graphs_and_node
import numpy as np


def BFS_subnet():
    # f = FaceData()
    # G = f.create_graph()                     # 获取原始数据
    # G = nx.navigable_small_world_graph(10)
    # G = nx.davis_southern_women_graph()
    G = nx.generators.wheel_graph(70)
    node_colo = []
    edge_colo = []
    node_label = dict()
    Subnet = child_graphs.BFS(G, total=30)
    Subnet.edges()
    for i in G.nodes():
        if i in Subnet.nodes():
            node_colo.append('cyan')
            node_label[i] = 1
        else:
            node_colo.append('black')
    for i in G.edges():
        if i in Subnet.edges():
            edge_colo.append('cyan')
        else:
            edge_colo.append('black')

    degree_set = set()
    for i in G.nodes():
        if G.degree(i) not in degree_set:
            degree_set.add(G.degree(i))
    degree_list = list(degree_set)

    degree_dict = dict()
    start = 300
    dept = 800
    for i in degree_list:
        degree_dict[i] = start
        start += dept
    node_size_list = []
    for i in G.nodes():
        node_size_list.append(degree_dict[G.degree(i)])

    nx.draw(G, pos=nx.spring_layout(G), node_size=node_size_list, node_color=node_colo, edge_color=edge_colo, arrows=False, width=2, labels=node_label)
    plt.show()

def MH_subnet():
    # f = FaceData()
    # G = f.create_graph()                     # 获取原始数据
    # G = nx.navigable_small_world_graph(10)
    # G = nx.davis_southern_women_graph()
    G = nx.generators.wheel_graph(70)
    node_colo = []
    edge_colo = []
    Subnet, sample_node = child_graphs_and_node.metropolis_hastings_random_walk(G, None,30,'unique')

    # 采样节点处理
    node_number_dict = dict()
    for i in sample_node:
        node_number_dict[i] = node_number_dict.get(i,0) + 1

    Subnet.edges()
    for i in G.nodes():
        if i in Subnet.nodes():
            node_colo.append('cyan')
        else:
            node_colo.append('black')
    for i in G.edges():
        if i in Subnet.edges():
            edge_colo.append('cyan')
        else:
            edge_colo.append('black')

    degree_set = set()
    for i in G.nodes():
        if G.degree(i) not in degree_set:
            degree_set.add(G.degree(i))
    degree_list =  list(degree_set)

    degree_dict = dict()
    start = 300
    dept = 800
    for i in degree_list:
        degree_dict[i] = start
        start += dept
    node_size_list = []
    for i in G.nodes():
        node_size_list.append(degree_dict[G.degree(i)])

    nx.draw(G, pos=nx.spring_layout(G), node_size=node_size_list, node_color=node_colo, edge_color=edge_colo, arrows=False, width=2, labels=node_number_dict)
    plt.show()

def RW_subnet():
    # f = FaceData()
    # G = f.create_graph()                     # 获取原始数据
    # G = nx.navigable_small_world_graph(10)
    # G = nx.davis_southern_women_graph()
    G = nx.generators.wheel_graph(70)
    node_colo = []
    edge_colo = []
    Subnet, sample_node = child_graphs_and_node.random_walk(G, None,30,'unique')

    # 采样节点处理
    node_number_dict = dict()
    for i in sample_node:
        node_number_dict[i] = node_number_dict.get(i,0) + 1

    Subnet.edges()
    for i in G.nodes():
        if i in Subnet.nodes():
            node_colo.append('cyan')
        else:
            node_colo.append('black')
    for i in G.edges():
        if i in Subnet.edges():
            edge_colo.append('cyan')
        else:
            edge_colo.append('black')

    degree_set = set()
    for i in G.nodes():
        if G.degree(i) not in degree_set:
            degree_set.add(G.degree(i))
    degree_list =  list(degree_set)

    degree_dict = dict()
    start = 300
    dept = 800
    for i in degree_list:
        degree_dict[i] = start
        start += dept
    node_size_list = []
    for i in G.nodes():
        node_size_list.append(degree_dict[G.degree(i)])

    nx.draw(G, pos=nx.spring_layout(G), node_size=node_size_list, node_color=node_colo, edge_color=edge_colo, arrows=False, width=2, labels=node_number_dict)
    plt.show()

def UD_subnet():
    # f = FaceData()
    # G = f.create_graph()                     # 获取原始数据
    # G = nx.navigable_small_world_graph(10)
    # G = nx.davis_southern_women_graph()
    G = nx.generators.wheel_graph(70)
    node_colo = []
    edge_colo = []
    Subnet, sample_node = child_graphs_and_node.impore_03(G, None, 30, 'unique')

    # 采样节点处理
    node_number_dict = dict()
    for i in sample_node:
        node_number_dict[i] = node_number_dict.get(i,0) + 1

    Subnet.edges()
    for i in G.nodes():
        if i in Subnet.nodes():
            node_colo.append('cyan')
        else:
            node_colo.append('black')
    for i in G.edges():
        if i in Subnet.edges():
            edge_colo.append('cyan')
        else:
            edge_colo.append('black')

    degree_set = set()
    for i in G.nodes():
        if G.degree(i) not in degree_set:
            degree_set.add(G.degree(i))
    degree_list = list(degree_set)

    degree_dict = dict()
    start = 300
    dept = 800
    for i in degree_list:
        degree_dict[i] = start
        start += dept
    node_size_list = []
    for i in G.nodes():
        node_size_list.append(degree_dict[G.degree(i)])

    nx.draw(G, pos=nx.spring_layout(G), node_size=node_size_list, node_color=node_colo, edge_color=edge_colo, arrows=False, width=2, labels=node_number_dict)
    plt.show()



BFS_subnet()
# MH_subnet()
# RW_subnet()
# UD_subnet()