#!/bin/env python
# coding=utf-8
import networkx as nx


class FaceData:

    def __init__(self):
        self.G = nx.Graph()

    def create_graph(self):
        # f = open("../dataSet/soc-Epinions1.txt", "r")
        # f = open("../dataSet/twitter_combined.txt", "r")
        f = open("../dataSet/facebook_combined.txt", "r")
        # f = open("../dataSet/email2.txt", "r")
        count = 0
        try:
            # twitter
            for line in f:
                self.G.add_edge(line.split(" ")[0], line.split(" ")[1][:-1])
                # a, b = line.split("\t")
                # self.G.add_edge(a, b.split("\r")[0])
                count += 1
                if count == 700:
                    f.close()
                    return self.G
        finally:
            f.close()
            return self.G
