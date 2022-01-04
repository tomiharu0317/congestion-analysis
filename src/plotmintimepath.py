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
    # {"['30', '.30']", "['40', '30']", '30;40', '80', "['40', '50']",
    # '100', '40', "['30', '20']", '60', "['60', '50']", "['100', '80']",
    # "['60', '06']", "['20', '30']", "['40', '30;40']", "['40', '60']",
    # '50', '20', '15', "['40', '100']", '30'}
    # set(maxspeed_dict.values())

        if maxspeed == "['30', '.30']":
            maxspeed = 30
        elif maxspeed == "['60', '06']":
            maxspeed = 60
        elif maxspeed == "['40', '30']":
            maxspeed = 35
        elif maxspeed == "['40', '50']":
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
                maxspeed = 40
            
            # 時間単位:(分)
            required_time = (float(length) / (maxspeed * 1000))*60

            required_time_dict[edge] = {'required_time': float(required_time)}

        nx.set_edge_attributes(self.G, required_time_dict)


    def plot_min_time_path(self):
        return

plot = PlotMinTimePath()
plot.add_required_time_attributes()
