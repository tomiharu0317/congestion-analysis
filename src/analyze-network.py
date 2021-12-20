import networkx as nx
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np

G = nx.read_graphml('data/tachikawa.graphml')

# network is a digraph.
print(nx.is_directed(G))

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

plot_degree_hist()


print('number of nodes: ', num_of_nodes)
print('number of edges: ', num_of_edges)
