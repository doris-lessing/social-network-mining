#!/usr/bin/env python
# coding: utf-8

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


# read in data about social network，
# including edges and PageRank Centrality of nodes and gender
social = pd.read_csv("social_total.csv")

#将数据集按班分开
social_class = []
for i in range(0,8):
    class_i = social[social['class'] == i+1]
    social_class.append(class_i)

# 创建社交网络图的函数，包含like和dislike,和gender
def createGraph(df) :
    G = nx.DiGraph()
    G.add_nodes_from(df.iloc[:,0])
    for index, line in df.iterrows():
        n1 = line[0]
        G.nodes[n1]['class_num'] = line[1]
        G.nodes[n1]['gender'] = line[2]
        k = 1
        while(k <= 5):
            if not pd.isnull(line[k+2]):
                n2 = int(line[k+2])
                if n2 in G.nodes():
                    G.add_edges_from([(n1, n2)], like = True)
            k += 1
        k = 1
        while(k <= 5):
            if not pd.isnull(line[k+8]):
                n2 = int(line[k+8])
                if n2 in G.nodes():
                    G.add_edges_from([(n1, n2)], like = False)
            k += 1
    return G


# 以班级为单位，建立social网络图
social_graph = []
for i in range(0,8):
    graph_i = createGraph(social_class[i])
    social_graph.append(graph_i)


total_graph = createGraph(social)
nx.write_gexf(total_graph,'total.gexf')  


for i in range(1,9):
    nx.write_gexf(social_graph[i],'class'+str(i)+'8.gexf')  

