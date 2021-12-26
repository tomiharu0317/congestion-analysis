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

class PlotNetwork(InitNetwork):

    node_data_dict = {}

    def __init__(self):
        self.node_data_dict = dict(self.G.nodes.data())

    def retrieve_coordinate(self, node):

        x = float(self.node_data_dict[node]['x'])
        y = float(self.node_data_dict[node]['y'])

        return [x,y]

    def make_nodes_for_plotly(self):

        node_x = []
        node_y = []

        for node, data in self.node_data_dict.items():
            node_x.append(self.retrieve_coordinate(node)[0]) 
            node_y.append(self.retrieve_coordinate(node)[1])

        nodes = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers',
            marker=dict(size=3, line=dict(width=1, color='red'))
        )

        return nodes

    def make_edges_for_plotly(self):

        edge_x = []
        edge_y = []

        edge_list = list(self.G.edges())

        for edge in edge_list:

            source = edge[0]
            target = edge[1]

            source_coordinate = self.retrieve_coordinate(source)
            target_coordinate = self.retrieve_coordinate(target)

            # source node coordinate
            edge_x.append(source_coordinate[0])
            edge_y.append(source_coordinate[1])

            # target node coordinate
            edge_x.append(target_coordinate[0])
            edge_y.append(target_coordinate[1])
            
            # edge delimiter
            edge_x.append(None)
            edge_y.append(None)

        edges = go.Scatter(
            x = edge_x,
            y = edge_y,
            mode = 'lines',
            opacity = 0.7,
            line = dict(width = 1, color='gray'),
            showlegend=False
        )

        return edges


    # plot road network using plotly
    def plot_road_network(self):


        nodes_for_plotly = self.make_nodes_for_plotly()
        edges_for_plotly = self.make_edges_for_plotly()

        # plotly Figure params
        data = [edges_for_plotly, nodes_for_plotly]
        layout = go.Layout(
            title = dict(
                text = 'Road Network in Tachikawa',
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

        # FIXME:filename
        fig.write_html('tachikawa.html', auto_open=True)


plotnet = PlotNetwork()
plotnet.plot_road_network()