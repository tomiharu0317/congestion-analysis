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
from plotroadnet import PlotNetwork

class Centrality(PlotNetwork, InitNetwork):

    initnet = InitNetwork()
    plotnet = PlotNetwork()

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
                func = "nx." + key + "(G2, max_iter=5000, weight='length')"
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
    def sturges_rule(self, centrality_dict):

        centrality_dict = np.asarray(list(centrality_dict.values()))

        class_size = int(np.log2(centrality_dict.size).round()) + 1

        return class_size
    
    # 中心性の値によって決定された階級に基づいて色を決定する
    def set_color(self, index):

        # color_list = px.colors.sequential.Mint
        # color_list = px.colors.sequential.Plotly3
        # color_list = px.colors.sequential.Teal
        # color_list = ['#0508b8', '#1910d8', '#3c19f0', '#6b1cfb', '#981cfd', '#bf1cfd', '#dd2bfd', '#f246fe', '#fc67fd', '#fe88fc', '#fea5fd', '#febefe', '#fec3fe']
        color_list = ['rgb(247,251,255)', 'rgb(222,235,247)', 'rgb(198,219,239)', 'rgb(158,202,225)', 'rgb(107,174,214)', 'rgb(66,146,198)', 'rgb(33,113,181)', 'rgb(8,81,156)', 'rgb(8,48,107)']

        color_list.reverse()

        n = len(color_list)

        if index < n:
            color = color_list[index]
        else:
            color = color_list[-1]

        return color

    def make_different_color_nodes_for_plotly(self, node_list, plotly_data, color, index):

        node_x = []
        node_y = []

        for node in node_list:
            node = node[0]
            node_x.append(self.plotnet.retrieve_coordinate(node)[0])
            node_y.append(self.plotnet.retrieve_coordinate(node)[1])

        nodes = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers',
            marker=dict(size=5,  color=color),
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
            values = [round(val, 7) for val in values]

            df['node'] = nodes
            # df.reindex(nodes)
            # df.index.name = 'node'
            df[key] = values

            print(df)
        
        df.to_csv(filename, mode='w')

    # 値の階級値を決め、それごとにnodes = go.Scatter()で別の色を与えていく
    def plot_centrality(self, key):

        centrality_dict = self.return_centrality_dict(key)
        edges_for_plotly = self.plotnet.make_edges_for_plotly()
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

        filename = 'results/images/html/' + key + '.html'
        fig = go.Figure(plotly_data, layout)
        fig.write_html(filename, auto_open=True)

# cent = Centrality()
# cent.save_all_centrality_to_csv()