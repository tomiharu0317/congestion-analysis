import csv
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import plotly.graph_objects as go
import plotly.express as px
import manipulatecsv

class InitNetwork:

    # G = nx.read_graphml('data/road/tachikawa.graphml')
    G = nx.read_graphml('data/road/target_region_2.graphml')

    def __init__(self):
        length_dict = nx.get_edge_attributes(self.G, name='length')

        # 'length' attributesがstrなのでfloatに変換
        for key, value in length_dict.items():
            length_dict[key] = {'length': round(float(value), 3)}

        nx.set_edge_attributes(self.G, length_dict)