import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import plotly.graph_objects as go
import plotly.express as px
from initnetwork import InitNetwork
from plot import PlotFunc
from centrality import Centrality
from plotshortestpath import PlotShortestPath

class PlotMinTimePath(PlotShortestPath, Centrality, PlotFunc, InitNetwork):

    initnet = InitNetwork()

    def __init__(self):
        self.node_data_dict = dict(self.G.nodes.data())
        self.initnet.__init__()

    def shape_maxspeed(self, maxspeed):
    # {"['30', '.30']", "['40', '30']", '30;40', '80', "['40', '50']",
    # '100', '40', "['30', '20']", '60', "['60', '50']", "['100', '80']",
    # "['60', '06']", "['20', '30']", "['40', '30;40']", "['40', '60']",
    # '50', '20', '15', "['40', '100']", '30'}
    # set(maxspeed_dict.values())

        if maxspeed == "['30', '.30']":
            maxspeed = 30
        elif maxspeed == "['60', '06']":
            maxspeed = 60
        elif maxspeed == "['06', '60']":
            maxspeed = 60
        elif maxspeed == "['40', '30']":
            maxspeed = 35
        elif maxspeed == "['30', '40']":
            maxspeed = 35
        elif maxspeed == "['40', '50']":
            maxspeed = 40
        elif maxspeed == "['50', '40']":
            maxspeed = 40
        elif maxspeed == "['30', '20']":
            maxspeed = 25
        elif maxspeed == "['20', '30']":
            maxspeed = 25
        elif maxspeed == "['40', '60']":
            maxspeed = 50
        elif maxspeed == "['60', '50']":
            maxspeed = 55
        elif maxspeed == "['100', '80']":
            maxspeed = 90
        elif maxspeed == "['40', '100']":
            maxspeed = 70
        elif maxspeed == "['100', '40']":
            maxspeed = 70
        elif maxspeed == "['40', '30;40']":
            maxspeed = 35
        elif maxspeed == "30;40":
            maxspeed = 35
        else:
            maxspeed = int(maxspeed)

        return maxspeed

    def add_required_time_attributes(self):
        required_time_dict = dict()
        
        maxspeed_dict = nx.get_edge_attributes(self.G, name='maxspeed')
        maxspeed_defined_edges = set(maxspeed_dict.keys())

        length_dict = nx.get_edge_attributes(self.G, name='length')

        for edge, length in length_dict.items():

            if edge in maxspeed_defined_edges:
                maxspeed = self.shape_maxspeed(maxspeed_dict[edge])
            else:
                maxspeed = 20
            
            # 時間単位: m / (m (km * 1000) / h) (時間)
            required_time = (float(length) / (maxspeed * 1000))

            required_time_dict[edge] = {'required_time': float(required_time)}

        nx.set_edge_attributes(self.G, required_time_dict)

    def retrieve_start_nodes_randomly(self):

        node_set = set()

        node_list = list(self.G.nodes())
        num_of_nodes = len(node_list)

        node_num = 6000
        node_count = 0

        while node_count < node_num:
            index = random.randint(0, num_of_nodes - 1)
            node = node_list[index]

            if node not in node_set and node != '912045522':
                node_count += 1
                node_set.add(node)

        return node_set

    def add_road(self, node_li, length, maxspeed):

        source = node_li[0]
        target = node_li[1]
        
        self.G.add_edge(source, target, length=length, maxspeed=maxspeed)
        self.G.add_edge(target, source, length=length, maxspeed=maxspeed)


    def plot_new_road(self, node_li):

        self.add_road(node_li, length='400', maxspeed='40')

        node_set = set()

        for node in node_li:
            node_set.add(node)

        node_for_plotly = self.node_set_to_nodes_for_plotly(node_set, size=6, color='red')

        edges_for_plotly = self.whole_edges_for_plotly()

        data = [edges_for_plotly, node_for_plotly]

        data.append(node_for_plotly)
        title_text = '新しい道路'
        layout = self.return_base_layout(title_text, showlegend=False)
        filename = 'results/target_region_2/html/newroad.html'

        self.plot(data, layout, filename)

    def plot_min_time_path(self):

        # 新しい道路の設置 ----------------------------------------------
        # 新しい道路1
        # node_li = ['921406627', '285331253']
        # length = '200', maxspeed = '40'
        
        # 新しい道路2
        node_li = ['948829609', '534240033']

        self.add_road(node_li, length='400', maxspeed='50')

        # 所要時間データを各エッジに追加
        self.add_required_time_attributes()

        edges_for_plotly = self.whole_edges_for_plotly()

        dest_node_set = set()
        dest_node_set.add('912045522')
        dest_node_for_plotly = self.node_set_to_nodes_for_plotly(dest_node_set, size=6, color='blue')

        data = [edges_for_plotly]

        # 35.665以南のノードを出発地点とする ------------------------
        start_node_set = self.retrieve_start_nodes()

        # 新しい道路に目的地までの経路がちゃんとあるか確認 -------------
        # start_node_set = set()
        # start_node_set.add('948829609')

        # 出発地点をランダムに選択 ---------------------------------
        # start_node_set = self.retrieve_start_nodes_randomly()

        shortest_path_list = self.make_shortest_path_list(start_node_set, '912045522', 'required_time')
        # shortest_path_list = self.make_shortest_path_list_from_csv('results/target_region_2/min_time_path_to_dest_newroad_40.csv', 'min_time_path')

        self.path_list_to_csv(shortest_path_list, 'min_time_path', 'results/target_region_2/min_time_path_to_dest_newroad_2_50.csv')

        edge_used_num_dict = self.make_edge_used_num_dict(shortest_path_list) 

        class_size = self.sturges_rule(edge_used_num_dict)

        data = self.add_shortest_path_edges_for_plotly(edge_used_num_dict, class_size, data)

        data.append(dest_node_for_plotly)
        title_text = '新しい道路(50km/h)を追加した場合の昭和記念公園までの最短時間経路'

        layout = self.return_base_layout(title_text, showlegend=True)
        filename = 'results/target_region_2/html/min_time_path_to_dest_newroad_2_50.html'

        self.plot(data, layout, filename)

    def main(self):

        self.plot_min_time_path()

        return

# node_li = ['948829609', '534240033']
# node_li = ['921406627', '285331253']
# plot.plot_new_road(node_li)
# plot = PlotMinTimePath()
# plot.main()