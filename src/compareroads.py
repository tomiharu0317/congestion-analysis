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

    def make_start_dest_node_for_plotly(self, data, color):
        # 目的地を可視化データとして作成して追加 
        dest_node_set = set()
        dest_node_set.add('912045522')
        dest_node_for_plotly = self.node_set_to_nodes_for_plotly(dest_node_set, size=8, color=color)
        data.append(dest_node_for_plotly)

        # 出発地点を可視化データとして作成して追加
        start_node_set = set()
        start_node_set.add('366264680')
        start_node_for_plotly = self.node_set_to_nodes_for_plotly(start_node_set, size=8, color=color)
        data.append(start_node_for_plotly)

        return data

    def plot_target_roads(self):

        # エッジを可視化データとして作成して追加 -------------------
        edges_for_plotly = self.whole_edges_for_plotly()
        data = [edges_for_plotly]
        
        # csvファイルからリストを復元する ------------------------
        filename = 'results/target_region_2/csv/compareroads/mintimepath_eachroads.csv'
        key = 'mintimepath'
        path_list = self.make_shortest_path_list_from_csv(filename, key)

        color_list = ['rgb(228,26,28)', 'rgb(55,126,184)', 'rgb(77,175,74)']
        roadname_list = ['最短時間経路', '新しい道路1', '新しい道路2']
        num_of_path = len(path_list)

        # 可視化の見栄えを良くするためにdataに追加する順番を変える
        road_data = []

        for i in range(num_of_path):

            path = path_list[i]

            edge_set = []
            num_of_edges = len(path)

            for source_j in range(num_of_edges - 1):                
                source = path[source_j]
                target = path[source_j + 1]

                edge_set.append([source, target])

            edges_for_plotly = self.edge_set_to_edges_for_plotly(edge_set, width=4, color=color_list[i], name=roadname_list[i])
            road_data.append(edges_for_plotly)

        # 可視化の見栄えを良くするためにdataに追加する順番を変える
        data.append(road_data[-1])
        data.append(road_data[-2])
        data.append(road_data[-3])

        data = self.make_start_dest_node_for_plotly(data, color='red')
        title_text = '3つの道路比較'
        layout = self.return_base_layout(title_text, showlegend=True)
        filename = 'results/target_region_2/html/compare_roads.html'

        self.plot(data, layout, filename)

    def compare_results_to_csv(self, sum_of_length_list, sum_of_required_time_list):

        results = []
        n = len(sum_of_length_list)
        for i in range(n):
            result_dict = dict()
            
            if i == 0:
                result_dict['name'] = 'mintimeroad'
            elif i == 1:
                result_dict['name'] = 'newroad1'
            else:
                result_dict['name'] = 'newroad2'

            result_dict['length'] = sum_of_length_list[i]
            result_dict['required_time'] = sum_of_required_time_list[i]

            results.append(result_dict)

        df = pd.json_normalize(results)
        df.to_csv('results/target_region_2/csv/compareroads/length_requiredtime_comparison.csv', index=False)

    def compare_length_requiredtime(self):

        self.set_road()

        # csvファイルからリストを復元する ------------------------
        filename = 'results/target_region_2/csv/compareroads/mintimepath_eachroads.csv'
        key = 'mintimepath'
        path_list = self.make_shortest_path_list_from_csv(filename, key)

        length_dict = nx.get_edge_attributes(self.G, name='length')
        required_time_dict = nx.get_edge_attributes(self.G, name='required_time')

        # 全体の最短時間経路: li[0], 新しい道路1: li[1], 新しい道路2: li[2]
        sum_of_length_list = []
        sum_of_required_time_list = []

        for path in path_list:

            sum_of_length = 0
            sum_of_required_time = 0
            num_of_edges = len(path)

            for i in range(num_of_edges - 1):
                key = (path[i], path[i+1], 0)

                try:
                    sum_of_length += float(length_dict[key])
                    sum_of_required_time += float(required_time_dict[key])
                
                # 同じノードに対してエッジを張っている例外がある
                # ('921406627', '921406627', 0)
                # ('948829609', '948829609', 0)
                except KeyError as e:
                    print(e)
                    continue

            sum_of_length_list.append(round(sum_of_length, 3))
            sum_of_required_time_list.append(round(sum_of_required_time, 5))

        self.compare_results_to_csv(sum_of_length_list, sum_of_required_time_list)

    def make_roadspeed_dict(self, path_list):

        maxspeed_dict = nx.get_edge_attributes(self.G, name='maxspeed')
        
        # roadspeed_dict = {
        #     speed: edge_list
        #     }
        # }
        roadspeed_dict = dict()

        for path in path_list:
            num_of_edges = len(path)

            for i in range(num_of_edges - 1):
                key = (path[i], path[i+1], 0)
                edge = (path[i], path[i+1])

                try:
                    maxspeed = float(maxspeed_dict[key])

                # 最高速度が存在しない道路は大きな道路ではないと仮定して
                # 20kmに設定
                except KeyError as e:
                    print(e)
                    maxspeed = float(20)

                if maxspeed in roadspeed_dict:
                    roadspeed_dict[maxspeed].append(edge)
                else:
                    roadspeed_dict[maxspeed] = []
                    roadspeed_dict[maxspeed].append(edge)

        roadspeed_dict = dict(sorted(roadspeed_dict.items(), reverse=True))

        return roadspeed_dict

    def plot_maxspeed(self):

        self.set_road()

        # csvファイルからリストを復元する ------------------------
        filename = 'results/target_region_2/csv/compareroads/mintimepath_eachroads.csv'
        key = 'mintimepath'
        path_list = self.make_shortest_path_list_from_csv(filename, key)

        # 法定速度ごとにグループ化されたエッジリストを作成
        roadspeed_dict = self.make_roadspeed_dict(path_list)

        # エッジを可視化データとして作成して追加 -------------------
        edges_for_plotly = self.whole_edges_for_plotly()
        data = [edges_for_plotly]

        # グループごとに異なる色をつけてプロット
        for maxspeed, edge_list in roadspeed_dict.items():
            
            color = ''
            if maxspeed == float(50):
                index = 0
                color = self.set_color(index)
            elif maxspeed == float(40):
                index = 3
                color = self.set_color(index)
            elif maxspeed == float(30):
                index = 6
                color = self.set_color(index)
            else:
                index = 9
                color = self.set_color(index)

            name = '法定速度' + str(int(maxspeed)) + 'km'
            edges = self.edge_set_to_edges_for_plotly(edge_list, width=4, color=color, name=name)
            data.append(edges)

        data = self.make_start_dest_node_for_plotly(data, color='blue')
        title_text = '3つの道路の法定速度比較'
        layout = self.return_base_layout(title_text, showlegend=True)
        filename = 'results/target_region_2/html/road_maxspeed_comparison.html'

        self.plot(data, layout, filename)

    def main(self):
        # self.make_path_list()
        # self.plot_target_roads()
        # self.compare_length_requiredtime()
        self.plot_maxspeed()

compare = CompareRoads()
compare.main()