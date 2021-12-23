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

    manipulatecsv.write_to_csv(key, average_path_length, filename)

# diameter --------------------------------------------------------------------------------------

# 全てのshortest path lengthから最大のものを取得しdiameterとする
def retrieve_diameter():

    diameter = 0
    path = []

    # shortest_path_length_dict = {
    #     source node : {
    #         target node: length,
    #         target node: length
    #     }
    # }
    # shortest_path_length_dict = dict(nx.shortest_path_length(G, weight='length'))
    shortest_path_length_dict = dict(nx.all_pairs_dijkstra_path_length(G, weight='length'))

    # -------------------------------------------------------
    for source_node, length_dict in list(shortest_path_length_dict.items()):
        length_dict = dict(length_dict)

        max_length = max(length_dict.values())

        if diameter < max_length:

            diameter = max_length

            for target_node, length_to_target in length_dict.items():

                if diameter == length_to_target:
                    path = [source_node, target_node]

    path = '-'.join(path)

    manipulatecsv.write_to_csv('diameter', diameter, filename)
    manipulatecsv.write_to_csv('diameter_source_target', path, filename)

# [source, target] から さらに細かい path を取得 
def retrieve_diameter_path():
    source_target = manipulatecsv.retrieve_value_from_csv('diameter_source_target', filename).split('-')
    
    source_node = source_target[0]
    target_node = source_target[1]

    diameter_path = nx.dijkstra_path(G, source_node, target_node, weight='length')
    diameter_path = '-'.join(diameter_path)

    manipulatecsv.write_to_csv('diameter_path', diameter_path, filename)

# TODO: ノードをつなぐエッジに色を与えてプロットする
def plot_diameter():
    return
    

# --------------------------------------------------------------------------------------------

# mini network test --------------------------------------------------------------------------

# execute function ---------------------------------------------------------------------------
# print('number of nodes: ', num_of_nodes)
# print('number of edges: ', num_of_edges)
# plot_degree_hist()
# plot_degree_dist()
# average_degree()
# average_path_length()
# path_length()
# retrieve_diameter()
# retrieve_diameter_path()
# plot_diameter()


# --------------------------------------------------------------------------------------------

# other feature values -----------------------------------------------------------------------

# edge length distribution ----------------------------------------------------------------

# FIXME
# 道路の長さで重み付けした最短距離の平均通過交差点数は
# all_pairs_dijkstraで計算できる
# len(path)ごとにlengthを集計して平均すれば良い
def path_length():

    shortest_path_dict = dict(nx.all_pairs_dijkstra_path(G, weight='length'))

    print(shortest_path_dict["190137856"]["190137876"])
    # path_length_dict = dict(nx.all_pairs_dijkstra_path_length(G, weight='length'))
    # print(path_length_dict["190137856"]["190137876"])


# retrieve diameter method2-----------------------------------------------------------------

# TODO: diameterの値を持つshorest pathを取得する
def retrieve_diameter_path_2():

    length_key = 'diameter'
    path_key = 'diameter_path'

    # diameter = float(manipulatecsv.retrieve_value_from_csv('diameter', filename))
    diameter = float(0)
    diameter_path = []

        # all_pairs_shortest_path_length_dict = {
    #     "source node1": (
    #         {
    #             "target node": length from source node to target node,
    #         }, 
    #         {
    #                             # path to target node
    #             "target node": [node1, node2, node3],
    #         }
    # ),
    # }
    all_pairs_shortest_path_length_dict = dict(nx.all_pairs_dijkstra(G, weight='length'))

    # n: num_of_nodes = 4106
    n = len(all_pairs_shortest_path_length_dict)

    value_list = list(all_pairs_shortest_path_length_dict.values())

    # FIXME: 別のやり方として、max_lengthを取得し、そのvalueを持つkey:pathを取得

    # value_list[n]: node n の tuple({length}, {path})
    # value_list[n][0] : node n から各 target node への length dict
    # value_list[n][1] : node n から各 target node への path dict
    for source_node_i in range(n):
        length_list = list(value_list[source_node_i][0].values())
        path_list = list(value_list[source_node_i][1].values())

        for target_node_j in range(n):
            # print(float(length_list[target_node_j]))
            length_to_target_node = float(length_list[target_node_j])

            if length_to_target_node > diameter:
            # if float(length_list[target_node_j]) == diameter:
                diameter = length_to_target_node
                diameter_path = path_list[target_node_j]

                print(diameter)
                print(diameter_path)

                break
        break

    manipulatecsv.write_to_csv(length_key, diameter, filename)
    manipulatecsv.write_to_csv(path_key, diameter_path, filename)

# ----------------------------------------------------------------------------------------------