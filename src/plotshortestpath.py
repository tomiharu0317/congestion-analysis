import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from initnetwork import InitNetwork
from plotroadnet import PlotNetwork

class PlotShortestPath(PlotNetwork, InitNetwork):

    initnet = InitNetwork()
    plotnet = PlotNetwork()

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
            x=node_x,
            y=node_y,
            mode='markers',
            marker=dict(size=6, line=dict(width=1, color='green'))
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
    def plot_shortest_path(self, shortest_path_list):

        return

plot = PlotShortestPath()
# plot.make_shortest_path_list()


