import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from initnetwork import InitNetwork
from plot import PlotFunc
from centrality import Centrality
from plotshortestpath import PlotShortestPath
from plotmintimepath import PlotMinTimePath

class CompareRoads(PlotMinTimePath, PlotShortestPath, Centrality, PlotFunc, InitNetwork):

    initnet = InitNetwork()

    def __init__(self):
        self.node_data_dict = dict(self.G.nodes.data())
        self.initnet.__init__()

    def set_road(self):
        # 新しい道路の追加
        road_li = [['921406627', '285331253'], ['948829609', '534240033']]
        self.add_road(road_li[0], length='200', maxspeed='50')
        self.add_road(road_li[1], length='400', maxspeed='50')            

        # 所要時間データの追加
        self.add_required_time_attributes()

    def make_path_list(self):

        self.set_road()

        # 3つの経路 (出発点:分岐点となる交差点 366264680)
        # 1: '366264680' -> '912045522' (mintimepath)
        # 2: '366264680' -> '921406627' -> '912045522' 
        # 3: '366264680' -> '948829609' -> '912045522' 
        path_list = [['366264680', '912045522'], ['366264680', '921406627', '912045522'], ['366264680', '948829609', '912045522']]
        num_of_path = len(path_list)
        joined_path_list = []

        # 分岐点となる交差点を出発地点とし、中間地点がある場合はそこまでの
        # 最短時間経路と中間地点から目的地までの最短時間経路を合わせたものを
        # その道を使った場合の最短時間経路とする
        for i in range(num_of_path):

            path = path_list[i]
            n = len(path)

            joined_path = ''

            for j in range(n - 1):

                start_node_set = set()
                start_node_set.add(path[j])

                dest_node = path[j + 1]

                mintimepath = self.make_shortest_path_list(start_node_set, dest_node, 'required_time')

                if j == 0 :
                    joined_path = '-'.join(mintimepath[0])
                else:
                    joined_path = joined_path + '-' + '-'.join(mintimepath[0])

            joined_path_list.append(joined_path)

        # csvに保存
        header = 'mintimepath'
        filename = ''
        path_dict = {header: joined_path_list}
        df = pd.DataFrame(path_dict)
        df.to_csv('results/target_region_2/csv/compareroads/mintimepath_eachroads.csv')

    def plot_target_roads(self):

        # 目的地のノード
        dest_node_set = set()
        dest_node_set.add('912045522')

    def main(self):
        self.make_path_list()

compare = CompareRoads()
compare.main()