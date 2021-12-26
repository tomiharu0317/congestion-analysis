import csv
import re
import math
from os import path
import networkx as nx
from networkx.algorithms import cluster
from networkx.algorithms.assortativity import pairs
from networkx.algorithms.centrality.degree_alg import in_degree_centrality
from networkx.algorithms.centrality.eigenvector import eigenvector_centrality
from networkx.algorithms.distance_measures import diameter
from networkx.algorithms.shortest_paths import weighted
from networkx.classes.function import density, edges
from networkx.drawing import layout
from networkx.readwrite.graph6 import data_to_n
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import plotly.graph_objects as go
import plotly.express as px
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
# 平均ノード間距離(道路の長さが距離)
# ネットワークの直径(shortest path length の中で最大のもの)
# エッジ密度
# クラスター係数
# 平均クラスター係数
# 次数中心性
# 固有値中心性
# 媒介中心性
# 近接中心性
# ページランク
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

def make_diameter_nodes_for_plotly(diameter_path_list, node_data_dict):

    node_x = []
    node_y = []

    for node in diameter_path_list:
        node_x.append(retrieve_coordinate(node, node_data_dict)[0]) 
        node_y.append(retrieve_coordinate(node, node_data_dict)[1])

    nodes = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        marker=dict(size=6, color='red')
    )

    return nodes

def plot_diameter():

    node_data_dict = dict(G.nodes.data())

    diameter_path = manipulatecsv.retrieve_value_from_csv('diameter_path', filename)
    diameter_path_list = diameter_path.split('-')

    diameter_nodes_for_plotly = make_diameter_nodes_for_plotly(diameter_path_list, node_data_dict)

    # nodes_for_plotly = make_nodes_for_plotly(node_data_dict)
    edges_for_plotly = make_edges_for_plotly(node_data_dict)

    # plotly Figure params
    data = [edges_for_plotly, diameter_nodes_for_plotly]
    layout = go.Layout(
        title = dict(
            text = 'diameter path',
            font = dict(size=20, color='gray'),
        ),
        showlegend=False,
        xaxis=dict(title='longitude', showline=True, linewidth=1, linecolor='lightgray'),
        yaxis=dict(title='latitude', showline=True, linewidth=1, linecolor='lightgray'),
        plot_bgcolor='white',
        width=800,
        height=600
    )

    fig = go.Figure(data, layout)
    fig.write_html('results/images/html/diameter.html', auto_open=True)
    
# density ------------------------------------------------------------------------------------
def calc_density():
    key = 'density'
    density_val = round(nx.density(G), 6)

    manipulatecsv.write_to_csv(key, density_val, filename)

# cluster coefficient-------------------------------------------------------------------------
def calc_cluster_coefficient():
    key = 'cluster_coefficient'
    cluster_coefficient = nx.clustering(G, weight='length')


# MultiDiGraphでは計算できないのでDiGraphに変換
# MultiDiGraph edge num: 10515
# DiGraph      edge num: 10441 
# average cluster coefficient-----------------------------------------------------------------
def calc_avg_cluster_coefficient():
    key = 'average_cluster_coefficient'

    G2 = nx.DiGraph(G)

    # G2_edges = set(G2.edges())
    # for edge in set(G.edges()):
    #     if edge not in G2_edges:
    #         print(edge)

    avg_cluster_coefficient = round(nx.average_clustering(G2, weight='length'),5)

    manipulatecsv.write_to_csv(key, avg_cluster_coefficient, filename)
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
# calc_density()
# calc_cluster_coefficient()
# calc_avg_cluster_coefficient()

# --------------------------------------------------------------------------------------------

# retrieve attiributes from node/edge data
def retrieve_attributes_from_data():
    data_dict = dict(G.nodes.data())
    pos = {}

    for node, data in data_dict.items():
        pos[node] = (float(data_dict[node]['x']), float(data_dict[node]['y']))


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

# ----------------------------------------------------------------------------------------------