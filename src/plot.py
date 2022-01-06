import networkx as nx
from networkx.classes.function import edges
import plotly.graph_objects as go
import plotly.express as px
from initnetwork import InitNetwork

class PlotFunc(InitNetwork):

    initnet = InitNetwork()

    def __init__(self):
        self.node_data_dict = dict(self.G.nodes.data())
        self.initnet.__init__()

    def retrieve_coordinate(self, node):

        x = float(self.node_data_dict[node]['x'])
        y = float(self.node_data_dict[node]['y'])

        return [x,y]

    def node_set_to_nodes_for_plotly(self, node_set, size, color):

        node_x = []
        node_y = []

        for node in node_set:
            node_x.append(self.retrieve_coordinate(node)[0]) 
            node_y.append(self.retrieve_coordinate(node)[1])

        nodes = go.Scatter(
            showlegend=False,
            x=node_x,
            y=node_y,
            mode='markers',
            marker=dict(size=size, color=color)
        )

        return nodes

    def edge_set_to_edges_for_plotly(self, edge_set, width, color):

        edge_x = []
        edge_y = []

        for edge in edge_set:

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
            line = dict(width = width, color=color),
            showlegend=False
        )

        return edges

    def whole_nodes_for_plotly(self):

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


    def whole_edges_for_plotly(self):

        edge_x = []
        edge_y = []

        edge_set = set(self.G.edges())

        for edge in edge_set:

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

    def set_color(self, index):

        # color_list = px.colors.sequential.Mint
        # color_list = px.colors.sequential.Plotly3
        # color_list = px.colors.sequential.Teal
        color_list = ['#0508b8', '#1910d8', '#3c19f0', '#6b1cfb', '#981cfd', '#bf1cfd', '#dd2bfd', '#f246fe', '#fc67fd', '#fe88fc', '#fea5fd', '#febefe', '#fec3fe']
        # color_list = ['rgb(247,251,255)', 'rgb(222,235,247)', 'rgb(198,219,239)', 'rgb(158,202,225)', 'rgb(107,174,214)', 'rgb(66,146,198)', 'rgb(33,113,181)', 'rgb(8,81,156)', 'rgb(8,48,107)']

        # color_list.reverse()

        n = len(color_list)

        if index < n:
            color = color_list[index]
        else:
            color = color_list[-1]

        return color

    def return_base_layout(self, title_text):

        layout = go.Layout(
            title = dict(
                text = title_text,
                font = dict(size=20, color='gray'),
            ),
            # showlegend=False,
            xaxis=dict(title='longitude', showline=True, linewidth=1, linecolor='lightgray'),
            yaxis=dict(title='latitude', showline=True, linewidth=1, linecolor='lightgray'),
            plot_bgcolor='white',
            width=800,
            height=600
        )

        return layout

    def plot(self, data, layout, filename):

        fig = go.Figure(data, layout)
        fig.write_html(filename, auto_open=True)

