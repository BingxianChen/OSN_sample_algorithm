#!/bin/env python
# coding=utf-8
import networkx as nx


class FaceLargeData:

    def __init__(self):
        self.G = nx.Graph()
    def get_edges(self, line):
        edges = []
        line_list = [int(i) for i in line.split()]
        for i in xrange(2, len(line_list)):
            edges.append((line_list[0], line_list[i]))
        return edges

    def create_graph(self):
        f = open("../dataSet/twitter_combined.txt", "r")
        try:
            count = 0
            for line in f:
                self.G.add_edges_from(FaceLargeData.get_edges(self, line))
                count += 1
                if count%1000 == 1:
                    print count
        finally:
            f.close()
            return self.G





