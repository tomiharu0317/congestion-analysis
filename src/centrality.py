import csv
import math
from typing import ValuesView
import networkx as nx
from networkx.algorithms import centrality
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import plotly.graph_objects as go
import plotly.express as px
import manipulatecsv
from initnetwork import InitNetwork
from plot import PlotFunc

class Centrality(PlotFunc, InitNetwork):

    initnet = InitNetwork()

    node_data_dict = {}

    keys_require_digraph = ['eigenvector_centrality', 'betweenness_centrality']
    keys_weightname_is_distance = ['closeness_centrality']

    def __init__(self):
        self.node_data_dict = dict(self.G.nodes.data())
        self.initnet.__init__()

    def return_centrality_dict(self, key):
        centrality_dict = {}

        if key in self.keys_require_digraph:

            G2 = nx.DiGraph(self.G)

            if key == 'eigenvector_centrality':
                func = "nx." + key + "(G2, max_iter=5000)"
                centrality_dict = eval(func)
            else:
                func = "nx." + key + "(G2, weight='length')"
                centrality_dict = eval(func)

        else:
            if key in self.keys_weightname_is_distance:
                func = "nx." + key + "(self.G, distance='length')"                
                centrality_dict = eval(func)
            elif key == 'pagerank':
                func = "nx." + key + "(self.G, weight='length')"
                centrality_dict = eval(func)
            else:
                func = "nx." + key + "(self.G)"
                centrality_dict = eval(func)

        return centrality_dict

    # 中心性の値の幅に基づいてスタージェスの公式から階級の数を求める
    def sturges_rule(self, dict):

        dict = np.asarray(list(dict.values()))

        class_size = int(np.log2(dict.size).round()) + 1

        return class_size
    
    def make_different_color_nodes_for_plotly(self, node_list, plotly_data, color, index):

        node_x = []
        node_y = []

        for node in node_list:
            node = node[0]
            node_x.append(self.retrieve_coordinate(node)[0])
            node_y.append(self.retrieve_coordinate(node)[1])

        nodes = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers',
            marker=dict(size=2,  color=color),
            name='class' + str(index + 1)
        )

        plotly_data.append(nodes)

        return plotly_data

    def save_centrality_to_csv(self, key):
        centrality_dict = self.return_centrality_dict(key)
        filename = 'results/centrality.csv'

        df = pd.read_csv(filename)

        # nodes = list(centrality_dict.keys())

        li = list(centrality_dict.values())
        li = [round(val, 7) for val in li]

        df[key] = li

        print(df)

        df.to_csv(filename, mode='w')


    def save_all_centrality_to_csv(self):
        filename = 'results/centrality.csv'

        key_list = ['in_degree_centrality', 'out_degree_centrality', 'eigenvector_centrality', 'betweenness_centrality', 'closeness_centrality', 'pagerank']        
        df = pd.DataFrame()

        for key in key_list:
            centrality_dict = self.return_centrality_dict(key)

            nodes = [node for node in centrality_dict.keys()]

            values = list(centrality_dict.values())

            if key != 'eigenvector_centrality':
                values = [round(val, 7) for val in values]

            df['node'] = nodes
            df[key] = values

            print(df)
        
        df.to_csv(filename, mode='w')

    # 値の階級値を決め、それごとにnodes = go.Scatter()で別の色を与えていく
    def plot_centrality(self, key):

        centrality_dict = self.return_centrality_dict(key)
        edges_for_plotly = self.whole_edges_for_plotly()
        plotly_data = [edges_for_plotly]

        # centralityの値に基づいて降順にソート
        centrality_dict_sorted = sorted(centrality_dict.items(), key=lambda x:x[1], reverse=True)

        # 中心性の値の階級の数をスタージェスの公式から求める
        class_size = self.sturges_rule(centrality_dict)

        # 階級ごとにノードを分け、異なる色を付与してplotly_dataに加える
        num_of_nodes = len(centrality_dict_sorted)
        split_size = math.floor(num_of_nodes / class_size)

        for i in range(class_size):

            # 階級値は切り捨ててあるので、最後のカテゴリーが11 nodes多くなる
            if i != (class_size - 1):
                start = i * split_size
                stop = (i + 1) * split_size

                # node_list = [('node_ID', centrality_val), (), () ...]
                node_list = centrality_dict_sorted[start:stop]
            else:
                start = i * split_size
                node_list = centrality_dict_sorted[start:]

            color = self.set_color(i)
            plotly_data = self.make_different_color_nodes_for_plotly(node_list, plotly_data, color, i)


        # plotly Figure params
        layout = go.Layout(
            title = dict(
                text = key,
                font = dict(size=20, color='gray'),
            ),
            # showlegend=False,
            xaxis=dict(title='longitude', showline=True, linewidth=1, linecolor='lightgray'),
            yaxis=dict(title='latitude', showline=True, linewidth=1, linecolor='lightgray'),
            plot_bgcolor='white',
            width=800,
            height=600
        )

        filename = 'results/target_region_2/html/' + key + '.html'
        fig = go.Figure(plotly_data, layout)
        fig.write_html(filename, auto_open=True)

# cent = Centrality()
# keyli = ['in_degree_centrality', 'out_degree_centrality', 'eigenvector_centrality']
# for key in keyli:
#     print(key)
#     cent.plot_centrality(key)
# cent.plot_centrality('closeness_centrality')