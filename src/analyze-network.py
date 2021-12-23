import csv
import re
from os import path
import networkx as nx
from networkx.algorithms.assortativity import pairs
from networkx.algorithms.distance_measures import diameter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import manipulatecsv

# sample node
# ["190137856"]["190137876"]

G = nx.read_graphml('data/tachikawa.graphml')
filename = 'results/basic_feature_value.csv'

def edge_length_str_to_float():
    length_dict = nx.get_edge_attributes(G, name='length')

    # 'length' attributesがstrなのでfloatに変換
    for key, value in length_dict.items():
        length_dict[key] = {'length': round(float(value), 3)}

    nx.set_edge_attributes(G, length_dict)

edge_length_str_to_float()

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

def is_digraph():
    key = 'is_directed'
    value = nx.is_directed(G)
    manipulatecsv.write_to_csv(key, value, filename) 

# number of nodes : 4106
def num_of_nodes():
    key = 'num_of_nodes'
    value = nx.number_of_nodes(G)
    manipulatecsv.write_to_csv(key, value, filename) 

# TODO: 一方通行を含む有向グラフに対してどのように計算しているか確認
# number of edges : 10515
def num_of_edges():
    key = 'num_of_edges'
    value = nx.number_of_edges(G)
    manipulatecsv.write_to_csv(key, value, filename)

# degree histgram ------------------------------------------------------------------------

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
    fig.savefig('results/images/degree_hist.jpg')

# degree distribution --------------------------------------------------------------------

def plot_degree_dist():

    degree_dist = make_degree_dist()

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
    fig.savefig('results/images/degree_dist.jpg')


def make_degree_dist():
    degree_hist = nx.degree_histogram(G)
    num_of_nodes = nx.number_of_nodes(G) 
    
    degree_dist = [round(n_k / num_of_nodes, 2) for n_k in degree_hist]
    
    return degree_dist

# average degree ---------------------------------------------------------------------------

# result : 5.12
def average_degree():
    key = 'average_degree'

    num_of_nodes = nx.number_of_nodes(G) 

    avg_deg = round(sum([degree for node, degree in nx.degree(G)]) / num_of_nodes, 2)

    manipulatecsv.write_to_csv(key, avg_deg, filename)

# average path length ------------------------------------------------------------------------

# result : 4044.685493640773
def average_path_length():

    key = 'average_path_length'

    average_path_length = nx.average_shortest_path_length(G, weight='length', method='dijkstra')

# result : 4044.685493640773
def average_path_length():

    edge_length_str_to_float()

    print(nx.average_shortest_path_length(G, weight='length', method='dijkstra'))

# 道路の長さで重み付けした最短距離の平均通過交差点数は
# all_pairs_dijkstraで計算できる
# len(path)ごとにlengthを集計して平均すれば良い
def path_length():

    edge_length_str_to_float()

    shortest_path_dict = dict(nx.all_pairs_dijkstra_path(G, weight='length'))

    print(shortest_path_dict["190137856"]["190137876"])
    # path_length_dict = dict(nx.all_pairs_dijkstra_path_length(G, weight='length'))
    # print(path_length_dict["190137856"]["190137876"])

# print('number of nodes: ', num_of_nodes)
# print('number of edges: ', num_of_edges)
# plot_degree_hist()
# plot_degree_dist()
# average_degree()
# average_path_length()
path_length()

# print(dict(nx.all_pairs_dijkstra_path_length(G))[])
# print(G.edges())
# print(G.edges.values())
# print(G.edges.items())
# print(nx.is_weighted(G))
# print(G.edges.data('length'))
# print(nx.get_edge_attributes(G, name='length'))

# sample node
# ["190137856"]["190137876"]