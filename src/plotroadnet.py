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
            filename = 'results/images/html/tachikawa.html'

        else:
            data = [edges_for_plotly]
            title_text = 'Road Network in target region'
            filename = 'results/images/html/target_region.html'

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