#!/usr/bin/env python
# coding: utf-8
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# read data of like and dislike
like = pd.read_csv("like2.csv",index_col = 0)
dislike = pd.read_csv("dislike2.csv", index_col = 0)


# split the data set according to class
like_class = []
for i in range(0,8):
    class_i = like[like['class'] == i+1]
    like_class.append(class_i)
dislike_class = []
for i in range(0,8):
    class_i = dislike[dislike['class'] == i+1]
    dislike_class.append(class_i)


# 创建社交网络图
def createGraph(df):
    G = nx.DiGraph()
    G.add_nodes_from(df.iloc[:,0])
    for index, line in df.iterrows():
        k = 3
        while(k <= 5):
            if not pd.isnull(line[k+1]):
                n1 = line[0]
                n2 = int(line[k+1])
                if n2 in G.nodes():
                    G.add_edges_from([(n1, n2)])
            k += 1
    return G


# 以班级为单位，建立like和dislike网络图
# like
like_graph = []
for i in range(0,8):
    graph_i = createGraph(like_class[i])
    like_graph.append(graph_i)
# dislike
dislike_graph = []
for i in range(0,8):
    graph_i = createGraph(dislike_class[i])
    dislike_graph.append(graph_i)

# 以班级为单位，算出所有人的PageRank中心性
# like
like_pr = pd.DataFrame(columns=['like']) # 存储pr值的数据框
for i in range(0,8):
    G = like_graph[i]
    pr = nx.pagerank(G)
    df = pd.DataFrame.from_dict(pr,orient= 'index', columns=['like'])
    like_pr = pd.concat([like_pr,df],axis = 0)
# dislike
dislike_pr = pd.DataFrame(columns=['dislike'])
for i in range(0,8):
    G = dislike_graph[i]
    pr = nx.pagerank(G)
    df = pd.DataFrame.from_dict(pr,orient = 'index', columns=['dislike'])
    dislike_pr = pd.concat([dislike_pr,df],axis = 0)


# 导出like和dislike的PageRank值
id_as_index_like = pd.read_csv("like2.csv",index_col = 1)
classes = class_as_index_like['class']
social_pr = pd.concat([like_pr,dislike_pr,classes],axis = 1)
social_pr.to_csv('social_pagerank.csv')


# 导出like和dislike和PageRank值的合集
id_as_index_like = pd.read_csv("like2.csv",index_col = 1)
id_as_index_dislike = pd.read_csv("dislike2.csv",index_col = 1)
result = pd.concat([id_as_index_like,like_pr,id_as_index_dislike,dislike_pr,],axis = 1)
result = result.iloc[:,[1,2,3,4,5,6,7,8,12,13,14,15,16,17]]
result.to_csv('social_total.csv')
