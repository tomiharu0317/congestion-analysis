import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes.function import get_edge_attributes
import japanize_matplotlib
import numpy as np

G = nx.read_graphml('data/tachikawa.graphml')

# network is a digraph.
# print(nx.is_directed(G))

# 基本特徴量---------------------------------------------
# ノード数
# エッジ数
# 次数のヒストグラム
# 次数分布
# 平均次数
# 平均ノード間距離
# ノード間距離の分布
# ネットワークの直径
# エッジ密度
# クラスター係数
# 平均クラスター係数
# 次数中心性
# 固有値中心性
# 媒介中心性
# 近接中心性
# -----------------------------------------------------

# type(nx.nodes(G)) :
# <class 'networkx.classes.reportviews.NodeView'>
node_list = list(nx.nodes(G))

# number of nodes : 4106
num_of_nodes = nx.number_of_nodes(G) 

# number of edges : 10515
num_of_edges = nx.number_of_edges(G)

# degree histgram
degree_list = nx.degree(G)

# A list of frequencies of degrees.
# The degree values are the index in the list. : 
# [0, 0, 763, 56, 482, 116, 2319, 49, 319, 1, 1]
def plot_degree_hist():
    degree_hist = nx.degree_histogram(G)
    max_degree = len(degree_hist) - 1
    labels = range(0, max_degree + 1)

    x = np.arange(len(labels))
    width = 0.7

    fig, ax = plt.subplots()
    rects = ax.bar(x, degree_hist, width)

    ax.set_title('立川市自動車道ネットワークにおける次数のヒストグラム')
    ax.set_xlabel('次数' + r'$k$')
    ax.set_ylabel(r'$n(k)$')

    ax.bar_label(rects)

    fig.tight_layout()

    plt.show()

def plot_degree_dist():
    degree_hist = nx.degree_histogram(G)
    
    num_of_nodes = nx.number_of_nodes(G) 

    degree_dist = make_degree_dist(degree_hist, num_of_nodes)

    max_degree = len(degree_dist) - 1
    labels = range(0, max_degree + 1)

    x = np.arange(len(labels))
    width = 0.7

    fig, ax = plt.subplots()
    rects = ax.bar(x, degree_dist, width)

    ax.set_title('立川市自動車道ネットワークにおける次数分布')
    ax.set_xlabel('次数' + r'$k$')
    ax.set_ylabel(r'$P(k)$')

    ax.bar_label(rects)

    fig.tight_layout()

    plt.show()

def make_degree_dist(degree_hist, num_of_nodes):
    
    degree_dist = [round(n_k / num_of_nodes, 2) for n_k in degree_hist]
    
    return degree_dist

def average_degree():
    num_of_nodes = nx.number_of_nodes(G) 

    avg_deg = round(sum([degree for node, degree in nx.degree(G)]) / num_of_nodes, 2)

    print(avg_deg)

    # return

# result : 4044.685493640773
def average_path_length():


    length_dict = nx.get_edge_attributes(G, name='length')

    # 'length' attributesがstrなのでfloatに変換
    for key, value in length_dict.items():
        length_dict[key] = {'length': round(float(value), 3)}

    nx.set_edge_attributes(G, length_dict)

    print(nx.average_shortest_path_length(G, weight='length', method='dijkstra'))




# print('number of nodes: ', num_of_nodes)
# print('number of edges: ', num_of_edges)
# plot_degree_hist()
# plot_degree_dist()
# average_degree()
# average_path_length()

# print(dict(nx.all_pairs_dijkstra_path_length(G))[])
# print(G.edges())
# print(G.edges.values())
# print(G.edges.items())
# print(nx.is_weighted(G))
# print(G.edges.data('length'))
# print(nx.get_edge_attributes(G, name='length'))