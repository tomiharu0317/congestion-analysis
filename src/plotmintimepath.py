import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import plotly.graph_objects as go
import plotly.express as px
from initnetwork import InitNetwork
from plot import PlotFunc
from centrality import Centrality

class PlotMinTimePath(PlotFunc, InitNetwork):

    initnet = InitNetwork()

    def __init__(self):
        self.node_data_dict = dict(self.G.nodes.data())
        self.initnet.__init__()

    def shape_maxspeed(self, maxspeed):

        return maxspeed

    def add_required_time_attributes(self):
        required_time_dict = dict()
        
        maxspeed_dict = nx.get_edge_attributes(self.G, name='maxspeed')
        maxspeed_defined_edges = set(maxspeed_dict.keys())
        
        length_dict = nx.get_edge_attributes(self.G, name='length')

        for edge, length in length_dict.items():

            if edge in maxspeed_defined_edges:
                maxspeed = shape_maxspeed(maxspeed_dict[edge])
            else:
                maxspeed = 40

            required_time = float(length) / (maxspeed * 1000)

            required_time_dict[edge] = {'required_time': float(required_time)}

        nx.set_edge_attributes(self.G, required_time_dict)

    def calc_required_time(self):
        return


    def plot_min_time_path(self):
        return

plot = PlotMinTimePath()
plot.add_required_time_attributes()

# {"['30', '.30']", "['40', '30']", '30;40', '80', "['40', '50']",
# '100', '40', "['30', '20']", '60', "['60', '50']", "['100', '80']",
# "['60', '06']", "['20', '30']", "['40', '30;40']", "['40', '60']",
# '50', '20', '15', "['40', '100']", '30'}
# set(maxspeed_dict.values())

# ['30', '.30'] -> '30'
# ['60', '06']" -> '60'

# ['40', '30'] -> '35'
# ['40', '50'] -> '45'
# ['30', '20'] -> '25'
# ['20', '30'] -> '25'
# ['40', '60'] -> '50'
# ['60', '50'] -> '55'
# ['100', '80'] -> '90'
# ['40', '100'] -> '70'

# '30;40' -> '35'
# ['40', '30;40'] -> '35'
