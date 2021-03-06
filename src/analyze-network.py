# 実装されている基本特徴量一覧---------------------------------------------

# - 有向グラフかどうか
# - ノード数

# - エッジ数 1（ノードの双方向にエッジが張られている場合は 2 とカウントされる）
# - 次数のヒストグラム（エッジ数 1 に対応）
# - 次数分布（エッジ数 1 に対応）
# - 平均次数（エッジ数 1 に対応）

# - エッジ数 2（交差点が繋がっている交差点の数をエッジ数とする）
# - 次数のヒストグラム（エッジ数 2 に対応）
# - 次数分布（エッジ数 2 に対応）
# - 平均次数（エッジ数 2 に対応）

# - 平均ノード間距離(道路の長さが距離)
# - ネットワークの直径
# - 直径のプロット
# - エッジ密度
# - クラスター係数（重み付き有向グラフには対応しない）
# - 平均クラスター係数（重み付き有向グラフには対応しない）
# -------------------------------------------------------------------

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
from networkx.classes.function import density, edges, number_of_edges
from networkx.drawing import layout
from networkx.readwrite.graph6 import data_to_n
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from initnetwork import InitNetwork
import japanize_matplotlib
import plotly.graph_objects as go
import plotly.express as px
import manipulatecsv
from plotroadnet import PlotFunc
class AnalyzeNetwork(PlotFunc, InitNetwork):

    initnet = InitNetwork()
    filename = 'results/target_region_2/basic_feature_value.csv'

    def __init__(self):
        self.node_data_dict = dict(self.G.nodes.data())
        self.initnet.__init__()

    def is_digraph(self):
        key = 'is_directed'
        value = nx.is_directed(self.G)
        manipulatecsv.write_to_csv(key, value, self.filename) 

    # number of nodes : 4106
    def num_of_nodes(self):
        key = 'num_of_nodes'
        value = nx.number_of_nodes(self.G)

        manipulatecsv.write_to_csv(key, value, self.filename) 

    # number of edges : 10515
    def num_of_edges(self):
        key = 'num_of_edges'
        value = nx.number_of_edges(self.G)
        manipulatecsv.write_to_csv(key, value, self.filename)

    # degree histgram ------------------------------------------------------------------------

    # A list of frequencies of degrees.
    # The degree values are the index in the list. : 
    # [0, 0, 763, 56, 482, 116, 2319, 49, 319, 1, 1]
    def plot_degree_hist(self):
        degree_hist = nx.degree_histogram(self.G)
        max_degree = len(degree_hist) - 1
        labels = range(0, max_degree + 1)

        x = np.arange(len(labels))
        width = 0.7

        fig, ax = plt.subplots()
        rects = ax.bar(x, degree_hist, width)

        ax.set_title('指定範囲自動車道ネットワークにおける次数のヒストグラム')
        ax.set_xlabel('次数' + r'$k$')
        ax.set_ylabel(r'$n(k)$')

        ax.bar_label(rects)

        fig.tight_layout()
        fig.savefig('results/target_region/images/degree_hist.jpg')

    # degree distribution --------------------------------------------------------------------

    def plot_degree_dist(self):

        degree_dist = self.make_degree_dist()

        max_degree = len(degree_dist) - 1
        labels = range(0, max_degree + 1)

        x = np.arange(len(labels))
        width = 0.7

        fig, ax = plt.subplots()
        rects = ax.bar(x, degree_dist, width)

        ax.set_title('指定範囲自動車道ネットワークにおける次数分布')
        ax.set_xlabel('次数' + r'$k$')
        ax.set_ylabel(r'$P(k)$')

        ax.bar_label(rects)

        fig.tight_layout()
        fig.savefig('results/target_region/images/degree_dist.jpg')


    def make_degree_dist(self):
        degree_hist = nx.degree_histogram(self.G)
        num_of_nodes = nx.number_of_nodes(self.G) 
        
        degree_dist = [round(n_k / num_of_nodes, 2) for n_k in degree_hist]
        
        return degree_dist

    # average degree ---------------------------------------------------------------------------

    # result : 5.12
    def average_degree(self):
        key = 'average_degree'

        num_of_nodes = nx.number_of_nodes(self.G) 

        avg_deg = round(sum([degree for node, degree in nx.degree(self.G)]) / num_of_nodes, 2)

        manipulatecsv.write_to_csv(key, avg_deg, self.filename)

    # average path length ------------------------------------------------------------------------

    # result : 4044.685493640773
    def average_path_length(self):

        key = 'average_path_length'

        average_path_length = nx.average_shortest_path_length(self.G, weight='length', method='dijkstra')

        manipulatecsv.write_to_csv(key, average_path_length, self.filename)

    # diameter --------------------------------------------------------------------------------------

    # 全てのshortest path lengthから最大のものを取得しdiameterとする
    def retrieve_diameter(self):

        diameter = 0
        path = []

        # shortest_path_length_dict = {
        #     source node : {
        #         target node: length,
        #         target node: length
        #     }
        # }
        # shortest_path_length_dict = dict(nx.shortest_path_length(G, weight='length'))
        shortest_path_length_dict = dict(nx.all_pairs_dijkstra_path_length(self.G, weight='length'))

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

        manipulatecsv.write_to_csv('diameter', diameter, self.filename)
        manipulatecsv.write_to_csv('diameter_source_target', path, self.filename)

    # [source, target] から さらに細かい path を取得 
    def retrieve_diameter_path(self):
        source_target = manipulatecsv.retrieve_value_from_csv('diameter_source_target', self.filename).split('-')
        
        source_node = source_target[0]
        target_node = source_target[1]

        diameter_path = nx.dijkstra_path(self.G, source_node, target_node, weight='length')
        diameter_path = '-'.join(diameter_path)

        manipulatecsv.write_to_csv('diameter_path', diameter_path, self.filename)

    def make_diameter_nodes_for_plotly(self, diameter_path_list):

        node_x = []
        node_y = []

        for node in diameter_path_list:
            node_x.append(self.plotnet.retrieve_coordinate(node)[0]) 
            node_y.append(self.plotnet.retrieve_coordinate(node)[1])

        nodes = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers',
            marker=dict(size=6, color='red')
        )

        return nodes

    def plot_diameter(self):

        diameter_path = manipulatecsv.retrieve_value_from_csv('diameter_path', self.filename)
        diameter_path_list = diameter_path.split('-')

        diameter_nodes_for_plotly = self.make_diameter_nodes_for_plotly(diameter_path_list)

        # nodes_for_plotly = make_nodes_for_plotly(node_data_dict)
        edges_for_plotly = self.plotnet.make_edges_for_plotly()

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
        fig.write_html('results/target_region_2/html/diameter.html', auto_open=True)
        
    # density ------------------------------------------------------------------------------------
    def calc_density(self):
        key = 'density'
        density_val = round(nx.density(self.G),8)

        manipulatecsv.write_to_csv(key, density_val, self.filename)

    # cluster coefficient-------------------------------------------------------------------------
    def calc_cluster_coefficient(self):
        key = 'cluster_coefficient'
        cluster_coefficient = nx.clustering(self.G, weight='length')


    # MultiDiGraphでは計算できないのでDiGraphに変換
    # MultiDiGraph edge num: 10515
    # DiGraph      edge num: 10441 
    # average cluster coefficient-----------------------------------------------------------------
    def calc_avg_cluster_coefficient(self):
        key = 'average_cluster_coefficient'

        G2 = nx.DiGraph(self.G)

        # G2_edges = set(G2.edges())
        # for edge in set(G.edges()):
        #     if edge not in G2_edges:
        #         print(edge)

        avg_cluster_coefficient = round(nx.average_clustering(G2, weight='length'), 7)

        manipulatecsv.write_to_csv(key, avg_cluster_coefficient, self.filename)

    def calc_average_street_count(self):

        key = 'average_street_count'

        num_of_nodes = 0
        degree_sum = 0

        for node, data_dict in self.node_data_dict.items():

            num_of_nodes += 1
            degree_sum += int(data_dict['street_count'])
        
        average_street_count = round((degree_sum / num_of_nodes), 3)

        manipulatecsv.write_to_csv(key, average_street_count, self.filename)

    def make_steet_count_data(self):

        degree_dict = dict()
        degree_set = set()

        for data_dict in self.node_data_dict.values():
            
            degree = int(data_dict['street_count'])

            if degree in degree_dict:
                degree_dict[degree] += 1
            else:
                degree_dict[degree] = 1
                degree_set.add(degree)

        return degree_dict, degree_set


    def plot_street_count_hist(self):

        degree_dict, degree_set = self.make_steet_count_data()

        max_degree = max(degree_set)

        x_data = range(1, max_degree + 1)
        y_data = [0] * (max_degree)
        width = 0.7

        for x in x_data:
            if x in degree_dict:
                y_data[x - 1] = degree_dict[x]      
                
        fig, ax = plt.subplots()
        rects = ax.bar(x_data, y_data, width)

        ax.set_title('指定範囲自動車道ネットワークにおける次数のヒストグラム')
        ax.set_xlabel('次数' + r'$k$')
        ax.set_ylabel(r'$n(k)$')

        ax.bar_label(rects)

        fig.tight_layout()
        fig.savefig('results/target_region_2/images/degree_hist.jpg')
        

    def plot_street_count_dist(self):

        degree_dict, degree_set = self.make_steet_count_data()

        num_of_nodes = nx.number_of_nodes(self.G)
        max_degree = max(degree_set)

        x_data = range(1, max_degree + 1)
        y_data = [0] * (max_degree)
        width = 0.7

        for x in x_data:
            if x in degree_dict:
                y_data[x - 1] = float('{:.3f}'.format(degree_dict[x] / num_of_nodes))

        fig, ax = plt.subplots()
        rects = ax.bar(x_data, y_data, width)

        ax.set_title('指定範囲自動車道ネットワークにおける次数分布')
        ax.set_xlabel('次数' + r'$k$')
        ax.set_ylabel(r'$P(k)$')

        ax.bar_label(rects)

        fig.tight_layout()
        fig.savefig('results/target_region_2/images/degree_dist.jpg')

analyze = AnalyzeNetwork()
# analyze.num_of_nodes()
# analyze.num_of_edges()
analyze.calc_density()
# analyze.calc_average_street_count()
# analyze.plot_street_count_hist()
# analyze.plot_street_count_dist()