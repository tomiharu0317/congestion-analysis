import networkx as nx
from networkx.classes.function import edges
from networkx.readwrite.graph6 import data_to_n
import plotly.graph_objects as go
import plotly.express as px
from initnetwork import InitNetwork
from plotroadnet import PlotNetwork
from centrality import Centrality

class PlotShortestPath(Centrality, PlotNetwork, InitNetwork):

    initnet = InitNetwork()
    plotnet = PlotNetwork()
    centrality = Centrality()

    def __init__(self):
        self.node_data_dict = dict(self.G.nodes.data())
        self.initnet.__init__()

    def make_motorway_nodes_for_plotly(self, motorway_node_set):
        
        node_x = []
        node_y = []

        for node in motorway_node_set:
            node_x.append(self.retrieve_coordinate(node)[0]) 
            node_y.append(self.retrieve_coordinate(node)[1])

        nodes = go.Scatter(
            showlegend=False,
            x=node_x,
            y=node_y,
            mode='markers',
            marker=dict(size=3, color='blue')
        )

        return nodes

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


    def plot_motorway(self):

        motorway_node_set = self.retrieve_motorway_nodes()

        edges_for_plotly = self.make_edges_for_plotly()
        nodes_for_plotly = self.make_motorway_nodes_for_plotly(motorway_node_set)

        data = [edges_for_plotly, nodes_for_plotly]

        layout = go.Layout(
            title = dict(
                text = 'Motorway nodes',
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
        fig.write_html('results/images/html/motorway_nodes.html', auto_open=True)

    # 中央自動車道の出口から昭和記念公園入口までの最短経路を算出
    def make_shortest_path_list(self):

        shortest_path_list = []

        source_node_set = self.retrieve_motorway_nodes()

        # dest: 昭和記念公園立川口
        # <node id="912045522">
        #     <data key="d4">35.701684</data>
        #     <data key="d5">139.4056977</data>
        #     <data key="d6">3</data>
        # </node>
        # dest = [139.4056977, 35.701684]
        target_node = "912045522"

        for source_node in source_node_set:

            try: 
                shortest_path = nx.dijkstra_path(self.G, source_node, target_node, weight='length')
                shortest_path_list.append(shortest_path)
            except Exception as e:
                # "270617457" No path to 912045522.
                # "267803815" No path to 912045522.
                print(source_node, e)
                continue

        return shortest_path_list

    # 同じ経路を通るほどその道路の色を濃くする
    # shortest_path_list: [[source, somenodes, target], [source, somenodes, target], ...]
    def make_edge_appearance_list(self, shortest_path_list):

        # all pattern of edges
        # {(source, target), (source, target)}
        edge_pattern_list = set()

        # edge_appearance_dict = {(source, target): num_of_appearance}
        edge_appearance_dict = dict()

        # shortest_path: [source, some nodes, target]
        for shortest_path in shortest_path_list:
            n = len(shortest_path)

            for i in range(n - 1):
                edge =(shortest_path[i], shortest_path[i+1])


                if edge in edge_pattern_list:
                    edge_appearance_dict[edge] += 1
                else:
                    edge_pattern_list.add(edge)
                    edge_appearance_dict[edge] = 1

        max_appearance = max(edge_appearance_dict.values())

        # indexがappearanceの数に対応（降順）
        edge_appearance_list = [list() for i in range(max_appearance)]

        for edge, appearance in edge_appearance_dict.items():
            edge_appearance_list[-appearance].append(edge)

        return edge_appearance_list

    def make_dest_node_for_plotly(self):

        node_x = []
        node_y = []

        node_x.append(self.retrieve_coordinate("912045522")[0]) 
        node_y.append(self.retrieve_coordinate("912045522")[1])

        nodes = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers',
            marker=dict(size=3, color='blue'),
            showlegend=False,
        )

        return nodes

    def add_different_color_edges_to_data(self, edge_list, data, index, max_num_used):

        edge_x = []
        edge_y = []

        for edge in edge_list:

            source = edge[0]
            target = edge[1]

            source_coordinate = self.plotnet.retrieve_coordinate(source)
            target_coordinate = self.plotnet.retrieve_coordinate(target)

            # source node coordinate
            edge_x.append(source_coordinate[0])
            edge_y.append(source_coordinate[1])

            # target node coordinate
            edge_x.append(target_coordinate[0])
            edge_y.append(target_coordinate[1])
            
            # edge delimiter
            edge_x.append(None)
            edge_y.append(None)

        color = self.centrality.set_color(index)

        edges = go.Scatter(
            x = edge_x,
            y = edge_y,
            mode = 'lines',
            opacity = 0.7,
            line = dict(width = 3, color=color),
            name = 'Number of times used' + str(max_num_used - index)
        )

        data.append(edges)

        return data

    def add_shortest_path_edges_for_plotly(self, edge_appearance_list, data):

        max_num_used = len(edge_appearance_list)

        for index in range(max_num_used):
            # edge_list = [(source, target), (source, target)]
            edge_list = edge_appearance_list[index]

            data = self.add_different_color_edges_to_data(edge_list, data, index, max_num_used)

        return data

    def plot_shortest_path(self, edge_appearance_list):

        motorway_node_set = self.retrieve_motorway_nodes()
        nodes_for_plotly = self.make_motorway_nodes_for_plotly(motorway_node_set)

        edges_for_plotly = self.make_edges_for_plotly()
        
        dest_node_for_plotly = self.make_dest_node_for_plotly()

        data = [edges_for_plotly]

        data = self.add_shortest_path_edges_for_plotly(edge_appearance_list, data)

        data.append(nodes_for_plotly)
        data.append(dest_node_for_plotly)

        layout = go.Layout(
            title = dict(
                text = 'shortest path to destination',
                font = dict(size=20, color='gray'),
            ),
            # showlegend=False,
            xaxis=dict(title='longitude', showline=True, linewidth=1, linecolor='lightgray'),
            yaxis=dict(title='latitude', showline=True, linewidth=1, linecolor='lightgray'),
            plot_bgcolor='white',
            width=800,
            height=600
        )

        fig = go.Figure(data, layout)
        fig.write_html('results/images/html/shortest_path_to_dest_2.html', auto_open=True)

    def main(self):

        shortest_path_list = self.make_shortest_path_list()

        edge_appearance_list = self.make_edge_appearance_list(shortest_path_list)

        self.plot_shortest_path(edge_appearance_list)

        return

plot = PlotShortestPath()
plot.main()


