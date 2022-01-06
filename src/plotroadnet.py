import csv
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import plotly.graph_objects as go
import plotly.express as px
import manipulatecsv
from initnetwork import InitNetwork
from plot import PlotFunc

class PlotNetwork(PlotFunc, InitNetwork):

    def __init__(self):
        self.node_data_dict = dict(self.G.nodes.data())

    # plot road network using plotly
    # code: {1: tachikawa, 2:target_region}
    def plot_road_network(self, code):


        nodes_for_plotly = self.whole_nodes_for_plotly()
        edges_for_plotly = self.whole_edges_for_plotly()

        # plotly Figure params
        data = []
        title_text = ''
        filename = ''

        if code == 1:
            data = [edges_for_plotly, nodes_for_plotly]
            title_text = 'Road Network in Tachikawa'
            filename = 'results/tachikawa/html/tachikawa.html'

        elif code == 2:
            data = [edges_for_plotly]
            title_text = 'Road Network in target region'
            filename = 'results/target_region/html/target_region.html'

        else :
            data = [edges_for_plotly]
            title_text = 'Road Network in target region'
            filename = 'results/target_region_2/html/target_region_2.html'

        layout = go.Layout(
            title = dict(
                text = title_text,
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
        fig.write_html(filename, auto_open=True)

    def plot_koushu_kaidou(self):

        road_name_dict = nx.get_edge_attributes(self.G, 'name')

        koushu_kaidou_edge_set = set()

        for edge, name in road_name_dict.items():
            if name == '甲州街道' or '甲州街道' in name:
                source = edge[0]
                target = edge[1]

                edge = (source, target)

                koushu_kaidou_edge_set.add(edge)

        koushu_kaidou_edges_for_plotly = self.edge_set_to_edges_for_plotly(koushu_kaidou_edge_set, 5, 'red')

        edges_for_plotly = self.whole_edges_for_plotly()

        data = [edges_for_plotly, koushu_kaidou_edges_for_plotly]

        title_text = '甲州街道'
        layout = self.return_base_layout(title_text)
        filename = 'results/target_region_2/html/kokushu_kaidou.html'

        self.plot(data, layout, filename)

        return

    def plot_chuo_expressway(self):

        road_name_dict = nx.get_edge_attributes(self.G, 'name')

        chuo_expressway_edge_set = set()

        for edge, name in road_name_dict.items():
            if name == '中央自動車道' or '中央自動車道' in name:
                source = edge[0]
                target = edge[1]

                edge = (source, target)

                chuo_expressway_edge_set.add(edge)

        chuo_expressway_edges_for_plotly = self.edge_set_to_edges_for_plotly(chuo_expressway_edge_set, 5, 'red')

        edges_for_plotly = self.whole_edges_for_plotly()

        data = [edges_for_plotly, chuo_expressway_edges_for_plotly]

        title_text = '中央自動車道'
        layout = self.return_base_layout(title_text)
        filename = 'results/target_region_2/html/chuo_expressway.html'

        self.plot(data, layout, filename)

        return

    def plot_dest(self):

        edges_for_plotly = self.whole_edges_for_plotly()

        dest_node_set = set()
        dest_node_set.add('912045522')

        dest_node_for_plotly = self.node_set_to_nodes_for_plotly(dest_node_set, size=8, color='red')

        data = [edges_for_plotly, dest_node_for_plotly]

        title_text = '昭和記念公園立川口'
        layout = self.return_base_layout(title_text)
        filename = 'results/target_region_2/html/destination.html'

        self.plot(data, layout, filename)

        return

# plotnet = PlotNetwork()
# plotnet.plot_road_network(3)
# plotnet.plot_dest()
# plotnet.plot_chuo_expressway()
# plotnet.plot_koushu_kaidou()