import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
from networkx.classes.function import edges, number_of_edges
from networkx.readwrite.graph6 import data_to_n
import plotly.graph_objects as go
import plotly.express as px
from initnetwork import InitNetwork
from plot import PlotFunc
from centrality import Centrality
class PlotShortestPath(Centrality, PlotFunc, InitNetwork):

    initnet = InitNetwork()

    def __init__(self):
        self.node_data_dict = dict(self.G.nodes.data())
        self.initnet.__init__()

    # latitudeが35.66以下のノードからスタートする
    # attributes name: y
    def retrieve_start_nodes(self):

        node_set = set()
        
        for node, data_dict in self.node_data_dict.items():
            if float(data_dict['y']) <= float(35.66):
                node_set.add(node)

        return node_set

    def retrieve_motorway_nodes(self):

        road_name_dict = nx.get_edge_attributes(self.G, 'name')

        motorway_node_set = set()

        for edge, name in road_name_dict.items():
            if name == '中央自動車道' or '中央自動車道' in name:
                source = edge[0]
                target = edge[1]

                motorway_node_set.add(source)
                motorway_node_set.add(target)

        # {'267803464', '260715070', '266949762', '267091414', '267803815',
        # '267803466', '270617457', '287053476', '262596241', '267803515',
        # '278281739', '6882442474', '286839315', '267803526', '260715121',
        # '270491993', '267803495', '267803498', '267776680', '260715110',
        # '260715011', '308923338', '260715112'}
        return motorway_node_set

    # 多対一の最短経路リスト取得関数
    # 中央自動車道の出口から昭和記念公園入口までの最短経路を算出
    def make_shortest_path_list(self, source_node_set, target_node):

        shortest_path_list = []

        # dest: 昭和記念公園立川口
        # <node id="912045522">
        #     <data key="d4">35.701684</data>
        #     <data key="d5">139.4056977</data>
        #     <data key="d6">3</data>
        # </node>
        # dest = [139.4056977, 35.701684]

        for source_node in source_node_set:
            print(source_node)

            try: 
                shortest_path = nx.dijkstra_path(self.G, source_node, target_node, weight='length')
                shortest_path_list.append(shortest_path)
            except Exception as e:
                # "270617457" No path to 912045522.
                # "267803815" No path to 912045522.
                print(source_node, e)
                continue

        # shortest path list をcsvに保存
        try: 
            n = len(shortest_path_list)

            for i in range(n):
                shortest_path_list[i] = '-'.join(shortest_path_list[i])
        
            shortest_path_dict = {'shortest_path': shortest_path_list}
            df = pd.DataFrame(shortest_path_dict)
            df.to_csv('results/shortest_path_to_dest.csv')
    
        except Exception as e:
            print(e)

        return shortest_path_list

    # FIXME: legacy code is here.
    # 同じ経路を通るほどその道路の色を濃くする
    # shortest_path_list: [[source, somenodes, target], [source, somenodes, target], ...]
    def make_edge_appearance_list(self, shortest_path_list):

        # all pattern of edges
        # {(source, target), (source, target)}
        edge_pattern_set = set()

        # edge_appearance_dict = {(source, target): num_of_appearance}
        edge_appearance_dict = dict()

        # shortest_path: [source, some nodes, target]
        for shortest_path in shortest_path_list:
            n = len(shortest_path)

            for i in range(n - 1):
                edge =(shortest_path[i], shortest_path[i+1])


                if edge in edge_pattern_set:
                    edge_appearance_dict[edge] += 1
                else:
                    edge_pattern_set.add(edge)
                    edge_appearance_dict[edge] = 1

        max_num_used = max(edge_appearance_dict.values())

        # indexがその道路が使われた回数に対応（降順）
        edge_appearance_list = [list() for i in range(max_num_used)]

        for edge, num_used in edge_appearance_dict.items():
            edge_appearance_list[-num_used].append(edge)

        return edge_appearance_list

    def make_edge_used_num_dict(self, shortest_path_list):

        # all pattern of edges
        # {(source, target), (source, target)}
        edge_pattern_set = set()

        # edge_appearance_dict = {(source, target): num_of_appearance}
        edge_appearance_dict = dict()

        # shortest_path: [source, some nodes, target]
        for shortest_path in shortest_path_list:
            n = len(shortest_path)

            for i in range(n - 1):
                edge =(shortest_path[i], shortest_path[i+1])


                if edge in edge_pattern_set:
                    edge_appearance_dict[edge] += 1
                else:
                    edge_pattern_set.add(edge)
                    edge_appearance_dict[edge] = 1

        max_num_used = max(edge_appearance_dict.values())

        # edge_used_num_dict = {
        #     num_used: {
        #         edge_list: [],
        #         num_of_edges: len(edge_list)
        #     },
        #     num_used: {
        #         edge_list: [],
        #         num_of_edges: len(edge_list)
        #     },
        #     ...
        # }
        edge_used_num_dict = dict()

        for edge, num_used in edge_appearance_dict.items():
            if num_used in edge_used_num_dict:
                edge_used_num_dict[num_used]['edge_list'].append(edge)
                edge_used_num_dict[num_used]['num_of_edges'] += 1
            else:
                edge_used_num_dict[num_used] = dict()
                edge_used_num_dict[num_used]['edge_list'] = []
                edge_used_num_dict[num_used]['edge_list'].append(edge)
                edge_used_num_dict[num_used]['num_of_edges'] = 1

        edge_used_num_dict = dict(sorted(edge_used_num_dict.items(), reverse=True))

        return edge_used_num_dict

    def add_different_color_edges_to_data(self, edge_list, data, index, class_size):

        edge_x = []
        edge_y = []

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

        color = self.set_color(index)

        edges = go.Scatter(
            x = edge_x,
            y = edge_y,
            mode = 'lines',
            opacity = 0.7,
            line = dict(width = 3, color=color),
            name = 'class' + str(class_size - index)
        )

        data.append(edges)

        return data

    def add_shortest_path_edges_for_plotly(self, edge_used_num_dict, class_size, data):

        class_width = math.ceil(list(edge_used_num_dict.keys())[0] / class_size)

        edge_lists = [list() for i in range(class_size)]

        for num_used, val_dict in edge_used_num_dict.items():

            index = math.ceil(num_used / class_width)

            edge_lists[- index] += val_dict['edge_list']

        for index in range(class_size):
            
            edge_list = edge_lists[index]

            data = self.add_different_color_edges_to_data(edge_list, data, index, class_size)

        return data

    # def add_shortest_path_edges_for_plotly(self, edge_appearance_list, data):

    #     max_num_used = len(edge_appearance_list)

    #     for index in range(max_num_used):
    #         # edge_list = [(source, target), (source, target)]
    #         edge_list = edge_appearance_list[index]

    #         data = self.add_different_color_edges_to_data(edge_list, data, index, max_num_used)

    #     return data

    def make_shortest_path_list_from_csv(self):

        df = pd.read_csv('results/shortest_path_to_dest.csv')

        shortest_path_list = list(df['shortest_path'])
        shortest_path_list = [shortest_path.split('-') for shortest_path in shortest_path_list]

        return shortest_path_list

    def plot_shortest_path(self):

        edges_for_plotly = self.whole_edges_for_plotly()

        # motorway_node_set = self.retrieve_motorway_nodes()
        # nodes_for_plotly = self.node_set_to_nodes_for_plotly(motorway_node_set)
        dest_node_set = set()
        dest_node_set.add('912045522')

        dest_node_for_plotly = self.node_set_to_nodes_for_plotly(dest_node_set, size=6, color='blue')

        data = [edges_for_plotly]

        start_node_set = self.retrieve_start_nodes()

        # shortest_path_list = self.make_shortest_path_list(start_node_set, '912045522')
        shortest_path_list = self.make_shortest_path_list_from_csv()

        # edge_appearance_list = self.make_edge_appearance_list(shortest_path_list) 
        edge_used_num_dict = self.make_edge_used_num_dict(shortest_path_list) 

        class_size = self.sturges_rule(edge_used_num_dict)

        data = self.add_shortest_path_edges_for_plotly(edge_used_num_dict, class_size, data)
        # # data.append(nodes_for_plotly)

        data.append(dest_node_for_plotly)
        title_text = '緯度35.66以南の交差点から昭和記念公園までの最短経路'
        layout = self.return_base_layout(title_text)
        filename = 'results/images/html/shortest_path_to_dest_3.html'

        self.plot(data, layout, filename)

    def plot_motorway(self):

        motorway_node_set = self.retrieve_motorway_nodes()

        edges_for_plotly = self.whole_edges_for_plotly()
        nodes_for_plotly = self.node_set_to_nodes_for_plotly(motorway_node_set, size=3, color='blue')

        data = [edges_for_plotly, nodes_for_plotly]
        layout = self.return_base_layout()
        filename = 'results/images/html/motorway_nodes.html'

        self.plot(data, layout, filename)

    def main(self):

        self.plot_shortest_path()

        return

plot = PlotShortestPath()
plot.main()

        # x_data = list(edge_used_num_dict.keys())
        # x_data.reverse()
        # x_data = np.array(x_data)

        # y_data = []
        # for data in edge_used_num_dict.values():
        #     y_data.append(len(data['edge_list']))
        # y_data.reverse()
        # y_data = np.array(y_data)

        # self.plot_line_graph(x_data, y_data)

    # def test_make_shortest_path_list(self):

    #     source_node_set = set()
    #     source_node_set.add("190197656")
    #     source_node_set.add("190137876")

    #     target_node = '912045522'

    #     shortest_path_list = self.make_shortest_path_list(source_node_set, target_node)

    #     print(shortest_path_list)